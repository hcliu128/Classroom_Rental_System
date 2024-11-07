import os
import mysql.connector
from mysql.connector import Error
import threading
import time


from dotenv import load_dotenv
load_dotenv('./.env')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_db = os.getenv('MYSQL_DB')
mysql_port = os.getenv('MYSQL_PORT')


print(f'MYSQL_USER: {mysql_user}')
print(f'MYSQL_PASSWORD: {mysql_password}')
print(f'MYSQL_HOST: {mysql_host}')
print(f'MYSQL_DB: {mysql_db}')
print(f'MYSQL_PORT: {mysql_port}')

class MySQLConnection:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.connection = None
        self._connect()

        # Start the thread to check and reconnect if needed
        self._reconnect_thread = threading.Thread(target=self._check_and_reconnect, daemon=True)
        self._reconnect_thread.start()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            self.connection.autocommit = True
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def _check_and_reconnect(self):
        while True:
            if self.connection:
                try:
                    self.connection.ping(reconnect=False, attempts=1, delay=0)
                except Error:
                    print("Connection lost, reconnecting...")
                    try:
                        self.connection.close()
                    except Error:
                        print("Failed to close the connection")
                    self._connect()
            else:
                self._connect()
            time.sleep(20)

    def __getattr__(self, name):
        # Delegate attribute access to the real connection object
        return getattr(self.connection, name)

    def get_one_data(self, query):
        if self.connection.is_connected():
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return cursor.fetchone()
        else: 
            print("Connection to MySQL DB failed")
    
    def get_all_data(self, query):
        if self.connection.is_connected():
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return cursor.fetchall()
        else: 
            print("Connection to MySQL DB failed")
        
    def execute_query(self, query):
        if self.connection.is_connected():
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        else: 
            print("Connection to MySQL DB failed")


connection = MySQLConnection(
    user=mysql_user,
    password=mysql_password,
    host=mysql_host,
    database=mysql_db,
    port=mysql_port
)


