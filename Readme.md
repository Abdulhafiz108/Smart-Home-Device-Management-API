Smart Home Device Management API


OVERVIEW

The Smart Home Device Management API is a backend system for managing and simulating smart home devices. It provides functionality for adding, updating, deleting, and scheduling device actions, as well as simulating device events and logging activities. This API is built using Flask and integrates with a MySQL database.


FEATURES  
-Device Management: Add, update, delete, and retrieve smart home devices.  
-Scheduling: Schedule actions (e.g., turning devices on or off) at specific times.  
-Simulation: Simulate random device status changes (on/off).  
-Logging: Track device actions with time-stamped logs.  
-Error Handling: Comprehensive error handling for database operations, scheduling, and device updates.  


TECH STACK  
-Backend: Flask (Python)  
-Database: MySQL  
-Scheduling: APScheduler  
-Simulation: Threading for simulating device status changes  
-Logging: Device actions are logged in the database  
-Tools: Git, Git Bash  


API ENDPOINTS  
 Device Management  
 -GET /devices: Retrieve a list of all devices  
 -POST /devices: Add a new device  
 -PUT /devices/<id>: Update the status of a device  
 -DELETE /devices/<id>: Remove a device  
 -GET /devices/logs: Retrieve device logs  

 Scheduling  
 -POST /schedule: Schedule a device action at a specific time  
 -GET /schedule: Get all scheduled activities  
 
 Simulation  
 -POST /simulate: Run a simulation for all devices  
 -POST /simulate/<id>: Simulate a specific device’s status change  
 -POST /shutdown: Shut down the simulation  


INSTALLATION  
 Clone the repository:  
 -git clone https://github.com/your-username/Smart-Home-Device-Management-API.git  
 -cd Smart-Home-Device-Management-API  

 Set up your virtual environment and install dependencies:  
  -python -m venv venv  
  -source venv/bin/activate  # On Windows use `venv\Scripts\activate`  
  -pip install -r requirements.txt  

 Set up your MySQL database:  
  -CREATE DATABASE smart_home;  

 Update the db.py file with your MySQL database connection details.  

 Start the Flask app:  
  -flask run  


USAGE  
Below is a summary of available API endpoints:  

   - **GET `/api/devices`**: Retrieve a list of all devices.
   
     Example usage:
     ```bash
     curl -X GET http://127.0.0.1:5000/api/devices
     ```

   - **POST `/api/devices`**: Add a new device.
     
     Example usage:
     ```bash
     curl -X POST http://127.0.0.1:5000/api/devices \
     -H "Content-Type: application/json" \
     -d '{"name": "Living Room Light", "status": "Off"}'
     ```

   - **PUT `/api/devices/<device_id>`**: Update the status of a device.
     
     Example usage:
     ```bash
     curl -X PUT http://127.0.0.1:5000/api/devices/1 \
     -H "Content-Type: application/json" \
     -d '{"action": "On"}'
     ```

   - **DELETE `/api/devices/<device_id>`**: Delete a device.
     
     Example usage:
     ```bash
     curl -X DELETE http://127.0.0.1:5000/api/devices/1
     ```

   - **GET `/api/logs`**: Retrieve a list of all device logs.
     
     Example usage:
     ```bash
     curl -X GET http://127.0.0.1:5000/api/logs
     ```

   - **POST `/api/schedule`**: Schedule a device to perform an action at a specific time.
     
     Example usage:
     ```bash
     curl -X POST http://127.0.0.1:5000/api/schedule \
     -H "Content-Type: application/json" \
     -d '{"device_id": 1, "action": "On", "time": "2024-10-22 18:30:00"}'
     ```

   - **POST `/api/simulate`**: Run a simulation of all devices and update their status randomly.

     Example usage:
     ```bash
     curl -X POST http://127.0.0.1:5000/api/simulate
     ```

   - **POST `/api/shutdown`**: Stop any ongoing device simulations.

     Example usage:
     ```bash
     curl -X POST http://127.0.0.1:5000/api/shutdown
     ```

FUTURE ENHANCEMENTS  
-Implement user authentication for secure device management.  
-Add support for more device types and statuses.  
-Create a frontend dashboard for device monitoring and control.  


CONTRIBUTING  
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.  
