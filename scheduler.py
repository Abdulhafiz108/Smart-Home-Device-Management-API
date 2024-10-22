from flask import jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from devices import update_device

# Initialize the background scheduler
scheduler = BackgroundScheduler()
scheduler.start()


def schedule_device_action():
    """
    Schedules a device action to be executed at a specific time.

    Input (JSON):
        - device_id: The ID of the device to be controlled (integer).
        - action: The action to perform (On/Off) (string).
        - time: The scheduled time for the action
          (string, format 'YYYY-MM-DD HH:MM:SS').

    Returns:
        - JSON response confirming the scheduling.
        - Error message with status code 400 or 500 in case of
          invalid input or failure.

    Methods:
        POST
    """
    try:
        data = request.get_json()

        # Extract necessary data from the request
        device_id = data.get('device_id')
        action = data.get('action')
        schedule_time = data.get('time')

        if not (device_id and action and schedule_time):
            return jsonify({
                "error": (
                    "Invalid data. "
                    "Make sure to include device_id, action, and time."
                )
            }), 400

        # Parse and schedule the action at the given time
        try:
            scheduled_time = datetime.strptime
            (schedule_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({
                "error": (
                    "Invalid time format. Use 'YYYY-MM-DD HH:MM:SS'."
                )
            }), 400

        job_id = f"device_{device_id}_action_{scheduled_time}"
        scheduler.add_job(
            update_device,
            'date',
            run_date=scheduled_time,
            args=[device_id, action],
            id=job_id
        )

        return jsonify({
            "message": (
                f"Device {device_id} scheduled to turn {action} "
                f"at {schedule_time}."
            )
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Scheduling failed: {str(e)}"
        }), 500


def get_scheduled_activities():
    """
    Fetches all scheduled device actions.

    Returns:
        - JSON response with a list of scheduled activities including job ID,
          next run time, and arguments.
        - Error message with status code 500 in case of failure.

    Methods:
        GET
    """
    try:
        jobs = scheduler.get_jobs()
        scheduled_activities = []

        for job in jobs:
            scheduled_activities.append({
                'id': job.id,
                'next_run_time': str(job.next_run_time),
                'args': job.args,
            })

        return jsonify({
            "scheduled_activities": scheduled_activities
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch scheduled activities: {str(e)}"
        }), 500
