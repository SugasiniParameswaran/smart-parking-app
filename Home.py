import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if st.button("Login"):

    if role == "Driver":
        st.switch_page("Driver_Login")
    else:
        st.switch_page("Admin_Login")
