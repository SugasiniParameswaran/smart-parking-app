import streamlit as st

# Initialize page
if "page" not in st.session_state:
    st.session_state.page = "home"

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

if st.button("Login"):
    if role == "Driver":
        st.session_state.page = "driver_login"
    else:
        st.session_state.page = "admin_login"

# Navigation
if st.session_state.page == "driver_login":
    st.switch_page("pages/Driver_Login.py")

elif st.session_state.page == "admin_login":
    st.switch_page("pages/Admin_Login.py")
