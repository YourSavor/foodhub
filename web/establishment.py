import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
state = st.session_state

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
        
