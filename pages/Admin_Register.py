import streamlit as st
import sqlite3

st.title("Admin Registration")

name = st.text_input("Admin Name")
admin_id = st.text_input("Admin ID")
password = st.text_input("Password", type="password")

if st.button("Register"):

    if name and admin_id and password:

        conn = sqlite3.connect("parking.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO admins (name, admin_id, password)
            VALUES (?, ?, ?)
            """, (name, admin_id, password))

            conn.commit()
            conn.close()

            st.success("Admin Registered Successfully ✅")

        except sqlite3.IntegrityError:
            st.error("Admin ID already exists ❌")
            conn.close()

    else:
        st.error("Please fill all fields.")
