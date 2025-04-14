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
image_folder = r"E:\pythonProjectsForUniversity\WORK\PARS_PICTURES\XXI\XXI_images"

def find_image_by_article(row):
    global image_count
    article = row['Артикул материала']
    for file in os.listdir(image_folder):
        if article in file and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            return f"KRONOSPAN\\{file}"
    return "Фото не найдено"

data['Текстура'] = data.apply(find_image_by_article, axis=1)
data.to_excel('XXI_new.xlsx', index=False, engine='openpyxl')

print("Файл успешно сохранён как XXI_new.xlsx")