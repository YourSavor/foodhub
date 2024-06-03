import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state


def refresh_profile():
    response = requests.get(f"{API_URL}/users/id/{state.user['id']}")

    if (response.status_code != 200):
        st.error("Failed to fetch user info.")
        return
    
    state.user = response.json()

def profile_info():
    refresh_profile()

    user = state.user

    full_name = f"{user['first_name']} {user['middle_name']} {user['last_name']}"
    created_at_dt = datetime.strptime(user['created_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
    formatted_created_at = created_at_dt.strftime('%B %d, %Y | %H:%M')


    profile_info = f"""
        **{full_name}**
        ---
        - **Username:** {user['username']}
        - **Joined:** {formatted_created_at}
        """
    
    st.info(profile_info)

    if (('show_edit_profile' not in state) or 
        ('show_edit_profile' in state and not state.show_edit_profile)):
        if (st.button('Edit Profile', key=f"editprofile_{user['id']}")):
            state.show_edit_profile = True
            st.rerun()

    if ('show_edit_profile' in state and state.show_edit_profile):
        edit_section()

    st.divider()

    if (st.button('Delete My Account', key=f"deleteprofile_{user['id']}")):
        response = requests.delete(f"{API_URL}/users/delete", json={"user_id": user['id']})

        if response.status_code == 200:
            st.success("Your account and all associated data have been deleted.")

def edit_section():
    user = state.user

    new_username = st.text_input('New Username:', value=f"{user['username']}", disabled=True)
    
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        new_first = st.text_input('First Name:', value=f"{user['first_name']}")
    with col2:
        new_middle = st.text_input('Middle Name:', value=f"{user['middle_name']}")
    with col3:
        new_last = st.text_input('Last Name:', value=f"{user['last_name']}")


    new_password = None    
    if (st.toggle('Update Password')):
        new_password = st.text_input("New Password", type="password")

    if (st.button('Confirm Changes', key=f"confirmeditprofile_{user['id']}")):
        update_account(new_username, new_first, new_middle, new_last, new_password)

      

    if (st.button('Cancel', key=f"canceleditprofile_{user['id']}")):
        state.show_edit_profile = False
        st.rerun()

def update_account(new_username, new_first, new_middle, new_last, new_password):
    user = state.user

    if not (new_username.strip() and new_first.strip() 
        and new_middle.strip() and new_last.strip()):
        st.error("Please fill all fields!")
        return

    if (new_password != None and not(new_password.strip())):
        st.error("Password can't be empty!")
        return
    
    if (new_password == None):
        new_password = ''
    
    response = requests.put(f"{API_URL}/users", json={
        'user_id': user['id'],
        'username': new_username,
        'first_name': new_first,
        'middle_name': new_middle,
        'last_name': new_last,
        'password': new_password
    })

    if (response.status_code == 200):
        st.toast('Success!')
        refresh_profile()
        state.show_edit_profile = False
        st.rerun()
    else:
        st.error("Failed updating your account.")

