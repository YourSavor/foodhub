from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

insert_review_query = 'INSERT INTO reviews (user_id, establishment_id, food_id, rating, description) VALUES (%s, %s, %s, (SELECT establishment_id , AVG(rating) FROM reviews WHERE establishment_id=%s), %s);'
update_review_query = 'UPDATE reviews SET (user_id=%s, establishment_id=%s, food_id=%s, description=%s) WHERE food_id=%s;'
delete_review_query = 'UPDATE reviews SET (is_deleted = true) WHERE id = %s;'

router = APIRouter(prefix="\reviews", tags=["reviews"])   
    

class UpdateReviewRequest(BaseModel):
    id: str
    user_id: str
    establishment_id: str
    food_id: str
    rating: float
    description: str

class CreateReviewRequest(BaseModel):
    user_id: str
    establishment_id: str
    food_id: str
    description: str

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.post('/')
async def create_review(review: CreateReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_review_query(review.user_id, review.establishment_id, review.food_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message' : 'Review added successfully'}

@router.post('/update')
async def update_review(review: UpdateReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_review_query(review.user_id, review.establishment_id, review.food_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message' : 'Review updated successfully'}

@router.put('/')
async def delete_review(id: str):
    connection, cursor = establish_connection()

    cursor.execute(delete_review_query, (id,))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Review deleted successfully'}