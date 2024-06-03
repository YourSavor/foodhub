import requests
import streamlit as st
from datetime import datetime

from menu import menu_with_redirect

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

import components.food as fd
import components.review as rw
import components.establishment as et 

def establishments():
    if 'page' in state and state.page == 'estab/info':
        et.estab_info()
    elif 'page' in state and state.page == 'estab/food/info':
        fd.food_info()
    elif 'page' in state and state.page == 'estab/review/add':
        rw.review_add_estab()
    elif 'page' in state and state.page == 'food/review/add':
        rw.review_add_food()
    else:
        et.estab_stream()

      
menu_with_redirect()
establishments()