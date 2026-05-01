import streamlit as st
import sqlite3

# -------------------- GET SELECTED BLOCK --------------------

block = st.session_state.get("selected_block")

if not block:
    st.error("No block selected.")
    st.stop()

# -------------------- DESIGN STYLING --------------------

st.markdown("""
<style>
.slot {
    padding: 12px;
    margin: 6px;
    text-align: center;
    font-weight: bold;
    border-radius: 6px;
    color: white;
    width: 50px;
}
.free { background-color: green; }
.occupied { background-color: red; }
.legend {
    display: inline-block;
    padding: 6px 10px;
    margin-right: 10px;
    color: white;
    border-radius: 5px;
    font-weight: bold;
}
.entry {
    text-align: center;
    font-weight: bold;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------- FETCH SLOT DATA FROM DATABASE --------------------

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("""
SELECT slot_number, status
FROM slots
WHERE block_name = ?
ORDER BY slot_number
""", (block,))

rows = cursor.fetchall()

cursor.execute("""
SELECT price_per_hour
FROM blocks
WHERE block_name = ?
""", (block,))

price_data = cursor.fetchone()

conn.close()

if not rows or not price_data:
    st.error("Block data not found.")
    st.stop()

# Convert to dictionary
slot_status = {row[0]: row[1] for row in rows}

price = price_data[0]

# -------------------- CALCULATIONS --------------------

all_slots = list(slot_status.values())
free_count = all_slots.count("F")
occupied_count = all_slots.count("O")
total_slots = len(all_slots)
predicted_occupancy = int((occupied_count / total_slots) * 100)

# -------------------- DASHBOARD DISPLAY --------------------

st.title("Driver Dashboard")
st.write(f"**Parking Block:** {block}")
st.write(f"**Free Slots:** {free_count}")
st.write(f"**Occupied Slots:** {occupied_count}")
st.write(f"**Predicted Occupancy:** {predicted_occupancy}%")
st.write(f"**Current Rate per Hour:** ₹{price}")

st.markdown("""
<div class="legend free">F</div>
<div class="legend occupied">O</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("<div class='entry'>⬅ ENTRY ➡</div>", unsafe_allow_html=True)

left, lane, right = st.columns([3,1,3])

# LEFT SIDE (1–10)
with left:
    for i in range(1, 11):
        cls = "free" if slot_status[i] == "F" else "occupied"
        st.markdown(
            f"<div class='slot {cls}'>{i}</div>",
            unsafe_allow_html=True
        )

# RIGHT SIDE (11–20)
with right:
    for i in range(11, 21):
        cls = "free" if slot_status[i] == "F" else "occupied"
        st.markdown(
            f"<div class='slot {cls}'>{i}</div>",
            unsafe_allow_html=True
        )
