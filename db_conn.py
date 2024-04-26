import mysql.connector
import streamlit as st

# def create_conn():
#     conn = mysql.connector.connect(
#         host=st.secrets["database"]["host"],
#         user=st.secrets["database"]["user"],
#         password=st.secrets["database"]["password"],
#         database=st.secrets["database"]["database"],
#     )
#     return conn

def create_conn():
    conn = mysql.connector.connect(
        host= "localhost",
        user= "root",
        password= "1234",
        database=st.secrets["database"]["database"],
    )
    return conn