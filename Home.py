import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if st.button("Login"):
    if role == "Driver":
        st.write("👉 Go to Driver Login from sidebar")
    else:
        st.write("👉 Go to Admin Login from sidebar")
