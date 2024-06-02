import streamlit as st
from menu import menu_with_redirect

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import establishment
import food

def myEstablishments():
    if 'page' in state and state.page == 'estab/add':
        establishment.estab_add()
    elif 'page' in state and state.page == 'estab/my/info':
        establishment.estab_info()
    elif 'page' in state and state.page == 'estab/my/edit':
        establishment.estab_edit()
    elif 'page' in state and state.page == 'food/add':
        food.food_add()
    elif 'page' in state and state.page == 'food/edit':
        food.food_edit()
    elif 'page' in state and state.page == 'estab/my/food':
        food.food_info()
    else:
        establishment.myestab_stream()

menu_with_redirect()
myEstablishments()