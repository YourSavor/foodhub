from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.db import establish_connection, close_connection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

select_user = 'SELECT * FROM users;'
delete_user = 'UPDATE users SET (is_deleted = true) WHERE user_id = %s;'
insert_user = 'INSERT INTO users (username, hashed_password, first_name, middle_name, last_name) VALUES (%s, %s, %s, %s, %s);'
update_user_query = 'UPDATE users SET username=%s, first_name=%s, middle_name=%s, last_name=%s WHERE id = %s;'
search_user_name = 'SELECT * FROM users WHERE name LIKE "% %s %";'
search_user_id = 'SELECT * FROM users WHERE id = %s;'
search_user_username = 'SELECT * FROM users WHERE username=%s;'


router = APIRouter(prefix="/users", tags=["users"])

class UpdateUserRequest(BaseModel):
    user_id: str
    username: str
    first_name: str
    middle_name: str
    last_name: str

class UserSignUpRequest(BaseModel):
    username: str
    password: str
    first_name: str
    middle_name: str
    last_name: str

class UserSignInRequest(BaseModel):
    username: str
    password: str

def get_columns(cursor):
    return [col[0] for col in cursor.description]

@router.get('')
async def get_user():
    connection, cursor = establish_connection()

    # shalle check first if user exist
    
    cursor.execute(select_user)
    user_data = cursor.fetchall()
    connection.commit()

    close_connection(connection, cursor)
    if not user_data:
        return {'message': 'No user exists!'}
    
    columns = get_columns(cursor)
    user_list = [dict(zip(columns, data)) for data in user_data]
    
    data_dict = {
        'message': 'Users fetched successfully!',
        'users': user_list
    }

    return data_dict

@router.put('')
async def update_user(user: UpdateUserRequest):
    connection, cursor = establish_connection()

    # shalle check first if user exist

    # add updated at parameter
    cursor.execute(update_user_query, (user.username, user.first_name, user.middle_name, user.last_name, user.user_id))
    connection.commit()
    
    close_connection(connection, cursor)
    return {'message': 'User updated successfully'}

@router.get('/username/{username}')
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


@router.get('/id/{user_id}')
async def user_transactions(user_id: str):
    connection, cursor = establish_connection()
    cursor.execute(search_user_id, (user_id,))

    columns = get_columns
    user_data = cursor.fetchone()
    connection.commit()

    close_connection(connection, cursor)
    if not user_data:
        return {'message': 'Invalid user id!'}

    user_dict = dict(zip(columns, user_data))
    user_dict['message'] = 'User found!'
    return user_dict

@router.post("/signin")
async def signin(user: UserSignInRequest):
    connection, cursor = establish_connection()
    cursor.execute(search_user_username, (user.username,))
    user_data = cursor.fetchone()
    close_connection(connection, cursor)

    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_dict = dict(zip(get_columns(cursor), user_data))
    if not pwd_context.verify(user.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": "Successfully signed in", "user": user_dict}

@router.post("/signup")
async def create_user(user: UserSignUpRequest):
    connection, cursor = establish_connection()
    hashed_password = pwd_context.hash(user.password)

    cursor.execute(search_user_username, (user.username,))
    if cursor.fetchone():
        close_connection(connection, cursor)
        raise HTTPException(status_code=400, detail="Username already exists")

    cursor.execute(insert_user, (user.username, hashed_password, user.first_name, user.middle_name, user.last_name))
    connection.commit()
    close_connection(connection, cursor)
    return {"message": "User created successfully"}
