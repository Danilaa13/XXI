import re


# "Артикул материала": f"{material} {group} {thickness} мм {structure} {code}",
# "Наименование материала": f"{material} {group} {thickness} мм {name} {structure} {code}",
# "Наименование группы": f"{group}/{material}/{thickness} мм",
# "Единица измерения": units_of_measurement,
# "Ширина": width,
# "Длина": '',
# "Толщина": thickness,
# "Обозначение": f"{material} {group} {thickness} мм {structure} {code}",


code_pattern = re.compile(r'\b(?:\d{4}[а-яА-Яa-zA-Z]{2}\s{1,2}-\s{1,2}[A-Z0-9]{6}|(?:\d{3,4}\s?-?\s?[A-Z0-9]{3}|[а-яА-Яa-zA-Z]\d{2,3}|[a-zA-Z]{1,2}\.\d{3}\.[A-Z0-9]{2,3}|[a-zA-Z0-9.-]{5,8}))\b')



title = "0101РЕ - 500112U Белый супер шагрень кромка PVC 1134 19/0,4 (300 м),"
code_match = re.search(code_pattern, title)
code = code_match.group(0) if code_match else ''
print(code)