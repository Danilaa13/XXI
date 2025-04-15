import re

import pandas as pd
import os


with open('products_new.json', 'r', encoding='utf-8') as file:
    data = pd.read_json(file)


data = data[~((data['Ширина'] == 1830) & (data['Длина'] == 2500))]
data = data[~data.apply(lambda row: row.astype(str).str.contains('PVC', case=False).any(), axis=1)]
data = data[data['Наименование материала'].str.contains('GP|Galoplast|SPAN', case=False, na=False)]
data = data.drop_duplicates()

# Получаем список столбцов
columns = list(data.columns)
thickness_index = columns.index('Толщина')
cost_index = columns.index('Стоимость')
columns.remove('Стоимость')
columns.insert(thickness_index + 1, 'Стоимость')
data = data[columns]

# Папка с изображениями
image_folder = r"E:\pythonProjectsForUniversity\WORK\PARS_PICTURES\KRONOSPAN\KRONOSPAN_images"

def find_image_by_article(row):
    global image_count
    article = row['Артикул материала']
    # Извлекаем только нужную часть артикула — например, 'К352' из 'К352 RT'
    match = re.match(r'\b(\d{3,4}|[а-яА-Яa-zA-Z]{1,2}\d{2,5})\b', article.strip(), re.IGNORECASE)
    if match:
        base_article = match.group(1)
    else:
        return "Фото не найдено"

    # Поиск файла по извлечённому артикулу
    for file in os.listdir(image_folder):
        if base_article in file and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            return f"\\KRONOSPAN\\{file}"

    return "Фото не найдено"


data['Текстура'] = data.apply(find_image_by_article, axis=1)
data.to_excel('XXI_new.xlsx', index=False, engine='openpyxl')

print("Файл успешно сохранён как XXI_new.xlsx")