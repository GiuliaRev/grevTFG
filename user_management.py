import streamlit as st
import mysql.connector
import hashlib
import re
from login import logout
import time


def create_account(username, password, repeat_password, selected_competences, keywords):

    if username.strip() == "" or password.strip() == "" or repeat_password.strip() == "" or not selected_competences or keywords.strip() == "":
        st.error("Error: ¡Todos los campos son obligatorios!")
        return False
    elif len(username) > 25:
        st.error("Error: ¡El nombre de usuario puede tener máximo 25 carácteres, el que has introducido es demasiado largo!")
    elif password != repeat_password:
        st.error("Error: ¡Las contraseñas no coinciden!")
        return False
    elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$", password):
        st.error("Error: ¡La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número, y tener al menos 6 carácteres!")
        return False
    else:
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="new_tfg"
        )
        cursor = conn.cursor()

        # Fetch competences from the database
        cursor.execute("SELECT id_kc, description FROM new_tfg.competences")
        competences = cursor.fetchall()
        #st.write("DB COMPETENCES", competences)

        # Check if username already exists
        query = "SELECT * FROM new_tfg.users WHERE username = %s"
        cursor.execute(query, (username,))
        if cursor.fetchone() is None:
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Insert new user into the database
            query = "INSERT INTO new_tfg.users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            conn.commit()

            # Insert competences for the user
            for comp_name in selected_competences:
                comp_id = [comp[0] for comp in competences if comp[1] == comp_name][0]
                #st.write("COMP ID:", comp_id)
                
                query = "INSERT INTO new_tfg.users_have_competences (username, id_kc) VALUES (%s, %s)"
                cursor.execute(query, (username, comp_id))
                conn.commit()

            # Split the keywords string into individual keywords
            keywords_list = [keyword.strip() for keyword in keywords.split(",")]

            # Insert keywords for the user
            for keyword in keywords_list:
                if len(keyword) > 50:
                    st.error(f"Error: ¡Una palabra clave puede tener máximo 50 carácteres, {keyword} es demasiado larga y no se almacenará!")
                else:
                    # Check if the keyword already exists for the user
                    query_check = "SELECT * FROM new_tfg.users_have_keywords WHERE username = %s AND keyword = %s"
                    cursor.execute(query_check, (username, keyword))
                    existing_keyword = cursor.fetchone()

                    # If the keyword doesn't exist, insert it
                    if not existing_keyword:
                        query_insert = "INSERT INTO new_tfg.users_have_keywords (username, keyword) VALUES (%s, %s)"
                        cursor.execute(query_insert, (username, keyword))
                        conn.commit()

            conn.close()

            st.success("¡Cuenta creada con éxito! :white_check_mark: ¡Ya puedes hacer log in!")
            return True
        else:
            conn.close()
            st.error("Error: ¡Nombre de usuario ya existe!")
            return False

def change_password(username, old_password, new_password, repeat_new_password):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"  
    )
    cursor = conn.cursor()

    # Check if the old password matches
    query = "SELECT password FROM new_tfg.users WHERE username = %s"
    cursor.execute(query, (username,))
    stored_password = cursor.fetchone()
    if not old_password or not new_password or not repeat_new_password:
        st.error ("¡Todos los campos son obligatorios!")
    if stored_password and stored_password[0] == hashlib.sha256(old_password.encode()).hexdigest():
        # Check if new passwords match
        if new_password == repeat_new_password:
            # Check if the new password meets the complexity requirements
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$", new_password):
                st.error("Error: ¡La contraseña nueva debe contener al menos una letra mayúscula, una letra minúscula, un número, y tener al menos 6 carácteres!")
                return False

            # Update the password
            if st.button("Guardar cambios"):
                hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
                query = "UPDATE new_tfg.users SET password = %s WHERE username = %s"
                cursor.execute(query, (hashed_new_password, username))
                conn.commit()
                conn.close()
                st.success("¡Contraseña cambiada con éxito! ...Redirigiendo...")
                time.sleep(3)
                logout()
                st.switch_page("pages/new_login.py")
                return True
        else:
            conn.close()
            st.error("Error: ¡Contraseñas nuevas no coinciden!")
    else:
        conn.close()
        st.error("Error: ¡Contraseña actual no coincide!")
    
