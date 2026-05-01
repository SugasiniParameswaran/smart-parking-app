import streamlit as st
import sqlite3

st.title("Admin Control Panel")

# ------------------ GET SELECTED BLOCK ------------------

block = st.session_state.get("selected_block")

if not block:
    st.error("No block selected.")
    st.stop()

# ------------------ CONNECT TO DATABASE ------------------

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT total_slots, free_slots, occupied_slots, price_per_hour
    FROM blocks
    WHERE block_name = ?
""", (block,))

data = cursor.fetchone()
conn.close()

if not data:
    st.error("Block data not found in database.")
    st.stop()

total_slots, free_slots, occupied_slots, current_rate = data

# ------------------ CALCULATE OCCUPANCY ------------------

predicted_occupancy = int((occupied_slots / total_slots) * 100)

# ------------------ TIER-BASED PRICING LOGIC ------------------

if predicted_occupancy <= 69:
    optimized_price = 45
    pricing_status = "Decrease"
elif 70 <= predicted_occupancy <= 80:
    optimized_price = 50
    pricing_status = "Base Rate"
else:  # 81–100
    optimized_price = 55
    pricing_status = "Increase"

# ------------------ DISPLAY SECTION ------------------

st.subheader("Parking Summary")
st.write(f"**Parking Block:** {block}")
st.write(f"**Total Slots:** {total_slots}")
st.write(f"**Free Slots:** {free_slots}")
st.write(f"**Occupied Slots:** {occupied_slots}")
st.write(f"**Current Rate per Hour (From DB): ₹{current_rate}**")

st.divider()

st.subheader("Prediction & Pricing")
st.write(f"**Predicted Occupancy:** {predicted_occupancy}%")
st.write("**Pricing Policy:**")
st.write("0–69% → ₹45")
st.write("70–80% → ₹50")
st.write("81–100% → ₹55")

st.write(f"**Optimized Price (Based on Rule): ₹{optimized_price}**")
st.write(f"**Pricing Status:** {pricing_status}")

st.divider()

if st.button("Update"):
    st.session_state.selected_block = block
    st.switch_page("pages/Admin_Update.py")
st.divider()

if st.button("Open ML Analytics"):
    st.switch_page("pages/Admin_ML_Analytics.py")
