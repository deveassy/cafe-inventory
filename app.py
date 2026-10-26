import csv
import os
from datetime import datetime

import streamlit as st
from inventory import inventory


st.title("Cafe Inventory")

results = []

# list
for category in inventory["categories"]:
    st.header(category["name"])

    for subcategory in category["subcategories"]:
        st.subheader(subcategory["name"])

        if subcategory["counting_instruction"]:
            st.caption(subcategory["counting_instruction"])

        for item in subcategory["items"]:
            if item.get("units_per_pack"):
                pack_count = st.number_input(
                    f"{item['name']} - Packs",
                    min_value=0,
                    value=None,
                    step=1,
                    placeholder="0",
                    key=f"{item['name']}_packs"
                )
                loose_count = st.number_input(
                    f"{item['name']} - Loose",
                    min_value=0,
                    value=None,
                    step=1,
                    placeholder="0",
                    key=f"{item['name']}_loose"
                )

                total = (pack_count or 0) * item['units_per_pack'] + (loose_count or 0)

                st.write(f"Total: {total}")

                results.append({
                    "category": category["name"],
                    "subcategory": subcategory["name"],
                    "item": item["name"],
                    "pack_count": pack_count,
                    "loose_count": loose_count,
                    "total_quantity": total,
                })

            else:
                quantity = st.number_input(
                    item["name"],
                    min_value=0,
                    value=None,
                    step=1,
                    placeholder="0",
                    key=item["name"]
                )

                results.append({
                    "category": category["name"],
                    "subcategory": subcategory["name"],
                    "item": item["name"],
                    "pack_count": "",
                    "loose_count": '',
                    "total_quantity": quantity,
                })

# save button 
if st.button("Save Stock Count"):
    os.makedirs("stock_counts", exist_ok=True)

    file_name = f"stock_counts/{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "category",
            "subcategory",
            "item",
            "pack_count",
            "loose_count",
            "total_quantity",
        ]

        # create csv file
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    st.success(f"Stock count saved: {file_name}")