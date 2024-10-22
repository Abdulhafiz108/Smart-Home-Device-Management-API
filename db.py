import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


def create_connection():
    """
    Establishes a connection to the MySQL database.

    Returns:
        A MySQL connection object if the connection is successful.
        None if the connection fails due to an error.

    Environment Variables:
        - DB_HOST: The hostname or IP address of the database server.
        - DB_USER: The username to authenticate with the database.
        - DB_PASSWORD: The password for the database user.
        - DB_NAME: The name of the database to connect to.

    Error Handling:
        - Catches connection errors and prints a detailed error message.
        - Ensures that any connection failure returns None\
        to avoid crashing the application.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "12345678"),
            database=os.getenv("DB_NAME", "smart_home")
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the database.")
        return None


def close_connection(connection):
    """
    Closes an existing MySQL database connection.

    Parameters:
        - connection: The active MySQL connection object.

    Returns:
        None

    Error Handling:
        - Ensures the connection is closed only if it exists.
        - Catches errors that may occur during closing process and logs them.
    """
    if connection is not None and connection.is_connected():
        try:
            connection.close()
            print("MySQL connection closed")
        except Error as e:
            print(
                f"error '{e}' occurred while closing the database connection."
            )
