import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if st.button("Login"):
    if role == "Driver":
        st.switch_page("1_Driver_Login")
    else:
        st.success("👉 Go to 'Admin_Login' from the sidebar")
