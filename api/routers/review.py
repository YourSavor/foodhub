from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

# SQL queries
insert_food_review_query = 'INSERT INTO reviews (user_id, food_id, rating, description) VALUES (%s, %s, %s, %s);'
insert_establishment_review_query = 'INSERT INTO reviews (user_id, establishment_id, rating, description) VALUES (%s, %s, %s, %s);'
update_review_query = 'UPDATE reviews SET user_id=%s, establishment_id=%s, food_id=%s, rating=%s, description=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s;'
delete_review_query = 'UPDATE reviews SET is_deleted = TRUE, updated_at=CURRENT_TIMESTAMP WHERE id = %s;'
view_reviews_by_establishment_query = "SELECT * FROM reviews WHERE establishment_id = %s ORDER BY %s %s"
view_reviews_by_food_query = 'SELECT * FROM reviews WHERE food_id = %s AND is_deleted = FALSE ORDER BY %s %s;'
view_review_query = 'SELECT * FROM reviews WHERE id = %s AND is_deleted = FALSE;'
view_reviews_recent_by_establishment_query = 'SELECT * FROM reviews WHERE establishment_id = %s AND created_at >= CURRENT_DATE - INTERVAL \'1 month\' AND is_deleted = FALSE ORDER BY %s %s;'
view_reviews_recent_by_food_query = 'SELECT * FROM reviews WHERE food_id = %s AND created_at >= CURRENT_DATE - INTERVAL \'1 month\' AND is_deleted = FALSE ORDER BY %s %s;'
search_reviews_query = """
    SELECT * FROM reviews 
    WHERE is_deleted = FALSE 
    AND LOWER(description) LIKE LOWER(CONCAT('%', %s, '%')) 
    ORDER BY 
        CASE 
            WHEN LOWER(description) = LOWER(%s) THEN 0 
            WHEN LOWER(description) LIKE LOWER(CONCAT(%s, '%')) THEN 1 
            ELSE 2 
        END;
"""

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Pydantic models
class UpdateReviewRequest(BaseModel):
    id: str
    user_id: str
    establishment_id: str = None
    food_id: str = None
    rating: float
    description: str

class CreateFoodReviewRequest(BaseModel):
    user_id: str
    food_id: str
    description: str
    rating: int

class CreateEstablishmentReviewRequest(BaseModel):
    user_id: str
    establishment_id: str
    description: str
    rating: int

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.post('/food')
async def create_food_review(review: CreateFoodReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_food_review_query, (review.user_id, review.food_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Review added successfully'}

@router.post('/establishment')
async def create_establishment_review(review: CreateEstablishmentReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_establishment_review_query, (review.user_id, review.establishment_id, review.rating, review.description))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review added successfully'}

@router.post('/update')
async def update_review(review: UpdateReviewRequest):
    connection, cursor = establish_connection()
    
    cursor.execute(update_review_query, (review.user_id, review.establishment_id, review.food_id, review.rating, review.description, review.id))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review updated successfully'}

@router.put('/delete/{id}')
async def delete_review(id: str):
    connection, cursor = establish_connection()
    
    cursor.execute(delete_review_query, (id,))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review deleted successfully'}

@router.get('/establishment/{establishment_id}/{attribute}/{order}')
async def view_reviews_by_establishment(establishment_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()
    
    # Check if the order is either ASC or DESC
    if order.upper() not in ['ASC', 'DESC']:
        return {'error': 'Invalid sort order. Use "ASC" or "DESC".'}
    
    # Ensure the attribute is a valid column name to prevent SQL injection
    if attribute not in ['column1', 'column2', 'column3']:
        return {'error': 'Invalid attribute name.'}
    
    # Construct the query with string interpolation
    query = f"{view_reviews_by_establishment_query} ORDER BY {attribute} {order};"
    
    cursor.execute(query, (establishment_id,))
    reviews = cursor.fetchall()
    connection.commit()
    
    close_connection(connection, cursor)
    
    if not reviews:
        return {'success': 0, 'reviews': []}
    
    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]
    
    return {'success': len(reviews_list), 'reviews': reviews_list}



@router.get('/food/{food_id}/{attribute}/{order}')
async def view_reviews_by_food(food_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()

    query = f"{view_reviews_by_food_query} ORDER BY {attribute} {order};"

    cursor.execute(query, (food_id,))
    reviews = cursor.fetchall()

    connection.commit()
    close_connection(connection, cursor)

    if not reviews:
        return {'success': 0, 'reviews': []}

    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]

    return {'success': len(reviews_list), 'reviews': reviews_list}

@router.get('/{id}')
async def view_review_by_id(id: str):
    connection, cursor = establish_connection()
    
    cursor.execute(view_review_query, (id,))
    review = cursor.fetchone()
    connection.commit()
    close_connection(connection, cursor)
    
    if not review:
        return {'success': 0, 'review': None}
    
    columns = get_columns(cursor)
    review_dict = dict(zip(columns, review))
    
    return {'success': 1, 'review': review_dict}

@router.get('/recent/establishment/{establishment_id}/{attribute}/{order}')
async def view_recent_reviews_by_establishment(establishment_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()
    query = view_reviews_recent_by_establishment_query % (attribute, order)
    cursor.execute(query, (establishment_id,))
    reviews = cursor.fetchall()
    connection.commit()
    close_connection(connection, cursor)
    
    if not reviews:
        return {'success': 0, 'reviews': []}
    
    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]
    
    return {'success': len(reviews_list), 'reviews': reviews_list}

@router.get('/recent/food/{food_id}/{attribute}/{order}')
async def view_recent_reviews_by_food(food_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()
    query = view_reviews_recent_by_food_query % (attribute, order)
    cursor.execute(query, (food_id,))
    reviews = cursor.fetchall()
    connection.commit()
    close_connection(connection, cursor)
    
    if not reviews:
        return {'success': 0, 'reviews': []}
    
    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]
    
    return {'success': len(reviews_list), 'reviews': reviews_list}

@router.get('/search')
async def search_reviews(description: str):
    connection, cursor = establish_connection()
    description_lower = description.lower()
    cursor.execute(search_reviews_query, (f'%{description_lower}%', description_lower, description_lower))
    reviews = cursor.fetchall()
    connection.commit()
    close_connection(connection, cursor)
    
    if not reviews:
        return {'success': 0, 'reviews': []}
    
    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]
    
    return {'success': len(reviews_list), 'reviews': reviews_list}