import streamlit as st

st.title("Smart Parking System")
st.subheader("Login Screen")

role = st.radio("Login as", ["Driver", "Admin"])

st.write("")  # spacing

# Button-style navigation
if role == "Driver":
    st.markdown("""
        <style>
        .btn {
            display: inline-block;
            padding: 10px 25px;
            font-size: 16px;
            color: white;
            background-color: #4CAF50;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
        }
        </style>
        <a href="/Driver_Login" target="_self" class="btn">Login</a>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .btn {
            display: inline-block;
            padding: 10px 25px;
            font-size: 16px;
            color: white;
            background-color: #4CAF50;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
        }
        </style>
        <a href="/Admin_Login" target="_self" class="btn">Login</a>
    """, unsafe_allow_html=True)
