import mysql.connector
import streamlit as st

# Create a global connection object
conn = None

def create_conn():
    global conn
    if conn is None:
        conn = mysql.connector.connect(
            host=st.secrets["database"]["host"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"],
        )
    return conn