from flask import Flask
from devices import get_devices, add_device
from devices import update_device_now, delete_device, get_device_logs
from scheduler import schedule_device_action, get_scheduled_activities
from simulation import simulate_devices, shutdown, shutdown_event

app = Flask(__name__)


@app.route('/')
def home():
    """
    Root route that returns a success message.

    Returns:
        A JSON response with a message confirming the server is running.

    Methods:
        GET
    """
    try:
        return 'Congratulations! Flask is running successfully.'
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/devices', methods=['GET'])
def api_get_devices():
    """
    Route to get the list of all devices.

    Returns:
        JSON response with a list of devices.
        Error message with status code 500 if the request fails.

    Methods:
        GET
    """
    try:
        return get_devices()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/devices', methods=['POST'])
def api_add_device():
    """
    Route to add a new device.

    Input (JSON):
        - name: The name of the device (string).
        - status: The status of the device (On/Off) (string).

    Returns:
        JSON response with a success message if the device is added.
        Error message with status code 500 if the request fails.

    Methods:
        POST
    """
    try:
        return add_device()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def api_update_device(device_id):
    """
    Route to update the status of a device.

    Input (JSON):
        - action: The new status of the device (On/Off) (string).

    Path Parameters:
        - device_id: ID of the device to update.

    Returns:
        JSON response with a success message if the device is updated.
        Error message with status code 500 if the request fails.

    Methods:
        PUT
    """
    try:
        return update_device_now(device_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def api_delete_device(device_id):
    """
    Route to delete a device.

    Path Parameters:
        - device_id: ID of the device to delete.

    Returns:
        JSON response confirming the device deletion.
        Error message with status code 500 if the request fails.

    Methods:
        DELETE
    """
    try:
        return delete_device(device_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/device_logs', methods=['GET'])
def api_get_device_logs():
    """
    Route to fetch device logs.

    Returns:
        JSON response with logs of device actions.
        Error message with status code 500 if the request fails.

    Methods:
        GET
    """
    try:
        return get_device_logs()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/schedule', methods=['POST'])
def api_schedule_device_action():
    """
    Route to schedule an action for a device.

    Input (JSON):
        - device_id: ID of the device (integer).
        - action: Action to schedule (On/Off) (string).
        - time: Time to schedule the action (string, format HH:MM).

    Returns:
        JSON response confirming the action scheduling.
        Error message with status code 500 if the request fails.

    Methods:
        POST
    """
    try:
        return schedule_device_action()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/scheduled', methods=['GET'])
def api_get_scheduled_activities():
    """
    Route to get all scheduled device actions.

    Returns:
        JSON response with the list of scheduled activities.
        Error message with status code 500 if the request fails.

    Methods:
        GET
    """
    try:
        return get_scheduled_activities()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/simulate', methods=['POST'])
def api_simulate_devices():
    """
    Route to manually trigger device simulation.

    Returns:
        JSON response confirming the simulation was successful.
        Error message with status code 500 if the request fails.

    Methods:
        POST
    """
    try:
        return simulate_devices()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/shutdown', methods=['POST'])
def api_shutdown():
    """
    Route to gracefully shut down the simulation.

    Returns:
        JSON response confirming the shutdown was successful.
        Error message with status code 500 if the request fails.

    Methods:
        POST
    """
    try:
        return shutdown()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return shutdown()


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    finally:
        shutdown_event.set()