def change_username(old_username, new_username):
    if not old_username or not new_username:
        st.error("¡El nombre de usuario actual y el nuevo son obligatorios!")
        return False
    if old_username == new_username:
        st.error("Error: ¡Nombre de usuario nuevo debe ser distinto al actual!")
        return False
    if old_username != st.session_state.username:
        st.error("Error: ¡Nombre de usuario actual no coincide!")
        return False
    if len(new_username) > 25:
        st.error("¡El nombre de usuario puede tener máximo 25 carácteres, el que has introducido es demasiado largo!")
        return False

    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"  
    )
    cursor = conn.cursor()

    # Check if the new username is already taken
    query = "SELECT * FROM new_tfg.users WHERE username = %s"
    cursor.execute(query, (new_username,))
    if cursor.fetchone() is not None:
        conn.close()
        st.error("Error: ¡Nombre de usuario nuevo ya existe!")
        return False

    if st.button("Guardar cambios"):
        # Update username
        query = "UPDATE new_tfg.users SET username = %s WHERE username = %s"
        cursor.execute(query, (new_username, old_username))
        conn.commit()
        conn.close()

        st.success("¡Nombre de usuario cambiado con éxito! ...Redirigiendo...")
        time.sleep(3)
        logout()
        st.switch_page("pages/new_login.py")
        return True

def delete_account(username):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
    )
    cursor = conn.cursor()
    
    # Check if the user exists
    query = "SELECT * FROM new_tfg.users WHERE username = %s"
    cursor.execute(query, (username,))
    if cursor.fetchone() is not None:
        st.info('Después de eliminar la cuenta, serás redirigid@ a la página "Sobre el Proyecto"')
        st.write("#### ¿Estás segur@ que quieres eliminar tu cuenta?")
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button("Si, eliminar mi cuenta :white_check_mark:"):
            # Delete the user's account
            query = "DELETE FROM new_tfg.users WHERE username = %s"
            cursor.execute(query, (username,))
            conn.commit()
            conn.close()
            st.success("¡Tu cuenta ha sido eliminada!")
            time.sleep(3)
            return True
        else:
            if col2.button("No, no eliminar mi cuenta :x:"):
                st.info("Eliminación de la cuenta cancelada")
                conn.close()
    else:
        conn.close()
        return False  # User not found

def manage_security_question(username):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
)
    cursor = conn.cursor()

    # Fetch security questions from the database
    query = "SELECT id_sq, question FROM new_tfg.security_questions"
    cursor.execute(query)
    security_questions = cursor.fetchall()
    question_options = [question[1] for question in security_questions]

    user_question_query = "SELECT id_sq FROM new_tfg.users WHERE username = %s"
    cursor.execute(user_question_query, (username,))
    user_question = cursor.fetchall()

    if st.checkbox("Establecer pregunta de seguridad"):

        if user_question[0][0]: 
            st.info("¡Ya has establecido una pregunta de seguridad! Si la quieres editar, ves al apartado **Cambiar pregunta o respuesta de seguridad**")
        
        else:

            security_question = st.selectbox("**Selecionar pregunta de seguridad**", options=question_options)
            security_answer = st.text_input("**Respuesta a la pregunta de seguridad**", type="password")
            repeat_security_answer = st.text_input("Repite la respuesta", type="password")


            if st.button("Guardar"):
                # Find the id_sq for the selected question
                selected_question_id = None
                for question in security_questions:
                    if question[1] == security_question:
                        selected_question_id = question[0]
                        break

                if selected_question_id is not None:
                    if len(security_answer) > 50 or len(repeat_security_answer) > 50:
                        st.error(f"Error: ¡La respuesta de seguridad puede tener máximo 50 carácteres, la que has introducido es demasiado larga!")
                    
                    else:

                        if security_answer == repeat_security_answer:
                            query = "UPDATE new_tfg.users SET id_sq = %s, sec_ans = %s WHERE username = %s"
                            cursor.execute(query, (selected_question_id, security_answer, username))
                            conn.commit()
                            conn.close()
                            st.success("¡Pregunta y respuesta de seguridad guardadas con éxito!")
                        else:
                            conn.close()
                            st.error("Error: ¡Respuestas no coinciden!")
                else:
                    conn.close()
                    st.error("Error: ¡Pregunta seleccionada no válida!")

    elif st.checkbox("Cambiar pregunta o respuesta de seguridad"):
        st.write("---")
        col31, col32 = st.columns(2)

        current_security_question = col31.selectbox("**Selecciona la pregunta de seguridad actual**", options=question_options, index=0, key="current_sec_ques")
        current_security_answer = col31.text_input("**Respuesta actual a la pregunta de seguridad**", type="password")
        
        new_security_question = col32.selectbox("**Selecciona la nueva pregunta de seguridad**", options=question_options, index=0, key="new_sec_ques")
        new_security_answer = col32.text_input("**Respuesta nueva a la pregunta de seguridad**", type="password")
        repeat_new_security_answer = col32.text_input("**Repite la respuesta nueva**", type="password")

        if col32.button("Guardar cambios"):
            # Find the id_sq for the current and new questions
            current_question_id = None
            new_question_id = None
            for question in security_questions:
                if question[1] == current_security_question:
                    current_question_id = question[0]
                if question[1] == new_security_question:
                    new_question_id = question[0]

            query = "SELECT id_sq, sec_ans FROM new_tfg.users WHERE username = %s"
            cursor.execute(query, (username,))
            current_sec_q_ans = cursor.fetchone()

            if current_sec_q_ans[0] == current_question_id:
                if current_sec_q_ans[1] == current_security_answer:
                    if len(new_security_answer) > 50 or len(repeat_new_security_answer) > 50:
                        st.error(f"Error: ¡La respuesta de seguridad puede tener máximo 50 carácteres, la que has introducido es demasiado larga!")
                    
                    elif new_security_answer == repeat_new_security_answer:
                        query = "UPDATE new_tfg.users SET id_sq = %s, sec_ans = %s WHERE username = %s"
                        cursor.execute(query, (new_question_id, new_security_answer, username))
                        conn.commit()
                        conn.close()
                        st.success("¡Pregunta y respuesta de seguridad guardadas con éxito!")
                    else:
                        conn.close()
                        st.error("Error: ¡Respuestas nuevas no coinciden!")
                else:
                    conn.close()
                    st.error("Error: ¡Respuesta actual incorrecta!")
            else:
                conn.close()
                st.error("Error: ¡Pregunta actual incorrecta!")

