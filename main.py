import pandas as pd

# Читаем JSON-файл
with open('products_new.json', 'r', encoding='utf-8') as file:
    data = pd.read_json(file)


data = data[~((data['Ширина'] == 1830) & (data['Длина'] == 2500))]
data = data[~data.apply(lambda row: row.astype(str).str.contains('PVC', case=False).any(), axis=1)]
data = data[data['Наименование группы'].str.contains('GP|Galoplast|SPAN', case=False, na=False)]


# Получаем список столбцов
columns = list(data.columns)
thickness_index = columns.index('Толщина')
cost_index = columns.index('Стоимость')
columns.remove('Стоимость')
columns.insert(thickness_index + 1, 'Стоимость')
data = data[columns]
data.to_excel('XXI_new.xlsx', index=False, engine='openpyxl')

print("Файл успешно сохранён как XXI_new.xlsx")