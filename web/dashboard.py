import requests
import streamlit as st
from streamlit_option_menu import option_menu

import establishment
import food
import review

state = st.session_state


currUser = {
    'id': '33bbf10e-cc0e-4669-8d9f-e06318a9b19d',
    'username': 'test2',
    'hashed_password': '$2b$12$a427s5rVOe7PHCFDWZm6q.HdFKk5Oog8OuDxcZSKTRFJQ68EH/8Ry',
    'first_name': 'test',
    'middle_name': 'test',
    'last_name': 'test',
    'created_at': '2024-06-01 13:22:40.094475+00',
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
    st.json(currUser)


# CSS for full-width buttons
st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
  dashboard()
