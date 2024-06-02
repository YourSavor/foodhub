from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

insert_food_query = 'INSERT INTO foods (establishment_id, name, type, price, rating) VALUES (%s, %s, %s, %s, %s);'
update_food_query = 'UPDATE foods SET name=%s, type=%s, price=%s WHERE id=%s;'
delete_food_query = 'UPDATE foods SET is_deleted = TRUE WHERE id = %s; UPDATE reviews SET is_deleted = TRUE WHERE food_id = %s;'

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

@router.post('')
async def create_food(food: CreateFoodRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_food_query, (food.establishment_id, food.name, food.type, food.price, 0))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food added successfully'}

@router.put('')
async def update_food(food: UpdateFoodRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_food_query, (food.name, food.type, food.price, food.id))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food updated successfully'}

@router.put('/delete/{food_id}')
async def delete_food(food_id: str):
    connection, cursor = establish_connection()

    cursor.execute(delete_food_query, (food_id, food_id))
    connection.commit()

    close_connection(connection, cursor)
    return {'message': 'Food and associated reviews deleted'}


view_all_food_query = 'SELECT * FROM foods WHERE is_deleted = false AND establishment_id = %s'

@router.get('/all/{establishment_id}/{attribute}/{order}')
async def retrieve_food(establishment_id: str, attribute: str, order: str):
    connection, cursor = establish_connection()

    order_by_query = ' ORDER BY ' + f"{attribute.lower()} {order.upper()};"

    print(view_all_food_query + order_by_query)

    cursor.execute(view_all_food_query + order_by_query, (establishment_id, ))
    food_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'foods': []
        }
    
    columns = get_columns(cursor)
    food_list = [dict(zip(columns, data)) for data in food_data]

    data_dict = {
        'success': len(food_list),
        'foods': food_list
    }

    return data_dict

@router.get('/all/{establishment_id}/{lowprice}/{highprice}/{attribute}/{order}')
async def retrieve_food_pricerange(establishment_id: str, lowprice:float, highprice:float, attribute: str, order: str):
    connection, cursor = establish_connection()

    order_by_query = ' ORDER BY' + f'{attribute.lower(), order.upper()};'

    additional_query = ' AND price BETWEEN %s AND %s' + order_by_query

    cursor.execute(view_all_food_query + additional_query, (establishment_id, lowprice, highprice))
    food_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'foods': []
        }
    
    columns = get_columns(cursor)
    food_list = [dict(zip(columns, data)) for data in food_data]

    data_dict = {
        'success': len(food_list),
        'foods': food_list
    }

    return data_dict


@router.get('/all/{establishment_id}/{type}/{attribute}/{order}')
async def retrieve_food_type(establishment_id: str, type:str, attribute: str, order: str):
    connection, cursor = establish_connection()

    order_by_query = ' ORDER BY' + f'{attribute.lower(), order.upper()};'

    additional_query = ' AND type = %s' + order_by_query

    cursor.execute(view_all_food_query + additional_query, (establishment_id, type))
    food_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'foods': []
        }
    
    columns = get_columns(cursor)
    food_list = [dict(zip(columns, data)) for data in food_data]

    data_dict = {
        'success': len(food_list),
        'foods': food_list
    }

    return data_dict


@router.get('/all/{establishment_id}/{type}/{lowprice}/{highprice}/{attribute}/{order}')
async def retrieve_food_type_pricerange(establishment_id: str, type:str, lowprice:float, highprice:float, attribute: str, order: str):
    connection, cursor = establish_connection()

    order_by_query = ' ORDER BY' + f'{attribute.lower(), order.upper()};'

    additional_query = ' AND type = %s AND price BETWEEN %s AND %s' + order_by_query

    cursor.execute(view_all_food_query + additional_query, (establishment_id, type, lowprice, highprice))
    food_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'foods': []
        }
    
    columns = get_columns(cursor)
    food_list = [dict(zip(columns, data)) for data in food_data]

    data_dict = {
        'success': len(food_list),
        'foods': food_list
    }

    return data_dict



view_food_query = 'SELECT * FROM foods WHERE is_deleted = false AND id = %s;'

@router.get('/{id}')
async def retrieve_food_id(id: str):
    connection, cursor = establish_connection()

    cursor.execute(view_food_query, (id,))
    food_data = cursor.fetchone() 
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'food': None
        }
    
    columns = get_columns(cursor)
    food_dict = dict(zip(columns, food_data))

    return {
        'success': 1,
        'food': food_dict
    }

search_food_query = """
    SELECT * FROM foods 
    WHERE is_deleted = false 
    AND LOWER(name) LIKE %s 
    ORDER BY 
        CASE 
            WHEN LOWER(name) = %s THEN 0 
            WHEN LOWER(name) LIKE %s THEN 1 
            ELSE 2 
        END;
"""

@router.get('/all/search/{name}')
async def search_food(name: str):
    connection, cursor = establish_connection()

    name_lower = name.lower()
    cursor.execute(
        search_food_query, 
        (f'{name_lower}%', f'%{name_lower}%', f'{name_lower}%')
    )
    food_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not food_data:
        return {
            'success': 0,
            'foods': []
        }
    
    columns = get_columns(cursor)
    food_list = [dict(zip(columns, data)) for data in food_data]

    data_dict = {
        'success': len(food_list),
        'foods': food_list
    }

    return data_dict

