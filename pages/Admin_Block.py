import streamlit as st

# If not logged in, stop
if "admin_logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

st.title("Admin Block Selection")

block = st.selectbox(
    "Select Parking Block",
    ["Block A", "Block B", "Block C", "Block D", "Block E"]
)

if st.button("Go to Control Panel"):
    st.session_state.selected_block = block
    st.switch_page("pages/Admin_Control.py")
