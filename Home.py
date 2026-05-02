import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if st.button("Login"):
    if role == "Driver":
        st.success("👉 Go to 'Driver_Login' from the sidebar")
    else:
        st.success("👉 Go to 'Admin_Login' from the sidebar")
