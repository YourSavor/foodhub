import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

def establish_connection():
    connection = psycopg2.connect(                                                  
        user = os.getenv("DATABASE_USERNAME"),                                      
        password = os.getenv("DATABASE_PASSWORD"),                                  
        host = os.getenv("DATABASE_IP"),                                            
        port = os.getenv("DATABASE_PORT"),                                          
        database = os.getenv("DATABASE_NAME")                                       
    )    

    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    connection.close()
    cursor.close()

def sample_query():
    connection, cursor = establish_connection()

    cursor.execute("INSERT INTO users (username, hashed_password, first_name, middle_name, last_name) VALUES ('test', 'test', 'test', 'test', 'test');")
    connection.commit()
    print('Succesfully Inserted Test User')

    cursor.execute("SELECT * FROM users;")
    records = cursor.fetchone()
    connection.commit()
    print(f'User: {records}')

    close_connection(connection, cursor)

if __name__ == '__main__':
    sample_query()