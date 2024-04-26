import mysql.connector
import streamlit as st

def create_conn():
    conn = mysql.connector.connect(
        host=st.secrets["database"]["host"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"],
    )
    return conn

# main for testing
if __name__ == "__main__":
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    print(books)
    conn.close()