import streamlit as st
from menu import menu_with_redirect

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import components.food as fd
import components.establishment as et 

st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

def myEstablishments():
    if 'page' in state and state.page == 'estab/add':
        et.estab_add()
    elif 'page' in state and state.page == 'estab/my/info':
        et.estab_info()
    elif 'page' in state and state.page == 'estab/my/edit':
        et.estab_edit()
    elif 'page' in state and state.page == 'food/add':
        fd.food_add()
    elif 'page' in state and state.page == 'food/edit':
        fd.food_edit()
    elif 'page' in state and state.page == 'estab/my/food':
        fd.food_info()
    else:
        et.myestab_stream()

menu_with_redirect()
myEstablishments()