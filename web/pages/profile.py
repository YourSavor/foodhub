import streamlit as st
from menu import menu_with_redirect

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import components.profile as pf

st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

def profile():
    pf.profile_info()

menu_with_redirect()
profile()


