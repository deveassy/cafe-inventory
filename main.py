import csv

with open("sample_stock_count.csv") as file:
    reader = csv.reader(file)

    for row in reader:
        # 완전히 빈 row는 제외하고 read
        if row and row[0]:
            print(row[0])