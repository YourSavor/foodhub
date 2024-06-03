from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

# SQL queries
view_review_query = 'SELECT * FROM reviews WHERE id = %s AND is_deleted = FALSE;'

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

update_review_query = 'UPDATE reviews SET user_id=%s, establishment_id=%s, food_id=%s, rating=%s, description=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s;'

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Pydantic models
class UpdateReviewRequest(BaseModel):
    id: str
    establishment_id: str = ''
    food_id: str = ''
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

insert_food_review_query = """
INSERT INTO reviews (user_id, food_id, rating, description) VALUES (%s, %s, %s, %s);
UPDATE foods SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE food_id = %s AND is_deleted = false), 0) where id = %s;
"""

@router.post('/food')
async def create_food_review(review: CreateFoodReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_food_review_query, (review.user_id, review.food_id, review.rating, review.description, review.food_id, review.food_id))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Review added successfully'}


insert_establishment_review_query = """
INSERT INTO reviews (user_id, establishment_id, rating, description) VALUES (%s, %s, %s, %s);
UPDATE establishments SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE establishment_id = %s AND is_deleted = false), 0) where id = %s;
"""

@router.post('/establishment')
async def create_establishment_review(review: CreateEstablishmentReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_establishment_review_query, (review.user_id, review.establishment_id, review.rating, review.description, review.establishment_id, review.establishment_id))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review added successfully'}



update_review_query = """
UPDATE reviews SET rating=%s, description=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s;
UPDATE establishments SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE establishment_id = %s AND is_deleted = false), 0) where id = %s;
UPDATE foods SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE food_id = %s AND is_deleted = false), 0) where id = %s;
"""


@router.post('/update')
async def update_review(review: UpdateReviewRequest):
    connection, cursor = establish_connection()
    
    cursor.execute(update_review_query, (review.rating, review.description, review.id, review.establishment_id, review.establishment_id, review.food_id, review.food_id))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review updated successfully'}




delete_review_query = """
UPDATE reviews SET is_deleted = TRUE, updated_at=CURRENT_TIMESTAMP WHERE id = %s;
UPDATE establishments SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE establishment_id = %s AND is_deleted = false), 0) where id = %s;
UPDATE foods SET rating = coalesce((SELECT AVG(rating) FROM reviews WHERE food_id = %s AND is_deleted = false), 0) where id = %s;
"""

@router.put('/delete/{id}/{establishment_id}/{food_id}')
async def delete_review(id: str, establishment_id: str, food_id: str):
    connection, cursor = establish_connection()
    
    cursor.execute(delete_review_query, (id, establishment_id, establishment_id, food_id, food_id))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'Review deleted successfully'}

view_reviews_by_establishment_query = """SELECT 
r.*, u.username
 FROM reviews r 
left join users u on r.user_id = u.id 
WHERE establishment_id = %s AND r.is_deleted = false"""

@router.get('/establishment/{establishment_id}/{attribute}/{order}')
async def view_reviews_by_establishment(establishment_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()

    # Construct the query with string interpolation
    query = f"{view_reviews_by_establishment_query} ORDER BY {attribute} {order}, r.updated_at {order};"

    cursor.execute(query, (establishment_id,))
    reviews = cursor.fetchall()
    connection.commit()
    
    close_connection(connection, cursor)
    
    if not reviews:
        return {'success': 0, 'reviews': []}

    columns = get_columns(cursor)
    reviews_list = [dict(zip(columns, review)) for review in reviews]
    
    return {'success': len(reviews_list), 'reviews': reviews_list}


view_reviews_by_food_query = """SELECT 
r.*, u.username
 FROM reviews r 
left join users u on r.user_id = u.id 
WHERE food_id = %s AND r.is_deleted = false"""

@router.get('/food/{food_id}/{attribute}/{order}')
async def view_reviews_by_food(food_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()

    query = f"{view_reviews_by_food_query} ORDER BY {attribute} {order}, r.updated_at {order};"

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

view_reviews_recent_by_food_query = """SELECT 
r.*, u.username
 FROM reviews r 
left join users u on r.user_id = u.id 
WHERE food_id = %s AND r.is_deleted = false AND r.created_at >= CURRENT_DATE - INTERVAL \'1 month\'"""

view_reviews_recent_by_establishment_query = """SELECT 
r.*, u.username
 FROM reviews r 
left join users u on r.user_id = u.id 
WHERE establishment_id = %s AND r.is_deleted = false AND r.created_at >= CURRENT_DATE - INTERVAL \'1 month\'"""

@router.get('/recent/establishment/{establishment_id}/{attribute}/{order}')
async def view_recent_reviews_by_establishment(establishment_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()

    # Construct the query with string interpolation
    query = f"{view_reviews_recent_by_establishment_query} ORDER BY {attribute} {order}, r.updated_at {order};"

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

    query = f"{view_reviews_recent_by_establishment_query} ORDER BY {attribute} {order}, r.updated_at {order};"

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