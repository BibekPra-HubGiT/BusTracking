from flask import Blueprint, jsonify, request, session
from db import get_db_connection, hash_password
createuser_bp = Blueprint('createUser', __name__)


@createuser_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        full_name = data.get('fullName')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        role = data.get('role')
        password = data.get('password')

        # Check if all required fields are present
        if not all([full_name, email, phone_number, role, password]):
            return jsonify({"error": "Missing required fields"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({"error": "Email already exists"}), 409  # 409 Conflict

        # Hash the password before storing
        hashed_password = hash_password(password)  # Assuming you have a hash_password function
        
        # Insert new user
        cursor.execute("""
            INSERT INTO Users (full_name, email, phone_number, role, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, phone_number, role, hashed_password))
        
        connection.commit()
        
        # Get the newly created user's ID
        cursor.execute("SELECT LAST_INSERT_ID() as user_id")
        user_id = cursor.fetchone()['user_id']

        cursor.close()
        connection.close()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
            "role": role
        }), 201  # 201 Created

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500