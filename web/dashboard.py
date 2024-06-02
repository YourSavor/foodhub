import requests
import streamlit as st
from streamlit_option_menu import option_menu

import establishment
import food
import review

state = st.session_state

def dashboard():
    with st.sidebar:
        # Option menu for navigation
        page = option_menu(
            'YourSavor',
            ['Establishments', 'My Establishments', 'Profile'],
            icons=['building', 'list-task', 'person'],
            menu_icon='house',
            default_index=0,
        )

    if page == 'Establishments':
        establishments()
    elif page == 'My Establishments':
        myEstablishments()
    elif page == 'Profile':
        myProfile()

def establishments():
    if 'page' in state and state.page == 'estab/info':
        establishment.estab_info()
    elif 'page' in state and state.page == 'estab/food/info':
        food.food_info()
    elif 'page' in state and state.page == 'estab/review/add':
        review.review_add_estab()
    elif 'page' in state and state.page == 'food/review/add':
        review.review_add_food()
    else:
        establishment.estab_stream()

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

def myProfile():
    st.title('Profile')
    st.json(state.user)


# CSS for full-width buttons
st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)
