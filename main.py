import csv

with open("sample_cafe_inventory.csv", encoding="utf-8-sig") as file:
    inventory = csv.reader(file)

    list = []

    for row in inventory:
        if row and row[0]:
            list.append(row[0].strip())

    print(list)