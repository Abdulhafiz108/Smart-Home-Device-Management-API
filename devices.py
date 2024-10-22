from flask import jsonify, request
from db import create_connection
from mysql.connector import Error


def create_logs_table():
    """
    Creates the device_logs table in the MySQL database if it does not exist.

    This table logs actions performed on devices, including the action taken,
    the device ID, and a timestamp.

    Error Handling:
        - If the database connection fails, an error is logged.
    """
    connection = create_connection()
    if connection is None:
        print("Failed to create logs table: Database connection failed.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id INT NOT NULL,
            action VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        connection.commit()
    except Error as e:
        print(f"Error creating logs table: {e}")
    finally:
        cursor.close()
        connection.close()


create_logs_table()


def get_devices():
    """
    Retrieves the list of all devices from the database.

    Returns:
        JSON response containing a list of devices.
        An error message with status code 500 if the request fails.

    Methods:
        GET
    """
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM devices;")
        devices = cursor.fetchall()
    except Error as e:
        return jsonify(
                {"error": f"The error '{e}' occurred while fetching devices."}
                ), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"devices": devices})


def add_device():
    """
    Adds a new device to the database.

    Input (JSON):
        - name: The name of the device (string).
        - status: The status of the device (On/Off) (string).

    Returns:
        JSON response with a success message if the device is added.
        An error message with status code 500 if the request fails.

    Methods:
        POST
    """
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    new_device = request.json
    device_name = new_device['name']
    device_status = new_device['status']

    cursor = connection.cursor()
    cursor.execute("SELECT id FROM devices ORDER BY id;")
    all_ids = [row[0] for row in cursor.fetchall()]

    vacant_id = 1
    for idx in all_ids:
        if vacant_id == idx:
            vacant_id += 1
        else:
            break

    try:
        cursor.execute(
                "INSERT INTO devices (id, name, status) VALUES (%s, %s, %s)", (
                    vacant_id, device_name, device_status))
        connection.commit()

        cursor.execute(
                "INSERT INTO device_logs (device_id, action) VALUES (%s, %s)",
                (vacant_id, f"Added device '{device_name}'"))
        connection.commit()

        return jsonify({
           "message": (
               f"Device '{device_name}' added successfully "
               + f"with ID {vacant_id}."
           )
        }), 201
    except Error as e:
        return jsonify({
            "error": f"The error '{e}' occurred while adding the device."
            }), 500
    finally:
        cursor.close()
        connection.close()


def update_device(device_id, action):
    """
    Updates the status of a device in the database.

    Input:
        - device_id: ID of the device to update.
        - action: The new status of the device (On/Off) (string).

    Returns:
        None

    Error Handling:
        - Logs the device action into device_logs if the update is successful.
    """
    connection = create_connection()
    if connection is None:
        print("Database connection failed")
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
                "SELECT status FROM devices WHERE id = %s", (device_id,))
        current_status = cursor.fetchone()

        if current_status is None:
            print(f"Device ID {device_id} does not exist.")
            return jsonify({"error": "Device not found."}), 404

        current_status = current_status[0]

        if current_status != action:
            cursor.execute(
                    "UPDATE devices SET status = %s WHERE id = %s",
                    (action, device_id))
            connection.commit()
            print(f"Device {device_id} status updated to {action}.")

            cursor.execute(
                    "INSERT INTO device_logs (device_id, action) "
                    "VALUES (%s, %s)",
                    (device_id, f"Updated device status to '{action}'")
            )
            connection.commit()
        else:
            print(f"Device {device_id} is already {action}. No change made.")
    except Error as e:
        print(f"Error updating device {device_id}: {e}")
    finally:
        cursor.close()
        connection.close()


def update_device_now(device_id):
    """
    Updates the device status based on the request's JSON data.

    Input (JSON):
        - action: The new status of the device (On/Off) (string).

    Path Parameters:
        - device_id: ID of the device to update.

    Returns:
        JSON response with a success message if the device is updated.
        An error message with status code 400 if the request is invalid.

    Methods:
        PUT
    """
    data = request.get_json()
    action = data.get('action')

    if action not in ['On', 'Off']:
        return jsonify(
                {"error": "Invalid action. Must be 'On' or 'Off'."}), 400

    update_device(device_id, action)
    return jsonify(
            {"message": f"Device {device_id} updated to {action}."}), 200


def delete_device(device_id):
    """
    Deletes a device from the database.

    Path Parameters:
        - device_id: ID of the device to delete.

    Returns:
        JSON response confirming the device deletion.
        An error message with status code 404 if the device ID does not exist.

    Methods:
        DELETE
    """
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT name FROM devices WHERE id = %s", (device_id,))
        device = cursor.fetchone()

        if device is None:
            return jsonify({"error": "Device not found."}), 404

        device_name = device[0]

        cursor.execute("DELETE FROM devices WHERE id = %s", (device_id,))
        connection.commit()

        cursor.execute(
                "INSERT INTO device_logs (device_id, action) VALUES (%s, %s)",
                (device_id, f"Deleted device '{device_name}'")
        )
        connection.commit()

        return jsonify({"message": "Device deleted successfully!"}), 200
    except Error as e:
        return jsonify(
            {
                "error": (
                    f"The error '{e}' occurred "
                    "while deleting the device."
                )
            }
        ), 500
    finally:
        cursor.close()
        connection.close()


def get_device_logs():
    """
    Fetches the logs of device actions from the database.

    Returns:
        JSON response with logs of device actions.
        An error message with status code 500 if the request fails.

    Methods:
        GET
    """
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM device_logs ORDER BY timestamp DESC;")
        logs = cursor.fetchall()
    except Error as e:
        return jsonify(
                {"error": f"The error '{e}' occurred while fetching logs."}
        ), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"logs": logs})
