import csv
import os
from datetime import datetime

import streamlit as st
from inventory import inventory


st.title("Cafe Inventory")

results = []










# Render inventory by category and subcategory
for category in inventory["categories"]:
    st.header(category["name"])
    for subcategory in category["subcategories"]:
        
# Calculate the number of items that have not been counted yet
        uncounted_count = 0

# Render the appropriate input fields for each counting type
        for item in subcategory["items"]:
            if item.get("units_per_pack"):
                pack_value = st.session_state.get(f"{item['name']}_packs")
                loose_value = st.session_state.get(f"{item['name']}_loose")

                if pack_value is None or loose_value is None:
                    uncounted_count += 1

            elif item.get("counting_type") == 'partial':
                full_value = st.session_state.get(f"{item['name']}_full")

                if full_value is None:
                    uncounted_count += 1

            else:
                quantity = st.session_state.get(item['name'])

                if quantity is None:
                    uncounted_count += 1
                    
# Show counting progress in the subcategory header
        if uncounted_count == 0:
            expander_label = f"{subcategory['name']} ✅"
        else:
            expander_label = f"{subcategory['name']} - ⚠️ {uncounted_count} remaining"

        has_started = uncounted_count < len(subcategory["items"])

# Keep an in-progress subcategory open while counting
        with st.expander(
            expander_label,
            expanded=has_started and uncounted_count > 0
        ):
    
            if subcategory["counting_instruction"]:
                st.caption(subcategory["counting_instruction"])

            for item in subcategory["items"]:
# Count full packs and loose units
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

# Count full units with an optional partial amount
                elif item.get("counting_type") == "partial":
                    st.markdown(f"#### {item['name']}")

                    full_count = st.number_input(
                        "Full",
                        min_value=0,
                        value=None,
                        step=1,
                        placeholder="0",
                        key=f"{item['name']}_full"
                    )

                    partial = st.selectbox(
                        "Open",
                        options=[None, 25, 50, 75],
                        format_func=lambda value: (
                            "Not selected"
                            if value is None
                            else f"{value}%"
                        ),
                        key=f"{item['name']}_partial"
                    )

                    if full_count is None:
                        st.caption("⚠️ Not counted")

                    total = (full_count or 0) + ((partial or 0) / 100)

                    st.markdown(
                        f"<p style='text-align: right;'>Total: {total}</p>",
                        unsafe_allow_html=True
                    )

                    results.append({
                        "category": category["name"],
                        "subcategory": subcategory["name"],
                        "item": item["name"],
                        "pack_count": full_count,
                        "loose_count": '' if partial is None else partial / 100,
                        "total_quantity": total,
                    })

# Count simple quantities
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
            


# Save the current stock count and provide a CSV download
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