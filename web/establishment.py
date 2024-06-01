import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
state = st.session_state

import requests
import streamlit as st

state = st.session_state 

def estab_stream():
    search = st.text_input("Search Establishment Name:")

    order_by = st.selectbox("Order by:", ["Name", "Rating"])
    sort_order = st.selectbox("Order", ["Ascending", "Descending"], label_visibility="collapsed")

    order = "asc" if sort_order == "Ascending" else "desc"

    response = requests.get(f"{API_URL}/establishments/all/{order}/{order_by}")

    if response.status_code == 200:
        estab_stream_data = response.json()['establishments']
        for establishment in estab_stream_data:
            st.write(establishment['name'])
    else:
        st.error(f"Failed to fetch establishments. Status code: {response.status_code}")


def myestab_stream():
    st.title("EstabStream Page")
    st.write("This is the content of the EstabStream page.")

    if st.button("Add", key="add_button"):
        state.page = 'add_estab'
        st.rerun()

def add_establishment():
    st.title("Add Establishment")
    
    name = st.text_input("Enter Establishment Name:")
    location = st.text_input("Enter Establishment Location:")

    if st.button("Submit"):
        
        if not (name.strip() and location.strip()):
            st.error("Name and location cannot be empty.")

            if st.button("Go Back"):
                state.page = 'stream'
                st.rerun()
            return
        
        response = requests.post(f"{API_URL}/establishments/insert", json={
            "user_id": state.user["id"],
            "name": name,
            "location": location,
        })

        st.success(f"{name} added to establishments!")


    if st.button("Go Back"):
        state.page = 'stream'
        st.rerun()
        
