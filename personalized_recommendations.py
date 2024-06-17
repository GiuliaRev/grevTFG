import streamlit as st
import pandas as pd
import mysql.connector
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download stopwords
nltk.download('stopwords')

# Function to process text
def build_terms(line): 
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("spanish"))
    line = line.lower()  
    line = line.split()  
    line = [x for x in line if x not in stop_words]  
    line = [x for x in line if x.startswith(("@", "https://", "$", '#')) != True]  
    line = [re.sub('[^a-záéíóúäëïöü]+', '', x) for x in line]
    line = [re.sub('[“”]', '', x) for x in line]  # Remove “ and ” characters using re.sub
    line = [stemmer.stem(word) for word in line] 
    return  line

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
)

def fetch_mean_rating(project_id):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="new_tfg"
    )

    # Define the query to fetch the mean rating and count of ratings of the project
    query = """
    SELECT AVG(rating) AS mean_rating, COUNT(*) AS rating_count
    FROM new_tfg.ratings r
    JOIN new_tfg.projects_general pg ON r.id_proj = pg.id_proj
    WHERE pg.name = %s
    """

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query, (project_id,))
    result = cursor.fetchone()
    cursor.close()

    # Close the database connection
    conn.close()

    # Check if there is a result
    if result[0] is not None:
        return result[0], result[1]  # Return mean rating and count of ratings
    else:
        return 0, 0  # Return 0 if there is no rating for the project

