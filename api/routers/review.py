from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

insert_food_review_query = 'INSERT INTO reviews (user_id, food_id, rating, description) VALUES (%s, %s, %s, %s);'
insert_establishment_review_query = 'INSERT INTO reviews (user_id, establishment_id, rating, description) VALUES (%s, %s, %s, %s);'
update_review_query = 'UPDATE reviews SET (user_id=%s, establishment_id=%s, food_id=%s, description=%s) WHERE food_id=%s;'
delete_review_query = 'UPDATE reviews SET (is_deleted = true) WHERE id = %s;'

router = APIRouter(prefix="/reviews", tags=["reviews"])   
    

class UpdateReviewRequest(BaseModel):
    id: str
    user_id: str
    establishment_id: str
    food_id: str
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
async def create_fodd_review(review: CreateFoodReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_food_review_query, (review.user_id, review.food_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message' : 'Review added successfully'}

@router.post('/establishment')
async def create_establsihment_review(review: CreateEstablishmentReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_establishment_review_query, (review.user_id, review.establishment_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message' : 'Review added successfully'}

@router.post('update')
async def update_review(review: UpdateReviewRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_review_query(review.user_id, review.establishment_id, review.food_id, review.rating, review.description))
    connection.commit()

    close_connection(connection, cursor)
    return {'message' : 'Review updated successfully'}

@router.put('')
async def delete_review(id: str):
    connection, cursor = establish_connection()

    cursor.execute(delete_review_query, (id,))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Review deleted successfully'}