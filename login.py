import streamlit as st
import pandas as pd
import hashlib

import mysql.connector

def authenticate_user(username, password):
    
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
)
    
    cursor = conn.cursor()

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Query to check if username and hashed password match any record in the users table
    query = "SELECT COUNT(*) FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, hashed_password))
    result = cursor.fetchone()[0]

    conn.close()

    # Return True if there is a match, False otherwise
    return result > 0


def logout():
    st.session_state.logged_in = False
    #st.switch_page("pages/recommender.py")