def recommendations_function(username):

    # MySQL connection to fetch project data
    com_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="new_tfg"
    )

    # Query to fetch project data
    project_query = """
    SELECT 
        pg.name, pg.link, pg.scope , pd.description, 
        pgls.goal, pfd.full_desc , pg.cs_web_name , pg.cs_web_link
    FROM 
        new_tfg.projects_general pg
    JOIN 
        new_tfg.projects_descriptions pd ON pg.id_proj = pd.id_proj
    JOIN 
        new_tfg.projects_goals pgls ON pg.id_proj = pgls.id_proj
    JOIN 
        new_tfg.projects_full_descriptions pfd ON pg.id_proj = pfd.id_proj
    """


    cursor_com = com_conn.cursor()
    cursor_com.execute(project_query)
    projects_full_info = cursor_com.fetchall()

    comdf = pd.DataFrame(projects_full_info, columns=['Name', 'Link', 'Scope', 'Description', 'Goal', 'Full Description', 'CS Web Name', 'CS Web Link'])


    # Initialize an empty list to store filtered rows
    filtered_rows = []

    # Define scopes for filtering
    life_science = ['Medicina y Salud', 'Biodiversidad', 'salud', 'ambiental', 'Ecología y Medioambiente', 'Ciencias de la Agricultura y Veterinaria', 'Naturaleza y Aire Libre', 'Ciencia de los Alimentos', 'Animales', 'Pájaros', 'Marino y Terrestre', 'Biogeografía', 'Insectos y Polinizadores', 'Biología', 'Seguimiento de Especies a largo plazo']
    physics_science = ['Océanos', 'Agua', 'Física', 'Espacio y Astronomía', 'Clima y Meteorología', 'Gestión de Recursos Naturales', 'Geología y Ciencias de la Tierra', 'Ciencias Químicas', 'Geografía']
    social_science = ['Cultura y Arqueología', 'Ciencias Sociales', 'Educación', 'social', 'Ciencias Políticas', 'Culturas Indígenas']
    tech = ['Informática y Ciencias de la Computación', 'Transporte', 'Sonido']

    scopes = ['Ciencias de la Vida y Biomedicina', 'Ciencias Físicas', 'Ciencias Sociales', 'Tecnología']
    selected_scopes = st.multiselect("""###### :books: **Ámbitos**""", scopes, scopes)

    # Combine all individual scopes lists into one dictionary for easier lookup
    all_scopes = {
        'Ciencias de la Vida y Biomedicina': life_science,
        'Ciencias Físicas': physics_science,
        'Ciencias Sociales': social_science,
        'Tecnología': tech
    }

    if not selected_scopes:
        st.error("¡Por favor selecciona al menos un ámbito!")
    else:
            
        # Query to fetch competences associated with a specific user
            competences_query = """
            SELECT c.short_kc 
            FROM new_tfg.competences c
            JOIN new_tfg.users_have_competences uc ON c.id_kc = uc.id_kc
            WHERE uc.username = %s
            """

            # Query to fetch keywords associated with a specific user
            keywords_query = """
            SELECT uk.keyword 
            FROM new_tfg.users_have_keywords uk
            WHERE uk.username = %s
            """
            
            # Execute key competences query
            cursor = com_conn.cursor()
            cursor.execute(competences_query, (username,))
            competences_data = cursor.fetchall()
            cursor.close()

            # Execute keywords query
            cursor = com_conn.cursor()
            cursor.execute(keywords_query, (username,))
            keywords_data = cursor.fetchall()
            cursor.close()

            # Create DataFrame for competences data
            competences_df = pd.DataFrame(competences_data, columns=['Competence'])

            # Create DataFrame for keywords data
            keywords_df = pd.DataFrame(keywords_data, columns=['Keyword'])

            col1, col2 = st.columns(2)

            filtered_rows = []

            # Iterate over each row in the DataFrame
            for index, row in comdf.iterrows():
                # Check if any selected scope is present in the project scopes
                for selected_scope in selected_scopes:
                    if any(scope in row['Scope'] for scope in all_scopes[selected_scope]):
                        # Add the row to the filtered list and break the loop to avoid duplicates
                        filtered_rows.append(row)
                        break

            # Create a new DataFrame with the filtered rows
            filtered_df = pd.DataFrame(filtered_rows)

            # Drop duplicates based on all columns
            filtered_df = filtered_df.drop_duplicates()

            # Create a copy of filtered DataFrame
            clean_df = filtered_df.copy()


            # Replace only the cells with spaces or empty strings with NaN
            clean_df['Description'].replace(r'^\s*$', np.nan, regex=True, inplace=True)

            # Fill the NaN values with the desired message
            clean_df['Description'] = clean_df['Description'].fillna(' _Lo sentimos, este proyecto no tiene una descripción en nuestra base de datos. Para más información puedes consultar el enlace de abajo._')

            # Apply build_terms on full_desc column of clean_df
            clean_df['Full Description'] = clean_df['Full Description'].apply(build_terms)


            # Display recommendations based on user input
            if col1.checkbox("**Mostrar recomendaciones para competencias**"):

                for index, row in competences_df.iterrows():

                    shortcomp = row['Competence']

                    # Apply build_terms to it
                    shortcomp_terms = build_terms(shortcomp)

                    # Text embeddings
                    
                    vectorizer = TfidfVectorizer()
                    text_embeddings = vectorizer.fit_transform(clean_df['Full Description'].apply(' '.join))

                    # Input embeddings
                    input_embeddings = vectorizer.transform(shortcomp_terms)

                    # Similarities between embeddings
                    similarities = cosine_similarity(text_embeddings, input_embeddings)
                    
                    # Get top project ids
                    top_project_ids = similarities.argsort(axis=0)[-1:][::-1]


                    top_projects = clean_df.iloc[top_project_ids.flatten()]
                    
                    col1.write(f"##### Para competencia: {shortcomp}")
                
                    # Fetch mean ratings for the top projects and add them to the DataFrame
                    mean_ratings = []
                    rating_counts = []

                    for project_name in top_projects['Name']:
                        mean_rating, rating_count = fetch_mean_rating(project_name)
                        mean_ratings.append(mean_rating)
                        rating_counts.append(rating_count)

                    top_projects['Mean Rating'] = mean_ratings
                    top_projects['Rating Count'] = rating_counts
                    col1.write("###### TOP PROYECTOS:")
                    top_projects.sort_values(by='Mean Rating', ascending=False)

                    for _, project in top_projects.iterrows():
                        col1.write(f":clipboard: **Nombre:** {project['Name']}")
                        col1.write(f":speech_balloon: **Descripción:** {project['Description']}")
                        col1.write(f":link: **Link:** [{project['Link']}]({project['Link']})")
                        col1.write(f":dart: **Ámbito(s):** {project['Scope']}")
                        col1.write(f":star:**Mean Rating:** {project['Mean Rating']} ({project['Rating Count']} valoraciones)")
                        col1.write("---")

            if col2.checkbox("**Mostrar recomendaciones para palabras clave**"):

                for index, row in keywords_df.iterrows():

                    kw = row['Keyword']

                    # Apply build_terms to it
                    kw_terms = build_terms(kw)

                    # Text embeddings
                    vectorizer = TfidfVectorizer()
                    text_embeddings = vectorizer.fit_transform(clean_df['Full Description'].apply(' '.join))

                    # Input embeddings
                    input_embeddings = vectorizer.transform(kw_terms)

                    # Similarities between embeddings
                    similarities = cosine_similarity(text_embeddings, input_embeddings)

                    # Get top project ids
                    top_project_ids = similarities.argsort(axis=0)[-2:][::-1]

                    # Put those projects in a dataframe and sort them based on mean rating
                    top_projects = clean_df.iloc[top_project_ids.flatten()]

                    col2.write(f"##### Para palabra clave: {kw}")
                    #st.dataframe(top_projects)

                    # Fetch mean ratings for the top projects and add them to the DataFrame
                    mean_ratings = []
                    rating_counts = []

                    for project_name in top_projects['Name']:
                        mean_rating, rating_count = fetch_mean_rating(project_name)
                        mean_ratings.append(mean_rating)
                        rating_counts.append(rating_count)

                    top_projects['Mean Rating'] = mean_ratings
                    top_projects['Rating Count'] = rating_counts
                    col2.write("###### TOP PROYECTOS:")
                    top_projects.sort_values(by='Mean Rating', ascending=False)

                    for _, project in top_projects.iterrows():
                        col2.write(f":clipboard: **Nombre:** {project['Name']}")
                        col2.write(f":speech_balloon: **Descripción:** {project['Description']}")
                        col2.write(f":link: **Link:** [{project['Link']}]({project['Link']})")
                        col2.write(f":dart: **Ámbito(s):** {project['Scope']}")
                        col2.write(f":star:**Mean Rating:** {project['Mean Rating']} ({project['Rating Count']} valoraciones)")
                        col2.write("---")

