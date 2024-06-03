import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import components.food as fd
import components.review as rw

def filters():
    col1, col2, col3 = st.columns(3)

    with col1:
        attrib = st.selectbox('Order by:', ['Name', 'Rating'])
    with col2:  
        sort_order = st.selectbox(' ', ['Ascending', 'Descending'])
        order = 'asc' if sort_order == 'Ascending' else 'desc'
    with col3:
        high_only = st.selectbox('Show:', ['All', 'High Only (Rating >= 4)'])

    st.divider()

    if high_only == 'All':
        refresh_stream(attrib, order)
    else:
        response = requests.get(f"{API_URL}/establishments/high/{order}")

        if response.status_code != 200:
            st.error("Error Fetching establishments!")
        
        state.stream = response.json()['establishments']

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

    if name.strip():
        response = requests.get(f"{API_URL}/establishments/search/{name}")

        if response.status_code == 200:
            state.stream = response.json().get('establishments') 
        else: 
            st.error(response.json().get('detail'))
    else:
        filters()

    if 'stream' not in state:
        return
    
   

    for establishment in st.session_state['stream']:

        estab = f"""    
            <h3> {establishment['name']} </h3>
            <div style="line-height: 1.2; margin-bottom: 0px;">
                <strong>Rating:</strong> {establishment['rating']}<br>
                <strong>Location:</strong> {establishment['location']}
            </div>
        """

        st.markdown(
            """
            <style>
            button[kind="primary"] {
                background: none!important;
                border: none;
                padding: 0!important;
                color: black !important;
                text-decoration: none;
                cursor: pointer;
                border: none !important;
                font-style: italic;
                text-align: left;
            }
            button[kind="primary"]:hover {
                text-decoration: none;
                color: black !important;
            }
            button[kind="primary"]:focus {
                outline: none !important;
                box-shadow: none !important;
                color: black !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
 
        st.markdown(estab, unsafe_allow_html=True)

        st.markdown("""
            <style>
                div.stButton > button {
                    width: auto !important;
                    padding: 0px;
                    margin: 0 px;
                }
            </style>
        """, unsafe_allow_html=True)

        if st.button("See more", key=f"estab_{establishment['id']}", type="primary"):
            st.session_state['selected_estab'] = establishment
            st.session_state['page'] = 'estab/info'
            st.rerun()


def clicked_estab(establishment):
    state.selected_estab = establishment
    state.page = 'estab/info'
    st.rerun()

def estab_info():

    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
        cursor: pointer;
        border: none !important;
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: black !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button('←', help="Go Back", type="primary"):
        refresh_stream('name', 'asc')
        state.page = 'stream'
        st.rerun()

    estab = state.selected_estab

    created_at_dt = datetime.strptime(estab['created_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
    formatted_created_at = created_at_dt.strftime('%B %d, %Y | %H:%M')

    estab_info = f"""
        **{estab['name']}**
        ---
        <div style="line-height: 1.2; margin-bottom: 30px;">
            <strong>Location:</strong> {estab['location']}<br>
            <strong>Rating:</strong> {estab['rating']}<br>
            <strong>Added:</strong> {formatted_created_at}
        </div>
        """

    if estab['updated_at']:
        updated_at_dt = datetime.strptime(estab['updated_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        formatted_updated_at = updated_at_dt.strftime('%B %d, %Y | %H:%M')
        estab_info = f"{estab_info} - **Updated:** {formatted_updated_at}"

    st.markdown(estab_info, unsafe_allow_html=True)

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

    fd.food_list()

    st.divider()


    rw.review_estab_list()
        
   

def myestab_stream():
    st.title('My Establishments')

    if st.button('Add', key='add_button'):
        state.page = 'estab/add'
        st.rerun()
    
    col1, col2 = st.columns(2)

    with col1:
        attrib = st.selectbox('Order by:', ['Name', 'Rating'])
    with col2:  
        sort_order = st.selectbox(' ', ['Ascending', 'Descending'])
        order = 'asc' if sort_order == 'Ascending' else 'desc'

    st.divider()

    refresh_stream(attrib, order)

    if 'stream' not in state:
        return
    
    for establishment in state.stream:
        if establishment['user_id'] != state.user['id']:
            continue
        with st.container():
            if st.button(establishment['name'], key=f"myestab_{establishment['id']}"):
                state.selected_estab = establishment
                state.page = 'estab/my/info'
                st.rerun()

def estab_edit():
    estab = state.selected_estab

    st.markdown(
    """
    <style>
    button[kind="primary"] {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
    }
    button[kind="primary"]:hover {
        text-decoration: none;
        color: black !important;
    }
    button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    if st.button('←', help="Go Back", type="primary"):
        refresh_stream('name', 'asc')
        state.page = 'estab/my/info'
        st.rerun()

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
    
    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
            cursor: pointer;
            border: none !important;
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: black !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button('←', help="Go Back", type="primary"):
        refresh_stream('name', 'asc')
        state.page = 'stream'
        st.rerun()
        
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
        
