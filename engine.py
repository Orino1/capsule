import os
import mysql.connector
from error import error

class DatabaseEngine:

    def __init__(self):
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

    def execute_query(self, query, param):
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query, param)
            self.__connection.commit()
            return True
        except:
            self.__connection.rollback()
            error.add_error('An error occurred')
            return False
        finally:
            cursor.close()

    def query_all(self, query, param):
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(query, param)
            result = cursor.fetchall()
            return True, result
        except:
            self.__connection.rollback()
            error.add_error('An error occurred')
            return False, None
        finally:
            cursor.close()

    def query_one(self, query, param):
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(query, param)
            result = cursor.fetchone()
            return True, result
        except:
            error.add_error('An error occurred')
            return False, None
        finally:
            cursor.close()

    def reset_token_exists(self, token):
        """

        """
        query = "SELECT * FROM users WHERE reset_password_token = %s"
        param = (token,)

        success, result = self.query_one(query, param)

        return success and result

    def email_exists(self, email):
        """
        """
        query = "SELECT * FROM users WHERE email = %s"
        param = (email,)

        success, result = self.query_one(query, param)

        return success and result

    def token_exists(self, token):
        """

        """
        query = "SELECT * FROM users WHERE verification_token = %s"
        param = (token,)
        
        success, result = self.query_one(query, param)

        return success and result

db = DatabaseEngine()
