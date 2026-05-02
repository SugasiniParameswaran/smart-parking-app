import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if role == "Driver":
    st.page_link("pages/1_Driver_Login.py", label="Login as Driver")

else:
    st.page_link("pages/Admin_Login.py", label="Login as Admin")
