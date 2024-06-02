import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

def review_add_estab():
    estab = state.selected_estab

    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'estab/info'
            st.rerun()

    with col2:
        st.title(f"Add Review {estab['name']}")


def review_add_food():
    estab = state.selected_estab
    food = state.selected_food

    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'estab/food/info'
            st.rerun()

    with col2:
        st.title(f"Add Review {food['name']}")

def review_estab_list():

    st.subheader("Reviews Estab")
    col1, col2 = st.columns([0.25, 10])

    with col2: 
        
        st.text("UNDER CONSTRUCTION")


def review_food_list():

    st.subheader("Reviews Food")
    col1, col2 = st.columns([0.25, 10])

    with col2: 
        
        st.text("UNDER CONSTRUCTION")