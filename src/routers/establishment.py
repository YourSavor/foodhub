from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

router = APIRouter(prefix="/establishments", tags=["establishments"])

insert_establishment_query = 'INSERT INTO establishments (user_id, name, location) VALUES ( %s, %s, %s);'
update_establishment_query = 'UPDATE establishments SET (name=%s, location=%s) WHERE id=%s;'
delete_establishment_query = 'UPDATE establishments SET (is_deleted = true) WHERE id = %s;'


class CreateEstablishmentRequest(BaseModel):
    user_id: str
    name: str
    location: str

class UpdateEstablishmentRequest(BaseModel):
    id: str
    name: str
    location: str

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.post('/')
async def create_establishment(establishment: CreateEstablishmentRequest):
    connection, cursor = establish_connection()

    cursor.execute(insert_establishment_query, (establishment.user_id, establishment.name, establishment.location))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}

@router.put('/')
async def update_food(establishment: UpdateEstablishmentRequest):
    connection, cursor = establish_connection()

    cursor.execute(update_establishment_query, (establishment.name, establishment.location, establishment.id))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}

@router.put('/delete/{establishment_id}')
async def delete_food(establishment_id: str):
    connection, cursor = establish_connection()

    cursor.execute(delete_establishment_query, (establishment_id,))
    connection.commit()

    close_connection(connection, cursor)
    return {'success': True}