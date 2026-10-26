import streamlit as st

from inventory import inventory


st.title("Cafe Inventory")

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
                    step=1,
                    key=f"{item['name']}_packs"
                )
                loose_count = st.number_input(
                    f"{item['name']} - Loose",
                    min_value=0,
                    step=1,
                    key=f"{item['name']}_loose"
                )

                total = pack_count * item['units_per_pack'] + loose_count

                st.write(f"Total: {total}")

            else:
                quantity = st.number_input(
                    item["name"],
                    min_value=0,
                    step=1,
                    key=item["name"]
            )