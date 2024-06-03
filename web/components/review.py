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

def review_estab_list():
    estab = state.selected_estab

    st.subheader(f"Reviews for {estab['name']}")
    
    url = f"{API_URL}/reviews/establishment/{estab['id']}/rating/desc"
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error(f"Failed to fetch reviews from {url}. Status code: {response.status_code}")
        return

    try:
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
                        # Handle edit functionality here
                        # Display form to edit review details
                        # Send request to API to update review
                        # Update UI accordingly
                        pass

                    # Add delete button
                    if st.button('Delete'):
                        # Prompt user to confirm deletion
                        if st.confirm(f"Are you sure you want to delete this review?"):
                            # Send request to API to delete review
                            # Update UI accordingly if deletion is successful
                            pass

                    st.divider()
    except Exception as e:
        st.error(f"Failed to parse JSON response: {str(e)}")




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
