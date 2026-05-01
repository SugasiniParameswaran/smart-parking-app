import streamlit as st
import sqlite3
from datetime import datetime

st.title("Driver Login")

name = st.text_input("Name")
vehicle = st.text_input("Vehicle Number")
phone = st.text_input("Phone Number")

if st.button("Proceed"):

    if name and vehicle and phone:

        # Get current timestamp
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Connect to database
        conn = sqlite3.connect("parking.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO drivers (name, vehicle_number, phone, login_time)
        VALUES (?, ?, ?, ?)
        """, (name, vehicle, phone, login_time))

        conn.commit()
        conn.close()

        st.success("Login successful ✅")

        st.switch_page("pages/Driver_Block.py")

    else:
        st.error("Please fill all fields.")
