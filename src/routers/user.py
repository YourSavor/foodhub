from fastapi import APIRouter
from pydantic import BaseModel
from db.db import establish_connection, close_connection

delete_user = "UPDATE users SET (is_deleted = true) WHERE user_id = %s;"
update_user = 'UPDATE users SET username=%s, first_name=%s, middle_name=%s, last_name=%s WHERE id = %s;'
search_user_name = 'SELECT * FROM users WHERE name LIKE "% %s %";'
search_user_id = 'SELECT * FROM users WHERE id = %s;'
search_user_username = 'SELECT * FROM users WHERE username=%s;'



router = APIRouter()   

class UpdateUser(BaseModel):
    user_id: str
    username: str
    first_name: str
    middle_name: str
    last_name: str

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.get('/users/by-username/{username}')
async def user_id(username: str):
    connection, cursor = establish_connection()
    cursor.execute(search_user_username, (username,))

    columns = get_columns
    user_data = cursor.fetchone()
    connection.commit()

    close_connection(connection, cursor)
    if not user_data:
        return {'message': 'Invalid username!'}

    user_dict = dict(zip(columns, user_data))
    user_dict['message'] = 'User found!'
    return user_dict


@router.get('/user/{user_id}')
async def user_transactions(user_id: str):
    return {}

@router.get('/user/{name}')
async def user_transactions(name: str):
    return {}


@router.post('/users/update')
async def update_user_details(user: UpdateUser):
    connection, cursor = establish_connection()

    # add updated at parameter
    cursor.execute(update_user, (user.username, user.first_name, user.middle_name, user.last_name, user.user_id))
    connection.commit()
    
    connection.commit()
    close_connection(connection, cursor)
    return {'message': 'User updated successfully'}
