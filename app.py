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
        uncounted_count = 0

        for item in subcategory["items"]:
            if item.get("units_per_pack"):
                pack_value = st.session_state.get(f"{item['name']}_packs")
                loose_value = st.session_state.get(f"{item['name']}_loose")

                if pack_value is None or loose_value is None:
                    uncounted_count += 1

            else:
                quantity = st.session_state.get(item['name'])

                if quantity is None:
                    uncounted_count += 1

        if uncounted_count == 0:
            expander_label = f"{subcategory['name']} ✅"
        else:
            expander_label = f"{subcategory['name']} - ⚠️ {uncounted_count} remaining"

        has_started = uncounted_count < len(subcategory["items"])

        with st.expander(
            expander_label,
            expanded=has_started and uncounted_count > 0
        ):
    
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

                    if pack_count is None or loose_count is None:
                        st.caption("⚠️ Not counted")

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
                    st.markdown(f"#### {item['name']}")
                    quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        value=None,
                        step=1,
                        placeholder="0",
                        key=item["name"]
                    )
                    if quantity is None:
                        st.caption("⚠️ Not counted")

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

    with open(file_name, "rb") as file:
        st.download_button(
            label="Download CSV",
            data=file,
            file_name=os.path.basename(file_name),
            mime="text/csv",
        )