import streamlit as st
import pandas as pd
from login import logout
from user_management import delete_account, change_password, change_username, manage_security_question, manage_kc_and_kw
from user_ratings import get_user_ratings, save_rating
from personalized_recommendations import recommendations_function

from streamlit_option_menu import option_menu

import mysql.connector

import base64
from pathlib import Path
from PIL import Image

import time

from new_main import get_base64, set_background

st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
set_background(wallpaper)

st.title(f"Bienvenid@, {st.session_state.username}! :wave: ")
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

col9.page_link(page="pages/about.py", label = "Logout :arrow_backward:")

selected = option_menu(
            menu_title=None,  # required
            options=["Mis Valoraciones", "Valoración Nueva", "Proyectos que te pueden interesar", "Ajustes"],  # required
            icons=["star", "star-half", "lightbulb", "gear"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )

if selected == "Mis Valoraciones":
    st.header("Mis Valoraciones :page_facing_up: ")
    get_user_ratings(st.session_state.username)

elif selected == "Valoración Nueva":
    st.header("Valoración Nueva :new:")

    # Connect to the MySQL database
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
    )

    # Create a cursor object to execute queries
    cursor = connection.cursor()

    # Query to fetch projects not rated by the user
    unrated_projects_query = """
        SELECT name 
        FROM new_tfg.projects_general 
        WHERE name NOT IN (
            SELECT p.name 
            FROM new_tfg.projects_general p
            INNER JOIN new_tfg.ratings r ON p.id_proj = r.id_proj
            WHERE r.username = %s
        )
    """
    cursor.execute(unrated_projects_query, (st.session_state.username,))
    unrated_projects = [row[0] for row in cursor.fetchall()]

    # Close cursor and connection
    cursor.close()
    connection.close()

    if unrated_projects:
        col21, col22 = st.columns([2,1])
        project_name = col21.selectbox("**Seleccionar un proyecto :mag_right:**", unrated_projects)
        rating = col21.selectbox("**Seleccionar valoración (1-5)**", [1, 2, 3, 4, 5])
        
        stars = "" 
        for i in range (0, rating):
            stars += ":star:"
        st.write(stars)

        if st.button("Guardar valoración"):
            # Function to save rating to the database
            save_rating(st.session_state.username, project_name, rating)
            st.success("¡Valoración guardada!")
            time.sleep(1)
            st.rerun()
    else:
        st.info('¡Ya has valorado todos los proyectos! :clap: ¡Si quieres editar alguna valoración, puedes ir a la página "Mis Valoraciones"!')

elif selected == "Proyectos que te pueden interesar":
    st.header("Proyectos que te pueden interesar")
    recommendations_function(st.session_state.username)


elif selected == "Ajustes":
    st.header("Ajustes :gear:")
    option = st.radio("Seleccionar opción", ["Cambiar contraseña :key:", "Cambiar nombre de usuario :bust_in_silhouette:", "Gestionar pregunta de seguridad :shield:", "Eliminar cuenta :x:", "Cambiar competencias y/o palabras clave :repeat:"])

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    if option == "Cambiar contraseña :key:":
        st.header("Ajustes de la Contraseña :key:")
        st.warning("_Después de realizar el cambio, serás redirigid@ a la página de login_")
        st.info("_Después de rellenar cada uno de los campos, pulsa enter_")
        
        old_password = st.text_input("**Contraseña actual**", type="password")
        new_password = st.text_input("**Contraseña nueva**", type="password")
        repeat_new_password = st.text_input("**Repetir contraseña nueva**", type="password")
        change_password(st.session_state.username, old_password, new_password, repeat_new_password)

    elif option == "Cambiar nombre de usuario :bust_in_silhouette:":
        st.header("Ajustes del Nombre de Usuario :bust_in_silhouette:")
        st.warning("_Después de realizar el cambio, serás redirigid@ a la página de login_")
        st.info("_Después de rellenar cada uno de los campos, pulsa enter_")
        
        old_username = st.text_input("**Nombre de usuario actual**")
        new_username = st.text_input("**Nombre de usuario nuevo**")
        
        if len(new_username) > 25 :
            st.error("Error: ¡El nombre de usuario puede tener máximo 25 carácteres, el que has introducido es demasiado largo!")
        
        else:

            change_username(old_username, new_username)

    elif option == "Eliminar cuenta :x:":
        st.header("Eliminar Cuenta :x:")
        if delete_account(st.session_state.username):
            st.switch_page("pages/about.py")

    elif option == "Gestionar pregunta de seguridad :shield:":
        st.header("Ajustes de la Pregunta de Seguridad :shield:")
        manage_security_question(st.session_state.username)
    
    elif option == "Cambiar competencias y/o palabras clave :repeat:":
        st.header("Cambiar Competencias y Palabras Clave :repeat:")
        manage_kc_and_kw(st.session_state.username)