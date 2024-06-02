import requests
import streamlit as st
from streamlit_option_menu import option_menu

import establishment
import food

state = st.session_state


currUser = {
    'id': '712a5ddd-94eb-484f-b3bd-cb4bfa97ab1c',
    'username': 'test',
    'hashed_password': '$2b$12$cQ0Yjj0jaPqfN1aphQmnueO7L8uYr9tEyf68RfczIqq4jJlaTr/o6',
    'first_name': 'test',
    'middle_name': 'test',
    'last_name': 'test',
    'created_at': '2024-06-01T06:46:24.341906+00:00',
    'updated_at': None,
    'is_deleted': False
}

state.user = currUser

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
    elif 'page' in state and state.page == 'food/info':
        food.food_info()
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
    st.json(currUser)


st.set_page_config(
    page_title='YourSavor', 
    layout='wide', 
    initial_sidebar_state='auto'
)

# CSS for full-width buttons
st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

dashboard()
