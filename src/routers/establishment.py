from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

router = APIRouter(prefix="/establishments", tags=["establishments"])

insert_establishment_query = 'INSERT INTO establishments (user_id, name, location) VALUES ( %s, %s, %s);'
update_establishment_query = 'UPDATE establishments SET (name=%s, location=%s) WHERE id=%s;'
delete_establishment_query = 'UPDATE establishments SET is_deleted = true WHERE id = %s;'

view_establishment_query = 'SELECT * FROM establishments WHERE is_deleted = false ORDER BY '
high_establishment_query = 'SELECT * FROM establishments WHERE rating >= 4 AND  is_deleted = false ORDER BY rating '

class CreateEstablishmentRequest(BaseModel):
    user_id: str
    name: str
    location: str

class UpdateEstablishmentRequest(BaseModel):
    id: str
    name: str
    location: str

class DeleteEstablishRequest(BaseModel):
    id: str

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.get('/all/{order}/{attribute}')
async def retrieve_establishments(order: str, attribute: str):
    connection, cursor = establish_connection()
    
    cursor.execute(view_establishment_query + f'{attribute.lower()} {order.upper()};')
    establishment_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not establishment_data:
        return {
            'success': 0,
            'establishments': []
        }
    
    columns = get_columns(cursor)
    establishment_list = [dict(zip(columns, data)) for data in establishment_data]
    
    data_dict = {
        'success': len(establishment_list),
        'establishments': establishment_list
    }

    return data_dict

@router.get('/high/{order}')
async def retrieve_high_establishments(order: str):
    connection, cursor = establish_connection()
    
    cursor.execute(high_establishment_query + f'{order.upper()};')
    establishment_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)

    if not establishment_data:
        return {
            'success': 0,
            'establishments': []
        }
    
    columns = get_columns(cursor)
    establishment_list = [dict(zip(columns, data)) for data in establishment_data]
    
    data_dict = {
        'success': len(establishment_list),
        'establishments': establishment_list
    }

    return data_dict

@router.post('/insert')
async def create_establishment(establishment: CreateEstablishmentRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_establishment_query, (establishment.user_id, establishment.name, establishment.location))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}

@router.put('/udate')
async def update_food(establishment: UpdateEstablishmentRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_establishment_query, (establishment.name, establishment.location, establishment.id))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}

@router.put('/delete/')
async def delete_food(establishment: DeleteEstablishRequest):
    connection, cursor = establish_connection()

    cursor.execute(delete_establishment_query, (establishment.id,))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}