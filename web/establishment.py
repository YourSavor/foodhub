import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import food

def refresh_stream(attrib, order):
    response = requests.get(f'{API_URL}/establishments/all/{order}/{attrib}')

    if response.status_code != 200:
        st.error("Error Fetching establishments!")
        return
    
    state.stream = response.json()['establishments']

    if 'selected_estab' not in state:
        return
    
    for establishment in state.stream:
        if establishment['id'] == state.selected_estab['id']:
            state.selected_estab = establishment
            break

def estab_stream():
    st.title('Establishments')
    name = st.text_input('Search:')
    attrib = st.selectbox('Order by:', ['Name', 'Rating'])

    sort_order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed')
    order = 'asc' if sort_order == 'Ascending' else 'desc'

    high_only = st.selectbox('Show:', ['All', 'High Only (Rating >= 4)'])

    st.divider()

    if high_only == 'All':
        refresh_stream(attrib, order)
    else:
        response = requests.get(f"{API_URL}/establishments/high/{order}")

        if response.status_code != 200:
            st.error("Error Fetching establishments!")
        
        state.stream = response.json()['establishments']


    if 'stream' not in state:
        return
    
    for establishment in state.stream:
        with st.container():
            if st.button(establishment['name']):
                state.selected_estab = establishment
                state.page = 'estab/info'
                st.rerun()

def estab_info():

    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'asc')
            state.page = 'stream'
            st.rerun()

    with col2:
        estab = state.selected_estab

        created_at_dt = datetime.strptime(estab['created_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        formatted_created_at = created_at_dt.strftime('%B %d, %Y | %H:%M')

        estab_info = f"""
            **{estab['name']}**
            ---
            - **Location:** {estab['location']}
            - **Rating:** {estab['rating']}
            - **Added:** {formatted_created_at}
            """
        
        if estab['updated_at']:
            updated_at_dt = datetime.strptime(estab['updated_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            formatted_updated_at = updated_at_dt.strftime('%B %d, %Y | %H:%M')
            estab_info = f"{estab_info} - **Updated:** {formatted_updated_at}"

        st.info(estab_info)

        if (state.page == 'estab/my/info'):
            if st.button('Edit', key='edit_button'):
                state.page = 'estab/my/edit'
                st.rerun()

            if st.button('Delete', key='delete_button'):
                response = requests.put(f"{API_URL}/establishments/delete", json={
                    'id': estab['id'],
                })

                if (response.status_code == 200):
                    refresh_stream('name', 'asc')
                    st.toast(f"{estab['name']} deleted!")
                    state.page = 'stream'
                    st.rerun()
                else:
                    st.error(f"Can't delete {estab['name']}!")

        if (state.page == 'estab/info' and state.user['id'] != estab['user_id']):
            if st.button('Add A Review', key='addreview_button'):
                state.page = 'estab/review/add'
                st.rerun()
        else:
            if st.button('Add A Review', key='addreview_button', disabled=True):
                st.toast("You are not allowed to review your own items.")
            
        st.divider()

        food.food_list()
   

def myestab_stream():
    st.title('My Establishments')

    if st.button('Add', key='add_button'):
        state.page = 'estab/add'
        st.rerun()
    
    attrib = st.selectbox('Order by:', ['Name', 'Rating'])
    sort_order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed')
    order = 'asc' if sort_order == 'Ascending' else 'desc'

    st.divider()

    refresh_stream(attrib, order)

    if 'stream' not in state:
        return
    
    for establishment in state.stream:
        if establishment['user_id'] != state.user['id']:
            continue
        with st.container():
            if st.button(establishment['name']):
                state.selected_estab = establishment
                state.page = 'estab/my/info'
                st.rerun()

def estab_edit():
    col1, col2 = st.columns([0.5, 10])
    estab = state.selected_estab

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'asc')
            state.page = 'estab/my/info'
            st.rerun()
    with col2:
        
        st.title(f"Edit {estab['name']}")

        name = st.text_input('New Name:', value=estab['name'])
        location = st.text_input('New Location:', value=estab['location'])

        if st.button('Submit'):
            
            if not (name.strip() and location.strip()):
                st.error('Name and location cannot be empty.')

            response = requests.put(f"{API_URL}/establishments/update", json={
                'id': estab['id'],
                'name': name,
                'location': location,
            })

            if response.status_code == 200:
                refresh_stream('name', 'asc')
                state.page = 'estab/info'
                st.toast(f"{estab['name']} edited!")
                st.rerun()
            else:
                st.error(f"Can't edit {estab['name']}!")


def estab_add():
    
    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'asc')
            state.page = 'stream'
            st.rerun()
            
    with col2:
        st.title('Add Establishment')

        name = st.text_input('Enter Establishment Name:')
        location = st.text_input('Enter Establishment Location:')

        if st.button('Submit'):
            
            if not (name.strip() and location.strip()):
                st.error('Name and location cannot be empty.')
            
            response = requests.post(f"{API_URL}/establishments/insert", json={
                'user_id': state.user['id'],
                'name': name,
                'location': location,
            })

            if (response.status_code == 200):
                st.toast(f"{name} added to establishments!")
            else:
                st.error(f"Can't add {name}!")
        
