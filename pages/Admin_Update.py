import streamlit as st
import sqlite3

st.title("Admin Slot Update Panel")

block = st.session_state.get("selected_block")

if not block:
    st.error("No block selected.")
    st.stop()

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("""
SELECT slot_number, status
FROM slots
WHERE block_name = ?
ORDER BY slot_number
""", (block,))

rows = cursor.fetchall()

if not rows:
    st.error("No slot data found.")
    conn.close()
    st.stop()

slot_status = {row[0]: row[1] for row in rows}

st.subheader(f"Update Slot Status – {block}")

left_col, middle, right_col = st.columns([2,1,2])

updated_slots = {}

with left_col:
    st.markdown("### Left Side")
    for i in range(1, 11):
        checked = True if slot_status[i] == "O" else False
        value = st.checkbox(
            f"Slot {i}",
            value=checked,
            key=f"{block}_slot_{i}"
        )
        updated_slots[i] = "O" if value else "F"

with right_col:
    st.markdown("### Right Side")
    for i in range(11, 21):
        checked = True if slot_status[i] == "O" else False
        value = st.checkbox(
            f"Slot {i}",
            value=checked,
            key=f"{block}_slot_{i}"
        )
        updated_slots[i] = "O" if value else "F"

st.divider()

if st.button("Save Changes"):

    # 1️⃣ Update each slot
    for slot_number, status in updated_slots.items():
        cursor.execute("""
        UPDATE slots
        SET status = ?
        WHERE block_name = ? AND slot_number = ?
        """, (status, block, slot_number))

    # 2️⃣ Recalculate free & occupied
    free_slots = list(updated_slots.values()).count("F")
    occupied_slots = list(updated_slots.values()).count("O")
    total_slots = free_slots + occupied_slots

    # 3️⃣ Calculate occupancy percentage
    predicted_occupancy = int((occupied_slots / total_slots) * 100)

    # 4️⃣ Tier-Based Pricing Logic
    if predicted_occupancy < 70:
        new_rate = 45
    elif 70 <= predicted_occupancy <= 80:
        new_rate = 50
    else:
        new_rate = 55

    # 5️⃣ Update blocks table
    cursor.execute("""
    UPDATE blocks
    SET free_slots = ?, occupied_slots = ?, price_per_hour = ?
    WHERE block_name = ?
    """, (free_slots, occupied_slots, new_rate, block))

    conn.commit()
    conn.close()

    st.success("Slots and pricing updated successfully ✅")

st.markdown("""
    <a href="/" target="_self">
        <button style="
            padding:10px 20px;
            background-color:#4CAF50;
            color:white;
            border:none;
            border-radius:8px;
            cursor:pointer;">
            🔙 Back to Home
        </button>
    </a>
""", unsafe_allow_html=True)
