import requests
import streamlit as st
from streamlit_option_menu import option_menu

import establishment


state = st.session_state

currUser = {
    "id": "712a5ddd-94eb-484f-b3bd-cb4bfa97ab1c",
    "username": "test",
    "hashed_password": "$2b$12$cQ0Yjj0jaPqfN1aphQmnueO7L8uYr9tEyf68RfczIqq4jJlaTr/o6",
    "first_name": "test",
    "middle_name": "test",
    "last_name": "test",
    "created_at": "2024-06-01T06:46:24.341906+00:00",
    "updated_at": None,
    "is_deleted": False
}

state.user = currUser


def dashboard():
    st.set_page_config(
            page_title="YourSavor", 
            layout="wide", 
            initial_sidebar_state="auto"
        )

    with st.sidebar:
        # Option menu for navigation
        page = option_menu(
            "YourSavor",
            ["Establishments", "My Establishments", "Profile"],
            icons=["building", "list-task", "person"],
            menu_icon="house",
            default_index=0,
        )

    if page == "Establishments":
        establishments()
    elif page == "My Establishments":
        myEstablishments()
    elif page == "Profile":
        myProfile()

def establishments():
    st.title("Establishments")

def myEstablishments():
    if 'page' in state and state.page == 'add_estab':
        establishment.add_establishment()
    else:
        establishment.myestab_stream()

def myProfile():
    st.title("Profile")
    st.json(currUser)

dashboard()
