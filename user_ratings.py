import streamlit as st
import pandas as pd

import mysql.connector

def get_user_ratings(username):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tfg"
    )
    cursor = conn.cursor(dictionary=True)

    # Query to fetch user's ratings with project titles
    query = """
        SELECT r.username, p.name AS project_title, r.rating
        FROM new_tfg.ratings r
        INNER JOIN new_tfg.projects_general p ON r.id_proj = p.id_proj
        WHERE r.username = %s
    """
    cursor.execute(query, (username,))
    user_ratings = cursor.fetchall()

    if user_ratings:
        # Display user's ratings
        col1, col2 = st.columns([2,1])
        col1.write("##### Proyecto :clipboard:")
        col2.write("##### Valoración :star:")
        ratings_df = pd.DataFrame(user_ratings)

        for row in ratings_df.iterrows():
            col1.write(f"- {row[1][1]}")
            col2.write(f"- {row[1][2]}")
        
        # Options to delete or edit ratings
        with st.expander("###### _Click aquí para ver acciones disponibles_"):
            col3, col4 = st.columns(2)
            rating_to_edit = col3.selectbox("**Selecciona una valoración a editar :pencil2:**", [rating['project_title'] for rating in user_ratings], key="edit_selection")
            new_rating = col3.selectbox("**Valoración :new:**", [1, 2, 3, 4, 5], key="new_rating_selection")
            
            stars = "" 
            for i in range (0, new_rating):
                stars += ":star:"
            st.write(stars)

            if col3.button("Editar valoración"):
                # Update rating in the database
                update_query = "UPDATE new_tfg.ratings SET rating = %s WHERE username = %s AND id_proj = (SELECT id_proj FROM new_tfg.projects_general WHERE name = %s)"
                cursor.execute(update_query, (new_rating, username, rating_to_edit))
                conn.commit()
                st.success("¡Valoración editada con éxito!")
                st.experimental_rerun()

            rating_to_delete = col4.selectbox("**Selecciona una valoración a eliminar :x:**", [rating['project_title'] for rating in user_ratings], key="delete_selection")
            if col4.button("Eliminar valoración"):
                # Delete rating from the database
                delete_query = "DELETE FROM new_tfg.ratings WHERE username = %s AND id_proj = (SELECT id_proj FROM new_tfg.projects_general WHERE name = %s)"
                cursor.execute(delete_query, (username, rating_to_delete))
                conn.commit()
                st.success("¡Valoración eliminada con éxito!")
                st.experimental_rerun()

    else:
        st.info(' ¡No has valorado ningún proyecto aún! :smile: ¡Para hacerlo, ves a la página "Valoración Nueva"!')

    conn.close()

def save_rating(username, project_name, rating):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
)
    cursor = conn.cursor()

    # Get project ID based on project name
    cursor.execute("SELECT id_proj FROM projects_general WHERE name = %s", (project_name,))
    project_id = cursor.fetchone()

    if project_id:
        # Insert new rating into ratings table
        insert_query = "INSERT INTO ratings (username, id_proj, rating) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, project_id[0], rating))
        conn.commit()
        conn.close()
        st.sidebar.success("¡Valoración guardada!")
    else:
        conn.close()
        st.warning("¡Proyecto no encontrado!")