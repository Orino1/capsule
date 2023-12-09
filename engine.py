"""
Database Engine Module

This module defines a basic DatabaseEngine class for interacting with
a MySQL database.

Usage:
-----------
Instantiate the DatabaseEngine class and use its methods to perform
database operations.

Example:
-----------
from database_engine import DatabaseEngine

# Instantiate the DatabaseEngine class
db = DatabaseEngine()

# Insert data into the database
insert_errors = db.insert(query, param)

# Query a single row from the database
result = db.queryOne(query, param)

# Insert user data into the database
user_insert_errors = db.insertUser(query, param)

"""


import os
import mysql.connector


class DatabaseEngine:
    """
    Simple DatabaseEngine Class
    """

    def __init__(self):
        """
        Initialize the DatabaseEngine instance.

        Environment Variables:
        -----------------------
        - DB_HOST: The database host address.
        - DB_PORT: The database port.
        - DB_USER: The database username.
        - DB_PASSWORD: The database password.
        - DB_DATABASE: The database name.
        """

        self.__host = os.getenv('DB_HOST')
        self.__port = int(os.getenv('DB_PORT'))
        self.__user = os.getenv('DB_USER')
        self.__password = os.getenv('DB_PASSWORD')
        self.__database = os.getenv('DB_DATABASE')

        self.__connection = mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database,
        )

    def insert(self, query, param):
        """
        Perform an insert operation on the database.

        Parameters:
        -----------
        query : str
            The SQL query for the insert operation.

        param : tuple
            The parameters for the SQL query.

        Returns:
        -----------
        errors : list
            List of error messages indicating issues with the database
            operation.
        """
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(query, param)
            self.__connection.commit()
            return []
        except:
            self.__connection.rollback()
            return ['An error occurred']
        finally:
            cursor.close()

    def queryOne(self, query, param):
        """
        Perform a single-row query operation on the database.

        Parameters:
        -----------
        query : str
            The SQL query for the query operation.

        param : tuple
            The parameters for the SQL query.

        Returns:
        -----------
        result : dict or list
            The result of the query or a list containing an error message.
        """
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(query, param)
            result = cursor.fetchone()
            return result
        except:
            self.__connection.rollback()
            return ['An error occurred']
        finally:
            cursor.close()

    def insertUser(self, query, param):
        """
        Perform an insert operation for user data on the database.

        Parameters:
        -----------
        query : str
            The SQL query for the insert operation.

        param : tuple
            The parameters for the SQL query.

        Returns:
        -----------
        errors : list
            List of error messages indicating issues with the database
            operation.
        """
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(query, param)
            self.__connection.commit()
            return []
        except mysql.connector.Error as err:
            self.__connection.rollback()
            if err.errno == 1062:
                return ['This email already exists']
            else:
                return ['An error occurred']
        finally:
            cursor.close()

    def tokenExists(self, token):
        """

        """
        query = "SELECT COUNT(*) FROM users WHERE token = %s"
        param = (token,)
        
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query, param)
            count = cursor.fetchone()[0]
            return True
        except:
            return False
        finally:
            cursor.close()

db = DatabaseEngine()
