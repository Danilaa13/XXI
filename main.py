import pandas as pd

# Читаем JSON-файл
with open('products_new.json', 'r', encoding='utf-8') as file:
    data = pd.read_json(file)

# Получаем список столбцов
columns = list(data.columns)

# Находим индекс столбца "Толщина" и "Стоимость"
thickness_index = columns.index('Толщина')  # индекс столбца "Толщина"
cost_index = columns.index('Стоимость')  # индекс столбца "Стоимость"

# Убираем столбец "Стоимость" из списка
columns.remove('Стоимость')

# Вставляем столбец "Стоимость" сразу после "Толщина"
columns.insert(thickness_index + 1, 'Стоимость')

# Переставляем столбцы в DataFrame
data = data[columns]

# Сохраняем в Excel
data.to_excel('XXI_new.xlsx', index=False, engine='openpyxl')

print("Файл успешно сохранён как XXI_new.xlsx")