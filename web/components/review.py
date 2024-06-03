import requests
import streamlit as st
from datetime import datetime

API_URL = 'http://127.0.0.1:8000'
state = st.session_state

import components.establishment as et 

def review_add_estab():
    estab = state.selected_estab

    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'estab/info'
            st.rerun()

    with col2:
        st.title(f"Add Review for {estab['name']}")
        
        rating = st.slider("Rating", 1, 5)
        description = st.text_area("Description")

        if st.button("Submit"):
            response = requests.post(f"{API_URL}/reviews/establishment", json={
                'user_id': state.user['id'],
                'establishment_id': estab['id'],
                'description': description,
                'rating': rating
            })
            if response.status_code == 200:
                refresh_estab_reviews(state.attrib, state.order)
                st.toast("Review added successfully!")
                state.page = 'estab/info'
                st.rerun()
            else:
                st.error("Failed to add review.")

def review_add_food():
    estab = state.selected_estab
    food = state.selected_food

    col1, col2 = st.columns([0.5, 10])

    with col1:
        if st.button('←', help="Go Back"):
            state.page = 'estab/food/info'
            st.rerun()

    with col2:
        st.title(f"Add Review for {food['name']}")
        
        rating = st.slider("Rating", 1, 5)  
        description = st.text_area("Description")

        if st.button("Submit"):
            response = requests.post(f"{API_URL}/reviews/food", json={
                'user_id': state.user['id'],
                'food_id': food['id'],
                'description': description,
                'rating': rating
            })
            if response.status_code == 200:
                st.toast("Review added successfully!")
                state.page = 'estab/food/info'
                st.rerun()
            else:
                st.error("Failed to add review.")
                

def delete_review(review_id):
    estab = state.selected_estab
    response = requests.put(f"{API_URL}/reviews/delete/{review_id}/{estab['id']}",)
    if response.status_code == 200:
        refresh_estab_reviews(state.attrib, state.order)
        st.toast("Review deleted successfully!")
    else:
        st.error("Failed to delete review.")


def edit_review(review_id, new_rating, new_description):
    estab = state.selected_estab
    response = requests.post(f"{API_URL}/reviews/update", json={
        'id': review_id,
        'rating': new_rating,
        'description': new_description,
        'establishment_id': estab['id']
    })
    if response.status_code == 200:
        refresh_estab_reviews(state.attrib, state.order)
        st.toast("Review updated successfully!")
    else:
        st.error("Failed to update review.")


def refresh_estab_reviews(attrib, order):
    estab = state.selected_estab

    response = requests.get(f"{API_URL}/reviews/establishment/{estab['id']}/{attrib}/{order}")

    if response.status_code != 200:
        st.error("Error Fetching establishments!")
        return
    
    et.refresh_stream('name', 'asc')
    state.rev_estab_stream = response.json()['reviews']

def review_estab_list():
    estab = state.selected_estab

    st.subheader(f"Reviews for {estab['name']}")
    
    attrib_mapping = {
        'Username': 'username',
        'Rating': 'rating',
        'Created At': 'created_at',
        'Updated At': 'updated_at'
    }

    attrib = st.selectbox('Order by:', ['Username', 'Rating', 'Created At'], index = 2, key = 'review_attrib')
    state.attrib = attrib_mapping[attrib]

    state.order = st.selectbox('Order', ['Ascending', 'Descending'], label_visibility='collapsed', key = 'review_order')
    state.order = 'asc' if state.order == 'Ascending' else 'desc'

    recent = st.selectbox('Show', ['All', 'Recent (<= 1 month)'], key='review_recent')

    if (recent == 'All'):
        refresh_estab_reviews(state.attrib, state.order)
    else:
        response = requests.get(f"{API_URL}/reviews/recent/establishment/{estab['id']}/{state.attrib}/{state.order}")

        if response.status_code != 200:
            st.error("Error Fetching establishments!")
        else:
            state.rev_estab_stream = response.json()['reviews']



    for review in state.rev_estab_stream:
        with st.container():
            st.divider()
            created_at_dt = datetime.strptime(review['created_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            formatted_created_at = created_at_dt.strftime('%B %d, %Y | %H:%M')

            # Building review information
            review_info = f"""
            **{review['username']}**
            ---
            - **Rating:** {review['rating']}  
            - **Description:** {review['description']}  
            - **Created:** {formatted_created_at}"""

            if review['updated_at']:
                updated_at_dt = datetime.strptime(review['updated_at'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
                formatted_updated_at = updated_at_dt.strftime('%B %d, %Y | %H:%M')
                review_info += f"- **Updated:** {formatted_updated_at}"

            st.info(review_info)

            if (state.user['id'] != review['user_id']):
                continue

            col3, col4 = st.columns(2)
            
            with col3:
                if st.button('Edit', key=f"edit_{review['id']}"):
                    state.show_edit = True

            with col4:
                if st.button('Delete', key=f"delete_{review['id']}"):
                    delete_review(review['id'])
                    refresh_estab_reviews(state.attrib, state.order)
                    st.rerun()

            if 'show_edit' in state and state.show_edit:
                new_rating = st.slider("New Rating", 1, 5, review['rating'], key=f"slider_{review['id']}")
                new_description = st.text_area("New Description", value=review['description'], key=f"descedit_{review['id']}")
                
                if st.button('Confirm Edit', key=f"confirm_edit_{review['id']}"):
                    state.show_edit = False
                    edit_review(review['id'], new_rating, new_description)
                    refresh_estab_reviews(state.attrib, state.order)
                    st.rerun()
                
                if st.button('Cancel', key=f"cancel_edit_{review['id']}"):
                    state.show_edit = False
                    st.rerun()

            st.divider()




def review_food_list():
    food = state.selected_food

    st.subheader(f"Reviews for {food['name']}")
    
    response = requests.get(f"{API_URL}/reviews/food/{food['id']}/rating/desc")
    
    if response.status_code != 200:
        st.error("Failed to fetch reviews.")
        return

    reviews = response.json().get('reviews', [])

    for review in reviews:
        with st.container():
            st.write(f"**Rating:** {review['rating']}")
            st.write(f"**Description:** {review['description']}")
            st.write(f"**Date:** {review['created_at']}")
            st.divider()
