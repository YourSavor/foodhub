from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

insert_food_query = 'INSERT INTO foods (establishment_id, name, type, price, rating) VALUES (%s, %s, %s, %s, %s);'
update_food_query = 'UPDATE foods SET (establishment_id=%s, name=%s, type=%s, price=%s) WHERE id=%s;'
delete_food_query = 'UPDATE foods SET is_deleted = TRUE WHERE id = %s;'

router = APIRouter(prefix="/foods", tags=["foods"])

class UpdateFoodRequest(BaseModel):
    id: str
    establishment_id: str
    name: str
    type: str
    price: float
    rating: float

class CreateFoodRequest(BaseModel):
    establishment_id: str
    name: str
    type: str
    price: float

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.post('/')
async def create_food(food: CreateFoodRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_food_query, (food.establishment_id, food.name, food.type, food.price, 0))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food added successfully'}

@router.put('/update')
async def update_food(food: UpdateFoodRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_food_query, (food.establishment_id, food.name, food.type, food.price, food.id))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food updated successfully'}

@router.put('/')
async def delete_food(id: str):
    connection, cursor = establish_connection()

    cursor.execute(delete_food_query, (id,))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food deleted successfully'}
