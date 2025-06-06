from flask import Blueprint, jsonify, request, session
from db import get_db_connection, verify_password
login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email_or_number = data.get('emailOrNumber')
        password = data.get('password')

        if not email_or_number or not password:
            return jsonify({"error": "Missing required fields"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)
        # Check both email and phone_number
        cursor.execute("""
            SELECT * FROM Users 
            WHERE email = %s OR phone_number = %s
        """, (email_or_number, email_or_number))
        
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            connection.close()
            return jsonify({"error": "Invalid credentials"}), 401

        if verify_password(user['password'], password):
            cursor.close()
            connection.close()
            return jsonify({
                "message": "Login successful",
                "user": {
                    "full_name": user['full_name'],
                    "email": user['email'],
                    "phone_number": user['phone_number'],
                    "role": user['role']
                }
            }), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500