import socket, ssl
from threading import Thread
import sqlite3 as sql

# Initialize the SQL Server Client
# |--> The SQL Server Client is going to allow us to store the results of the analysis
# |--> We are going to use SQLite as our SQL Server Client
# |--> We are going to use a SQLite database to store the results

class SQLServerClient(Thread):
    def __init__(self):
        super(Thread, self).__init__()
        self.connection = sql.connect('results.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, content TEXT, entities TEXT)')
        self.connection.commit()