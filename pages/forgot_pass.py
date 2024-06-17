import streamlit as st
import hashlib
import mysql.connector

import re

from login import logout

import base64
from pathlib import Path
from PIL import Image

from new_main import get_base64, set_background

import time

st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
set_background(wallpaper)

def forgot_password():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="new_tfg"
    )

    # Create a cursor object to execute queries
    cursor = connection.cursor()

    col1, col2 = st.columns([2,1])

    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'security_question' not in st.session_state:
        st.session_state.security_question = ""
    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        col1.caption(f"**Paso {st.session_state.step} de 4**")
        st.session_state.username = col1.text_input("Nombre de usuario")
        if st.button("Enviar nombre de usuario"):
            # Query to check if the username exists
            user_query = "SELECT id_sq FROM users WHERE username = %s"
            cursor.execute(user_query, (st.session_state.username,))
            user_data = cursor.fetchone()

            if user_data:
                # Query to get security question
                question_query = "SELECT question FROM security_questions WHERE id_sq = %s"
                cursor.execute(question_query, (user_data[0],))
                security_question = cursor.fetchone()

                if security_question:
                    st.session_state.security_question = security_question[0]
                    col1.success('¡Nombre de usuario enviado correctamente! :white_check_mark: Por favor, pulsa el botón "Siguiente"')
                    st.session_state.step = 2
                else:
                    col1.error("Esta cuenta no tiene establecida una pregunta de seguridad. ¡Lo sentimos, no podemos ayudarte! :pensive:")
            else:
                col1.error("¡Nombre de usuario no encontrado!")
        
        elif st.button("Cancelar operación"):
            col1.info("¡Operación de reestablecimiento de la contraseña cancelada!")
            st.session_state.step = 1
            return False

        st.button("Siguiente :arrow_forward:")

    elif st.session_state.step == 2:
        col1.caption(f"**Paso {st.session_state.step} de 4**")
        col1.write(st.session_state.security_question)
        st.session_state.security_answer = col1.text_input("Respuesta", type="password")
        if st.button("Enviar respuesta"):
            # Query to check if the security answer is correct
            answer_query = "SELECT COUNT(*) FROM users WHERE username = %s AND sec_ans = %s"
            cursor.execute(answer_query, (st.session_state.username, st.session_state.security_answer))
            answer_count = cursor.fetchone()[0]

            if answer_count > 0:
                col1.success('¡Pregunta de seguridad contestada correctamente! :white_check_mark: Por favor, pulsa el botón "Siguiente"')
                st.session_state.step = 3
            else:
                col1.error("¡Pregunta de seguridad contestada erróneamente!")
       
        elif st.button("Cancelar operación"):
            col1.info("¡Operación de reestablecimiento de la contraseña cancelada!")
            col1.info('¡Si vuelves a pulsar "Cancelar operación", volverás a la página inicial de reestablecimiento de contraseña :smile:!')
            st.session_state.step = 1
            return False
        
        st.button("Siguiente :arrow_forward:")

    elif st.session_state.step == 3:
        col1.caption(f"**Paso {st.session_state.step} de 4**")
        st.session_state.new_password = col1.text_input("Nueva contraseña", type="password")
        st.session_state.verify_password = col1.text_input("Repite la nueva contraseña", type="password")
        if st.button("Enviar contraseña"):
            # Check password pattern
            pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$")
            if pattern.match(st.session_state.new_password):
                if st.session_state.new_password == st.session_state.verify_password:
                    col1.success('¡Contraseña enviada correctamente! :white_check_mark: Por favor, pulsa el botón "Siguiente"')
                    hashed_password = hashlib.sha256(st.session_state.new_password.encode()).hexdigest()

                    # Update password in the database
                    update_query = "UPDATE users SET password = %s WHERE username = %s"
                    cursor.execute(update_query, (hashed_password, st.session_state.username))
                    connection.commit()

                    st.session_state.step = 4
                else:
                    col1.error("¡Contraseñas no coinciden!")
            else:
                col1.error("Error: ¡La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número, y tener al menos 6 carácteres!")
        
        elif st.button("Cancelar operación"):
            col1.info("¡Operación de reestablecimiento de la contraseña cancelada!")
            col1.info('¡Si vuelves a pulsar "Cancelar operación", volverás a la página inicial de reestablecimiento de contraseña :smile:!')
            st.session_state.step = 1
            return False

        st.button("Siguiente :arrow_forward:")

    elif st.session_state.step == 4:
        col1.caption(f"**Paso {st.session_state.step} de 4**")
        col1.success("¡Contraseña restablecida con éxito!")
        st.session_state.step = 1

    # Close cursor and connection
    cursor.close()
    connection.close()

    return True

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
col2.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
col3.page_link("pages/kc.py", label="Competencias", icon="📚")
col4.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
col5.page_link("pages/new_login.py", label="Login", icon="🔒")
col6.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

st.title("Reestablecer contraseña :key:")
logout()

placeholder = st.empty()
status = forgot_password()
#if status == False:
#    st.info ("¡Ya puedes cambiar de página!")
