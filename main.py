import csv

with open("sample_cafe_inventory.csv", encoding="utf-8-sig") as file:
    items = csv.reader(file)

    categories = []
    parsing_list = []
    find_header = []

    inventory = {}
    inventory_item = []


# 기존 csv 파일에서 내용이 있는 셀만 추출
    for item in items:
        if item and item[0]:
            parsing_list.append(item[0].strip())

# 추출된 리스트에서 헤더 역할을 하는 카테고리만 추출
    for index, row in enumerate(parsing_list):
        if row == "ITEMS":
            categories.append(parsing_list[index - 1])


# 카테고리를 상위 레벨로 딕셔너리 구조 생성
    for index, category in enumerate(categories):
        start_index = parsing_list.index(category)
        if index != len(categories) - 1:
            next_category = categories[index + 1]
            end_index = parsing_list.index(next_category)
        # inventory[category] = inventory_item.append(parsing_list[start_index + 1:end_index])
        print(start_index, end_index)

# 규칙이 없는 카테고리 영역 파악
    for index, row in enumerate(parsing_list):
        if row == "Name" or row == "Total":
            find_header.append(f"{row}-{index}")
    

# print(inventory)