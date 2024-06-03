import requests
import streamlit as st

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
                st.success("Review added successfully!")
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
                st.success("Review added successfully!")
                state.page = 'estab/food/info'
                st.rerun()
            else:
                st.error("Failed to add review.")
                

def delete_review(review_id):
    response = requests.put(f"{API_URL}/reviews/delete/{review_id}")
    if response.status_code == 200:
        st.success("Review deleted successfully!")
    else:
        st.error("Failed to delete review.")


def edit_review(review_id, new_rating, new_description):
    response = requests.put(f"{API_URL}/reviews/update", json={
        'id': review_id,
        'rating': new_rating,
        'description': new_description
    })
    if response.status_code == 200:
        st.success("Review updated successfully!")
    else:
        st.error("Failed to update review.")


def review_estab_list():
    estab = state.selected_estab

    st.subheader(f"Reviews for {estab['name']}")
    
    # Fetch reviews from the API
    response = requests.get(f"{API_URL}/reviews/establishment/{estab['id']}/rating/desc")
    
    if response.status_code != 200:
        st.error("Failed to fetch reviews.")
        return

    reviews = response.json().get('reviews', [])

    if not reviews:
        st.info("No reviews available for this establishment.")
    else:
        for review in reviews:
            with st.container():
                st.write(f"**Rating:** {review['rating']}")
                st.write(f"**Description:** {review['description']}")
                st.write(f"**Date:** {review['created_at']}")
                
                # Add edit button
                if st.button('Edit'):
                    new_rating = st.slider("New Rating", 1, 5, review['rating'])
                    new_description = st.text_area("New Description", value=review['description'])
                    
                    # Prompt user to confirm edit
                    if st.button('Confirm Edit'):
                        # Call edit_review function
                        edit_review(review['id'], new_rating, new_description)

                # Add delete button
                if st.button('Delete'):
                    # Prompt user to confirm deletion
                    if st.confirm(f"Are you sure you want to delete this review?"):
                        # Call delete_review function
                        delete_review(review['id'])

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
