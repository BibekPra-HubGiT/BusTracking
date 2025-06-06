from flask import Blueprint, jsonify, request, session
from db import get_db_connection
from geopy.distance import geodesic

busRoutes_bp = Blueprint('busRoutes', __name__)

# Helper function to calculate distance
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters


@busRoutes_bp.route('/search_route', methods=['POST'])
def busRoutes():
    data = request.get_json()
    start_stop = data.get('from')
    end_stop = data.get('to')

    # Get and strip the input stops
    start_stop = start_stop.strip()
    end_stop = end_stop.strip()

    print(start_stop, end_stop)

    if not start_stop or not end_stop:
        return jsonify({"error": "Missing required fields"}), 400

    # Database connection
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)

    try:
        # Find routes that contain both start and end stops
        route_query = """
            SELECT DISTINCT r.route_id, r.route_name
            FROM routes r
            JOIN route_stops rs1 ON r.route_id = rs1.route_id
            JOIN stops s1 ON rs1.stop_id = s1.stop_id
            JOIN route_stops rs2 ON r.route_id = rs2.route_id
            JOIN stops s2 ON rs2.stop_id = s2.stop_id
            WHERE LOWER(s1.stop_name) = LOWER(%s) AND LOWER(s2.stop_name) = LOWER(%s)
        """
        cursor.execute(route_query, (start_stop, end_stop))
        matching_routes = cursor.fetchall()
        print(matching_routes)

        if not matching_routes:
            return jsonify({"error": "No matching routes found"}), 404

        results = []

        for route in matching_routes:
            route_id = route['route_id']
            route_name = route['route_name']

            # Get all stops on this route
            stops_query = """
                SELECT rs.stop_id, s.stop_name, rs.sequence, s.stop_order
                FROM route_stops rs
                JOIN stops s ON rs.stop_id = s.stop_id
                WHERE rs.route_id = %s
                ORDER BY rs.sequence ASC
            """
            cursor.execute(stops_query, (route_id,))
            route_data = cursor.fetchall()

            # Find start and end stop sequence numbers
            start_seq = end_seq = None
            for stop in route_data:
                if stop["stop_name"].lower() == start_stop.lower():
                    start_seq = stop["sequence"]
                if stop["stop_name"].lower() == end_stop.lower():
                    end_seq = stop["sequence"]

            if start_seq is None or end_seq is None:
                continue  # Skip routes where stop sequences are not found

            

            # Determine direction
            if start_seq > end_seq:
                direction = "reverse"
            else:
                direction = "forward"


             # Fetch buses in the correct direction
            buses_query = """
                SELECT id, bus_id, direction, stop_name
                FROM buses
                WHERE route_id = %s AND direction = %s
            """
            cursor.execute(buses_query, (route_id, direction))
            buses = cursor.fetchall()

            bus_details = []

            for bus in buses:
                bus_id = bus["bus_id"]
                stop_name = bus["stop_name"]


                # Find the sequence and stop_order of the bus's current stop
                bus_seq = None
                # bus_order = None
                for stop in route_data:
                    if stop["stop_name"].lower() == stop_name.lower():
                        bus_seq = stop["sequence"]
                        bus_order = stop["stop_order"]
                        break

                if bus_seq is None:
                    continue  # Skip if bus stop is not found in route_data

        
                # Include buses that are at the start stop or any stop before it
                if direction == "forward":
                    if bus_seq > start_seq:
                        continue  # Skip buses that are ahead of the user's start
                else:  # reverse direction
                    if bus_seq < start_seq:
                        continue  # Skip buses that are ahead in reverse direction


                # Calculate distance for this bus
                distance_query = """
                    SELECT ABS(s1.stop_order - s2.stop_order) AS distance_in_km
                    FROM stops s1, stops s2
                    WHERE s1.stop_name = %s AND s2.stop_name = %s
                """
                cursor.execute(distance_query, (start_stop, end_stop))
                distance_result = cursor.fetchone()
                distance_km = distance_result["distance_in_km"] if distance_result else None

                bus_details.append({
                        "bus_id": bus_id,
                        "direction": direction,
                        "distance_km": distance_km,
                        "stop_name":stop_name,
                    })
                    

            # Append final route details
            results.append({
                "route_id": route_id,
                "route_name": route_name,
                "buses": bus_details
            })

        cursor.close()
        connection.close()

        print(results)

        return jsonify({"routes": results})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
