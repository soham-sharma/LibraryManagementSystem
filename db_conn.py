import mysql.connector


def create_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="library",
    )
    return conn
