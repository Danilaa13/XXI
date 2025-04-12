import json
from playwright.sync_api import sync_playwright
from parse_ldsp import parse_ldsp
from parse_lmdf import parse_lmdf
from parse_hdf import parse_hdf
from parse_edge_band import parse_edge_band

BASE_URL = 'https://21vekst.ru'

def scroll_until_show_more(page):
    """Прокручивает страницу и нажимает 'Показать еще', пока кнопка существует."""
    while True:
        page.evaluate('window.scrollBy(0, window.innerHeight);')
        show_more_button = page.query_selector('span.more_text_ajax.font_upper_md')
        if show_more_button:
            show_more_button.click()
            page.wait_for_timeout(2000)
        else:
            break

def collect_products(page):
    """Собирает названия и цены товаров со страницы."""
    data = []
    product_elements = page.query_selector_all('a.dark_link.js-notice-block__title.option-font-bold.font_sm')

    for product in product_elements:
        title_element = product.query_selector('span')
        title = title_element.inner_text() if title_element else 'Не найдено'

        price_block = product.evaluate_handle('el => el.closest(".item_block")')
        if price_block:
            price_value_element = price_block.query_selector('span.price_value')
            price = price_value_element.inner_text() if price_value_element else ''
        else:
            price = ''

        parsed_data = None
        if '/catalog/mebelnye_plity/ldsp/' in page.url:
            parsed_data = parse_ldsp(title)
        elif '/catalog/mebelnye_plity/lmdf/' in page.url:
            parsed_data = parse_lmdf(title)
        elif '/catalog/mebelnye_plity/khdf/' in page.url:
            parsed_data = parse_hdf(title)
        elif '/catalog/kromka_pvkh/' in page.url:
            parsed_data = parse_edge_band(title)

        if parsed_data:
            parsed_data["Стоимость"] = price
            data.append(parsed_data)

    return data

# Запуск Playwright
browser = None  # Объявляем заранее, чтобы можно было закрыть в finally
total_count = 0

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(BASE_URL, timeout=60000)
            page.wait_for_load_state('load')
        except Exception as e:
            print(f"[Ошибка загрузки BASE_URL]: {e}")
            browser.close()
            exit()

        data_all = []

        for link in ['/catalog/mebelnye_plity/ldsp/', '/catalog/mebelnye_plity/lmdf/', '/catalog/mebelnye_plity/khdf/']:
            full_link = BASE_URL + link
            try:
                page.goto(full_link, timeout=60000)
                page.wait_for_load_state('load')
            except Exception as e:
                print(f"[Ошибка загрузки категории]: {full_link} — {e}")
                continue

            kronospan_link = page.query_selector('a.thumb[href*="kronospan"]')
            if kronospan_link:
                kronospan_link.click()
                page.wait_for_load_state('load')

                scroll_until_show_more(page)
                products = collect_products(page)
                data_all.extend(products)

                print(f"🔍 Найдено товаров в категории {link}: {len(products)}")
                total_count += len(products)


        try:
            page.goto(BASE_URL + '/catalog/kromka_pvkh/', timeout=60000)
            page.wait_for_load_state('load')
            scroll_until_show_more(page)
            products = collect_products(page)
            data_all.extend(products)

            print(f"🔍 Найдено товаров в категории кромка ПВХ: {len(products)}")
            total_count += len(products)

        except Exception as e:
            print(f"[Ошибка загрузки категории кромки]: {e}")

        with open("products_new.json", "w", encoding="utf-8") as f:
            json.dump(data_all, f, ensure_ascii=False, indent=4)

        print(f"✅ Данные сохранены в products_new.json. Всего товаров собрано: {total_count}")

finally:
    if browser:
        try:
            browser.close()
        except Exception as e:
            print(f"[Ошибка при закрытии браузера]: {e}")
