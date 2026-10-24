import csv

with open("sample_cafe_inventory.csv", encoding="utf-8-sig") as file:
    items = csv.reader(file)

    categories = []
    parsing_list = []


    for item in items:
        if item and item[0]:
            # list.append(f"{index}-{item[0].strip()}")
            parsing_list.append(item[0].strip())

    for index, row in enumerate(parsing_list):
        if row == "ITEMS":
            categories.append(parsing_list[index - 1])

    print(categories)