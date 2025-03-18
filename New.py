
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
            page.wait_for_timeout(2000)  # Ждем загрузку новых товаров
        else:
            break

def collect_products(page):
    """Собирает названия и цены товаров со страницы."""
    data = []
    product_elements = page.query_selector_all('a.dark_link.js-notice-block__title.option-font-bold.font_sm')

    for product in product_elements:
        title_element = product.query_selector('span')
        title = title_element.inner_text() if title_element else 'Не найдено'

        # Ищем цену внутри родительского блока
        price_block = product.evaluate_handle('el => el.closest(".item_block")')  # Родительский блок товара
        if price_block:
            price_value_element = price_block.query_selector('span.price_value')
            price = price_value_element.inner_text() if price_value_element else ''
        else:
            price = ''

        # Применяем функцию парсинга в зависимости от категории
        parsed_data = None
        if '/catalog/ldsp/' in page.url:
            parsed_data = parse_ldsp(title)
        elif '/catalog/lmdf/' in page.url:
            parsed_data = parse_lmdf(title)
        elif '/catalog/khdf/' in page.url:
            parsed_data = parse_hdf(title)
        elif '/catalog/kromka_pvkh/' in page.url:
            parsed_data = parse_edge_band(title)

        # Добавляем цену и другие данные в итоговый словарь
        parsed_data["Стоимость"] = price
        data.append(parsed_data)

    return data


# Запуск Playwright
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state('load')

        # Список для хранения данных
        data_all = []

        # Перебираем категории ЛДСП, ЛМДФ, ХДФ (с переходом по "kronospan")
        for link in ['/catalog/ldsp/', '/catalog/lmdf/', '/catalog/khdf/']:
            full_link = BASE_URL + link
            page.goto(full_link)
            page.wait_for_load_state('load')

            # Кликаем по ссылке kronospan
            kronospan_link = page.query_selector('a.thumb.shine[href*="kronospan"]')
            if kronospan_link:
                kronospan_link.click()
                page.wait_for_load_state('load')

                # Прокручиваем страницу и собираем товары
                scroll_until_show_more(page)
                data_all.extend(collect_products(page))

        # Обрабатываем категорию "КРОМКА ПВХ" (без перехода по "kronospan")
        page.goto(BASE_URL + '/catalog/kromka_pvkh/')
        page.wait_for_load_state('load')

        # Прокручиваем страницу и собираем товары
        scroll_until_show_more(page)
        data_all.extend(collect_products(page))

        # Сохраняем данные в JSON-файл
        with open("products_new.json", "w", encoding="utf-8") as f:
            json.dump(data_all, f, ensure_ascii=False, indent=4)

        print("Данные сохранены в products.json")

finally:
    browser.close()
