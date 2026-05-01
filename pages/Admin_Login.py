import streamlit as st
import sqlite3

st.title("Admin Login")

admin_name = st.text_input("Admin Name")
admin_id = st.text_input("Admin ID")
password = st.text_input("Password", type="password")

if st.button("Login"):

    conn = sqlite3.connect("parking.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM admins 
        WHERE name=? AND admin_id=? AND password=?
    """, (admin_name, admin_id, password))

    result = cursor.fetchone()
    conn.close()

    if result:
        st.session_state.admin_logged_in = True
        st.session_state.admin_name = admin_name
        st.success("Login Successful")
        st.switch_page("pages/Admin_Block.py")   # 👈 MUST GO HERE
    else:
        st.error("Invalid Credentials")

    st.markdown("---")
if st.button("New Admin? Register Here"):
    st.switch_page("pages/Admin_Register.py")
