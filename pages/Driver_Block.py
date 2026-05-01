import streamlit as st

st.title("Select Parking Block")

block = st.selectbox(
    "Choose Block",
    ["Block A", "Block B", "Block C", "Block D", "Block E"]
)

if st.button("View Parking"):
    st.session_state.selected_block = block
    st.switch_page("pages/Driver_Dashboard.py")
