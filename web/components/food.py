import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import components.review as rw

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
    estab = state.selected_estab

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

        max_price = 0.00

        if len(state.foodstream) != 0:
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
        if (estab['user_id'] == state.user['id'] and state.page == 'estab/my/info'):
            if st.button('Add an Item', key='add_button'):
                state.page = 'food/add'
                st.rerun()

        name = st.text_input('Search Food:')

        if name.strip():
            response = requests.get(f"{API_URL}/foods/all/search/{name}")

            if response.status_code != 200:
                st.error("Error Fetching foods!")
            
            state.foodstream = response.json()['foods']
        else:
            filters()

    

        if 'foodstream' not in state:
            return
        
        for food in state.foodstream:
            with st.container():
                food_label = f"{food['name']} | (P {food['price']:.2f})"
                if st.button(food_label):
                    state.selected_food = food
                    
                    if (state.page == 'estab/my/info'):
                        state.page = 'estab/my/food'
                    else:
                        state.page = 'estab/food/info'
                    
                    st.rerun()

    
def food_info():
    col1, col2 = st.columns([0.5, 10])
    food = state.selected_food
    estab = state.selected_estab

    created_at_dt = datetime.strptime(food['created_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
    formatted_created_at = created_at_dt.strftime('%B %d, %Y | %H:%M')

    food_info = f"""
        **{food['name']}**
        ---
        - **Type:** {food['type']}
        - **Price:** {food['price']}
        - **Rating:** {food['rating']}
        - **Added:** {formatted_created_at}
        """
    
    if food['updated_at']:
        updated_at_dt = datetime.strptime(food['updated_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        formatted_updated_at = updated_at_dt.strftime('%B %d, %Y | %H:%M')
        estab_info = f"{estab_info} - **Updated:** {formatted_updated_at}"
    

    with col1:
        if st.button('←', help="Go Back"):
            refresh_foodstream('name', 'asc')
            if state.page == 'estab/my/food':
                state.page = 'estab/my/info'
            else:
                state.page = 'estab/info'
            
            st.rerun()
    with col2:
        food = state.selected_food
        st.info(food_info)

        if state.page == 'estab/my/food':
            if st.button('Edit', key='edit_button'):
                state.page = 'food/edit'
                st.rerun()

            if st.button('Delete', key='delete_button'):
                response = requests.put(f"{API_URL}/foods/delete/{food['id']}")

                if (response.status_code == 200):
                    refresh_foodstream('name', 'asc')
                    st.toast(f"{food['name']} deleted!")
                    state.page = 'estab/my/info'
                    st.rerun()
                else:
                    st.error(f"Can't delete {food['name']}!")

        if (state.page == 'estab/food/info' and state.user['id'] != estab['user_id']):
            if st.button('Add A Review', key='addreview_button'):
                state.page = 'food/review/add'
                st.rerun()
        else:
            if st.button('Add A Review', key='addreview_button', disabled=True):
                st.toast("You are not allowed to review your own items.")

        st.divider()

        rw.review_food_list()

def food_edit():
    col1, col2 = st.columns([0.5, 10])
    food = state.selected_food

    with col1:
        if st.button('←', help="Go Back"):
            refresh_foodstream('name', 'asc')
            state.page = 'estab/my/food'
            st.rerun()
            
    with col2:
        st.title(f"Edit {food['name']}")

        name = st.text_input('Food Name:', value = food['name'])

        if (food['type'] in ('Meat', 'Vegetable')):
            type = st.selectbox('Food Type:', ['Meat', 'Vegetable', 'Others'], index = ['Meat', 'Vegetable'].index(food['type']))
        else:
            type = st.selectbox('Food Type:', ['Meat', 'Vegetable', 'Others'], value = 'Others')

        if (type == 'Others'):
            others_type = st.text_input('Food Type:', value = food['type'])

            if others_type.strip():
                type = others_type

        price = st.number_input('Price:', min_value=0.00, format="%.2f", value = food['price'])

        if st.button('Submit'):
            
            if not (name.strip() and type.strip() and price > 0):
                st.error('Please fill all fields.')
                return
            
            response = requests.put(f"{API_URL}/foods", json={
                'id': food['id'],
                'name': name,
                'type': type,
                'price': price,
            })

            if (response.status_code == 200):
                refresh_foodstream('name', 'asc')
                st.toast(f"{name} edited!")
                state.page = 'estab/my/food'
                st.rerun()
            else:
                st.error(f"Can't edit {name}!")


def food_add():
    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'estab/my/info'
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