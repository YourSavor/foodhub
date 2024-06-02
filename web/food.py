import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

def refresh_foodstream(attrib, order):
    estab = state.selected_estab

    response = requests.get(f"{API_URL}/foods/all/{estab['id']}/{attrib}/{order}")

    if response.status_code != 200:
        st.error("Error Fetching foods!")
        return
    
    state.foodstream = response.json()['foods']

    if 'selected_food' not in state:
        return
    
    for food in state.foodstream:
        if food['id'] == state.selected_food['id']:
            state.selected_food = food
            break

def filters():
    attrib = st.selectbox('Order by:', ['Name', 'Price', 'Rating'])

    sort_order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed')
    order = 'asc' if sort_order == 'Ascending' else 'desc'

    refresh_foodstream(attrib, order)

    type_filter = st.selectbox('Show:', ['All', 'Meat', 'Vegetable', 'Others'])
    if (type_filter == 'Others'):
        others_type = st.text_input('Food Type:')

        if others_type.strip():
            type_filter = others_type
        else:
            type_filter = 'All'

    filter_price = st.toggle("Price Filter", value = False)

    if (type_filter != 'All') and not filter_price:
        response = requests.get(f"{API_URL}/foods/all/{estab['id']}/{type_filter}/{attrib}/{order}")

        if response.status_code != 200:
            st.error("Error Fetching foods!")
        
        state.foodstream = response.json()['foods']
    elif (type_filter == 'All') and filter_price:
        max_price = max(food['price'] for food in state.foodstream)
        low_price = st.number_input('Min:', min_value=0.00, format="%.2f")
        high_price = st.number_input('Max:', min_value=0.00, value=max_price, format="%.2f")

        response = requests.get(f"{API_URL}/foods/all/{estab['id']}/{low_price}/{high_price}/{attrib}/{order}")

        if response.status_code != 200:
            st.error("Error Fetching foods!")
        
        state.foodstream = response.json()['foods']

    elif (type_filter != 'All') and filter_price:
        max_price = max(food['price'] for food in state.foodstream)
        low_price = st.number_input('Min:', min_value=0.00, format="%.2f")
        high_price = st.number_input('Max:', min_value=0.00, value=max_price, format="%.2f")

        response = requests.get(f"{API_URL}/foods/all/{estab['id']}/{type_filter}/{low_price}/{high_price}/{attrib}/{order}")

        if response.status_code != 200:
            st.error("Error Fetching foods!")
        
        state.foodstream = response.json()['foods']

def food_list():
    estab = state.selected_estab

    st.subheader("Menu")

    col1, col2 = st.columns([0.25, 10])


    with col2:
        if (estab['user_id'] == state.user['id'] and state.page == 'myestab_info'):
            if st.button('Add an Item', key='add_button'):
                state.page = 'food_add'
                st.rerun()

        name = st.text_input('Search Food:')

        if name.strip():
            response = requests.get(f"{API_URL}/foods/all/search/{name}")

            if response.status_code != 200:
                st.error("Error Fetching foods!")
            
            state.foodstream = response.json()['foods']
        else:
            filters()

        st.divider()

        if 'foodstream' not in state:
            return
        
        for food in state.foodstream:
            with st.container():
                food_label = f"{food['name']} | (P {food['price']:.2f})"
                if st.button(food_label):
                    state.selected_food = food
                    state.page = 'food_info'
                    st.rerun()

    
def food_info():
    col1, col2 = st.columns([0.5, 10])
    estab = state.selected_estab

    with col1:
        if st.button('←', help="Go Back"):
            refresh_foodstream('name', 'asc')
            state.page = 'estab_info'
            st.rerun()
    with col2:
        food = state.selected_food
        st.title(f"Info page {food['name']}")


def food_add():
    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'myestab_info'
            st.rerun()
            
    with col2:
        st.title('Add Food')

        name = st.text_input('Food Name:')
        type = st.selectbox('Food Type:', ['Meat', 'Vegetable', 'Others'])

        if (type == 'Others'):
            others_type = st.text_input('Food Type:')

            if others_type.strip():
                type = others_type

        price = st.number_input('Price:', min_value=0.00, format="%.2f")

        if st.button('Submit'):
            
            if not (name.strip() and type.strip() and price > 0):
                st.error('Please fill all fields.')
            
            response = requests.post(f"{API_URL}/foods", json={
                'establishment_id': state.selected_estab['id'],
                'name': name,
                'type': type,
                'price': price
            })

            if (response.status_code == 200):
                st.toast(f"{name} added!")
            else:
                st.error(f"Can't add {name}!")