def manage_kc_and_kw(username):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
    )
    cursor = conn.cursor()

    # Fetch competences from the database
    cursor.execute("SELECT id_kc, description, short_kc FROM new_tfg.competences")
    competences = cursor.fetchall()

    # Fetch user's competences
    cursor.execute("SELECT u.username, c.id_kc, c.description, c.short_kc FROM new_tfg.users_have_competences u INNER JOIN new_tfg.competences c ON u.id_kc = c.id_kc WHERE username = %s", (username,))
    user_competences = cursor.fetchall()
    user_competences_ids = [comp[1] for comp in user_competences]

    # Fetch user's keywords
    cursor.execute("SELECT keyword FROM new_tfg.users_have_keywords WHERE username = %s", (username,))
    user_keywords = cursor.fetchall()
    user_keywords = [kw[0] for kw in user_keywords]
    current_keywords = ", ".join(user_keywords)

    # Display current competences
    st.subheader("Competencias actuales")
    current_competences = [comp[1] for comp in competences if comp[0] in user_competences_ids]

    for competence in user_competences:
        st.write (f" - {competence[2]} :arrow_right:**{competence[3]}**")

    #for id in user_competences_ids:


    # Display current keywords
    st.subheader("Palabras clave actuales")
    st.write(f"**{current_keywords}**")
    col11, col12 = st.columns(2)

    if col11.checkbox("Cambiar competencias"):
        selected_competences = col11.multiselect("**Seleccionar competencias**", options= [comp[1] for comp in competences], default=current_competences)


        if col11.button("Guardar competencias"):

            if not selected_competences:
                col11.error("¡Debes seleccionar al menos una competencia!")
    
            else:
        
                # Delete existing user's competences
                cursor.execute("DELETE FROM new_tfg.users_have_competences WHERE username = %s", (username,))
                conn.commit()

                # Insert new competences
                for comp_name in selected_competences:
                    comp_id = [comp[0] for comp in competences if comp[1] == comp_name][0]
                    cursor.execute("INSERT INTO new_tfg.users_have_competences (username, id_kc) VALUES (%s, %s)", (username, comp_id))
                conn.commit()
                conn.close()
                st.success("¡Competencias actualizadas con éxito!")
                st.experimental_rerun()

    if col12.checkbox("Cambiar palabras clave"):
        col12.info("Tus palabras clave actuales serán reemplazadas por las nuevamente introducidas")
        keywords_input = col12.text_input("**Ingresar palabras clave (separadas por comas)**", value=current_keywords)


        if col12.button("Guardar palabras clave"):

            if not keywords_input:
                col12.error("¡Debes introducir al menos una palabra clave!")
    
            else:

                # Delete existing user's keywords
                cursor.execute("DELETE FROM new_tfg.users_have_keywords WHERE username = %s", (username,))
                conn.commit()

                # Insert new keywords
                for keyword in keywords_input.split(","):
                    if len(keyword) > 50:
                        st.error(f"Error: ¡Una palabra clave puede tener máximo 50 carácteres, {keyword} es demasiado larga y no se almacenará!")
                    else:
                        cursor.execute("INSERT INTO new_tfg.users_have_keywords (username, keyword) VALUES (%s, %s)", (username, keyword.strip()))
                conn.commit()
                conn.close()
                st.success("¡Palabras clave actualizadas con éxito!")
                st.experimental_rerun()
