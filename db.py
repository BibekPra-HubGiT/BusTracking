import mysql.connector
import bcrypt
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',        
            password='Bibek@2025',   
            database='Bus_Tracking'     
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(stored_hash, password):
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'),stored_hash)
