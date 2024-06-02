import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

def refresh_stream(order_by, sort_order):
    order = 'asc' if sort_order == 'Ascending' else 'desc'
    response = requests.get(f'{API_URL}/establishments/all/{order}/{order_by}')

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
    order_by = st.selectbox('Order by:', ['Name', 'Rating'])
    sort_order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed')
    
    st.divider()

    refresh_stream(order_by, sort_order)

    if 'stream' not in state:
        return
    
    for establishment in state.stream:
        with st.container():
            if st.button(establishment['name']):
                state.selected_estab = establishment
                state.page = 'estab_info'
                st.rerun()

def estab_info():
    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'Ascending')
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

        if (estab['user_id'] == state.user['id'] and state.page):
            if st.button('Edit', key='edit_button'):
                state.page = 'estab_edit'
                st.rerun()

            if st.button('Delete', key='delete_button'):
                response = requests.put(f'{API_URL}/establishments/delete', json={
                    'id': estab['id'],
                })

                if (response.status_code == 200):
                    refresh_stream('name', 'Ascending')
                    state.page = 'stream'
                    st.rerun()
                else:
                    st.error(f"Can't delete {estab['name']}!")

            
        st.divider()
   

def myestab_stream():
    st.title('My Establishments')

    if st.button('Add', key='add_button'):
        state.page = 'estab_add'
        st.rerun()
    
    order_by = st.selectbox('Order by:', ['Name', 'Rating'])
    sort_order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed')
  
    st.divider()

    refresh_stream(order_by, sort_order)

    if 'stream' not in state:
        return
    
    for establishment in state.stream:
        if establishment['user_id'] != state.user['id']:
            continue
        with st.container():
            if st.button(establishment['name']):
                state.selected_estab = establishment
                state.page = 'estab_info'
                st.rerun()

def estab_edit():
    col1, col2 = st.columns([0.5, 10])
    estab = state.selected_estab

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'Ascending')
            state.page = 'estab_info'
            st.rerun()
    with col2:
        
        st.title(f"Update {estab['name']}")

    name = st.text_input('New Name:', value=estab['name'])
    location = st.text_input('New Location:', value=estab['location'])

    if st.button('Submit'):
        
        if not (name.strip() and location.strip()):
            st.error('Name and location cannot be empty.')

        response = requests.put(f'{API_URL}/establishments/update', json={
            'id': estab['id'],
            'name': name,
            'location': location,
        })

        if response.status_code == 200:
            refresh_stream('name', 'Ascending')
            state.page = 'estab_info'
            st.rerun()
        else:
            st.error(f"Can't edit {estab['name']}!")


def estab_add():
    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            refresh_stream('name', 'Ascending')
            state.page = 'stream'
            st.rerun()
            
    with col2:
        st.title('Add Establishment')

    name = st.text_input('Enter Establishment Name:')
    location = st.text_input('Enter Establishment Location:')

    if st.button('Submit'):
        
        if not (name.strip() and location.strip()):
            st.error('Name and location cannot be empty.')
          
        response = requests.post(f'{API_URL}/establishments/insert', json={
            'user_id': state.user['id'],
            'name': name,
            'location': location,
        })

        if (response.status_code == 200):
            st.success(f'{name} added to establishments!')
        else:
            st.error(f"Can't add {name}!")

        st.clear()
        
