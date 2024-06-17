import streamlit as st
import mysql.connector

from user_management import create_account

import base64
from pathlib import Path
from PIL import Image

from new_main import get_base64, set_background

st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
set_background(wallpaper)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
col2.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
col3.page_link("pages/kc.py", label="Competencias", icon="📚")
col4.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
col5.page_link("pages/new_login.py", label="Login", icon="🔒")
col6.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

st.title("Crear una cuenta nueva :new:")


# Connect to the MySQL database
connection = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="new_tfg"
)

# Create a cursor object to execute queries
cursor = connection.cursor()

# Fetch competences from the database
cursor.execute("SELECT id_kc, description FROM new_tfg.competences")
competences = cursor.fetchall()

col6, col7 = st.columns(2)

new_username = col6.text_input("**Usuario**")
new_password = col6.text_input("**Contraseña**", type="password")
repeat_password = col6.text_input("**Repetir Contraseña**", type="password")


selected_competences = col7.multiselect("**Selecciona tus competencias clave**:", [comp[1] for comp in competences])
keywords = col7.text_input("**Añade palabras clave (separadas por coma) para describir tus intereses**:")

if col7.button("Crear cuenta"):
    if create_account(new_username, new_password, repeat_password, selected_competences, keywords):
        pass
    else:
        st.error("¡Error en la creación de la cuenta! :warning: ")

