from flask import Blueprint, jsonify, request
from db import get_db_connection  # Assuming you have a function to get DB connection

rfid_bp = Blueprint('rfid', __name__)

# This route handles the RFID data from the ESP32
@rfid_bp.route('/rfid_tap', methods=['POST'])
def rfid_tap():
    try:
        # Get the incoming JSON data
        data = request.get_json()

        # Extract bus_id and stop_name from the data
        bus_id = data.get('bus_id')
        stop_name = data.get('stop_name')

        # Check if both fields are present
        if not all([bus_id, stop_name]):
            return jsonify({"error": "Missing required fields"}), 400

        # Connect to the database
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)
            
        #connection.commit()


        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Respond with a success message and the scan ID
        return jsonify({
            "message": "RFID data received successfully",
            "bus_id": bus_id,
            "stop_name": stop_name
        }), 201  # 201 Created

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
