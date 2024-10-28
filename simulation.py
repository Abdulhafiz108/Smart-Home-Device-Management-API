import threading
import time
import random
from db import create_connection
from devices import update_device
from flask import jsonify

# Event for shutting down the simulation loop
shutdown_event = threading.Event()


def simulate_device_event(device_id):
    """
    Simulates a device event by randomly changing its status.
    Logs the status change in the database if it occurs.

    Args:
        device_id (int): The ID of the device to simulate.

    Returns:
        None
    """
    connection = create_connection()
    if connection is None:
        print("Database connection failed.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT status FROM devices WHERE id = %s", 
                       (device_id,))
        current_status = cursor.fetchone()[0]

        new_status = random.choice(['On', 'Off'])

        if new_status != current_status:
            cursor.execute(
                "UPDATE devices SET status = %s WHERE id = %s", 
                (new_status, device_id)
            )
            connection.commit()

            cursor.execute(
                "INSERT INTO device_logs (device_id, action) "
                "VALUES (%s, %s)", 
                (device_id, f"Simulated status change to {new_status}")
            )
            connection.commit()

            print(f"Simulated device {device_id} status change to {new_status}")

    except Exception as e:
        print(f"Error occurred during simulation: {str(e)}")
    
    finally:
        cursor.close()
        connection.close()


def simulate_all_devices():
    """
    Simulates events for all devices by randomly changing their statuses.

    Returns:
        None
    """
    connection = create_connection()
    if connection is None:
        print("Database connection failed.")
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM devices;")
        devices = cursor.fetchall()

        for device in devices:
            simulate_device_event(device['id'])

        print("Simulation completed successfully.")

    except Exception as e:
        print(f"Error occurred during device simulation: {str(e)}")

    finally:
        cursor.close()
        connection.close()


def run_simulation_interval():
    """
    Runs the simulation at a fixed interval, checking for shutdown events.

    Returns:
        None
    """
    simulation_interval = 15
    check_interval = 1
    elapsed_time = 0

    while not shutdown_event.is_set():
        if elapsed_time >= simulation_interval:
            simulate_all_devices()
            elapsed_time = 0

        time.sleep(check_interval)
        elapsed_time += check_interval


def simulate_devices():
    """
    Simulates all devices and returns a success message as a JSON response.

    Returns:
        (Response, int): A JSON response with a success message and status code
    """
    simulate_all_devices()
    return jsonify({
        "message": "Simulation completed successfully"
    }), 200


def shutdown():
    """
    Shuts down the simulation by setting the shutdown event.

    Returns:
        (Response, int): A JSON response with a shutdown message and status code
    """
    shutdown_event.set()
    return jsonify({
        "message": "Shutting down..."
    }), 200

# Uncomment to start the simulation automatically
# simulation_thread = threading.Thread(target=run_simulation_interval)
# simulation_thread.start()
