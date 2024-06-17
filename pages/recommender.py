import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot
import nltk
nltk.download('stopwords') #Dowload list of stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re #Library used to remove certain symbols / characters from a text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
from pathlib import Path

import base64
from PIL import Image

from new_main import get_base64, set_background

st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

import numpy as np


def load_data(filename):
    data = pd.read_csv(filename, sep=",")
    data = data.drop_duplicates(subset=['Project Name'], keep = 'first')
    data = data.rename(columns={'Project Name': 'Nombre del Proyecto', 'Project Link': 'Link del Proyecto', 'Project Scope': 'Ámbitos del Proyecto', 'Project Description': 'Descripción del Proyecto', 'Project Goal': 'Objetivo del Proyecto', 'Citizen Science Web Name': 'Nombre de la Plataforma de Ciencia Ciudadana', 'Citizen Science Web Link': 'Link de la Plataforma'})
    return data

projectsCS = load_data(Path(__file__).parents[0]/"CS_Projects.csv")

def barcelona_proj(web):
    if str(web) == 'Ciencia Ciudadana Ayuntamiento de Barcelona':
        return 'Oficina de la Ciència Ciutadana'
    return str(web)


life_science = ['Medicina y Salud', 'Biodiversidad', 'salud', 'ambiental', 'Ecología y Medioambiente', 'Ciencias de la Agricultura y Veterinaria', 'Naturaleza y Aire Libre', 'Ciencia de los Alimentos', 'Animales', 'Pájaros', 'Marino y Terrestre', 'Biogeografía', 'Insectos y Polinizadores', 'Biología', 'Seguimiento de Especies a largo plazo']
physics_science = ['Océanos', 'Agua', 'Física', 'Espacio y Astronomía', 'Clima y Meteorología', 'Gestión de Recursos Naturales', 'Geología y Ciencias de la Tierra', 'Ciencias Químicas', 'Geografía']
social_science = ['Cultura y Arqueología', 'Ciencias Sociales', 'Educación', 'social', 'Ciencias Políticas', 'Culturas Indígenas']
tech = ['Informática y Ciencias de la Computación', 'Transporte', 'Sonido']
def scope_categories(proj_scope, categories = []):
    proj_scopes = str(proj_scope).replace('.', '').split(', ')
    for sco in proj_scopes:
        if sco in life_science:
            categories.append('Ciencias de la Vida y Biomedicina')
        elif sco in physics_science:
            categories.append('Ciencias Físicas')
        elif sco in social_science:
            categories.append('Ciencias Sociales')
        else:
            categories.append('Tecnología')
        return list(set(categories))
    

projectsCS['Nombre de la Plataforma de Ciencia Ciudadana'] = projectsCS.apply(lambda row: barcelona_proj(row['Nombre de la Plataforma de Ciencia Ciudadana']), axis=1)
projectsCS['Ámbitos del Proyecto'] = projectsCS.apply(lambda row: scope_categories(row['Ámbitos del Proyecto']), axis=1)


def scope_in_project(proj_sco, scope):
    if str(scope) in str(proj_sco):
        return str(scope)
    return str(proj_sco)


#This function receives a line of text as input and returns a list of the words contained in it after having removed the stopwords and non-important symbols, 
#transforming to lowercase, tokenizing and stemming.
def build_terms(line): 
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("spanish"))
    line = line.lower()  #Convert to lowercase
    line = line.split()  # Tokenize the text to get a list of terms
    line = [x for x in line if x not in stop_words]  # eliminate the stopwords
    line = [x for x in line if x.startswith(("@", "https://", "$", '#')) != True]  # eliminate non-important symbols
    line = [re.sub('[^a-záéíóúäëïöü]+', '', x) for x in line] # since it's in spanish we only have to worry about 'closed' accents
    line = [stemmer.stem(word) for word in line] # perform stemming
    return line


def select_max_rec(df):
    if len(df)<=10:
        return 1
    elif len(df)<=20:
        return 2
    elif len(df)<=30:
        return 3
    elif len(df)<=40:
        return 5
    return 7


def create_wordcloud(df, idxs):
    top_idx_desc = []
    for idx in idxs:
        top_idx_desc.append(', '.join(build_terms(df['Project Full Description'].iloc[idx])))
    return top_idx_desc


# def search_project(name, search):
#     if str(search).lower() in str(name).lower:
#         return 'YES'
#     return ''



def show_characteristics_page():

    wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
    set_background(wallpaper)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
    col2.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
    col3.page_link("pages/kc.py", label="Competencias", icon="📚")
    col4.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
    col5.page_link("pages/new_login.py", label="Login", icon="🔒")
    col6.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

    st.title("Sistema de Recomendación de Proyectos de Ciencia Ciudadana Basados en el Currículum de Primaria de Cataluña")

    st.write("""### Este es el dataset de proyectos de Ciencia Ciudadana""")
    st.write(""" :globe_with_meridians: Los proyectos pertenecen a las plataformas "Observatorio de la Ciencia Ciudadana en España" y "Oficina de la Ciència Ciutadana". """)
    st.write(""" Filtrar por:""")
    filteredCS = projectsCS.copy()
    
    scopes = ['Ciencias de la Vida y Biomedicina', 'Ciencias Físicas', 'Ciencias Sociales', 'Tecnología']
    scope = st.multiselect("""###### :books: **Ámbitos**""", scopes, scopes)
    # st.write('Los ámbitos mencionados incluyen las siguientes categorías relacionadas con la ciencia:')
    st.write(':seedling: **Ciencias de la Vida y Biomedicina**: Medicina y Salud, Biodiversidad, salud, ambiental, Ecología y Medioambiente, Ciencias de la Agricultura y Veterinaria, Naturaleza y Aire Libre, Ciencia de los Alimentos, Animales, Pájaros, Marino y Terrestre, Biogeografía, Insectos y Polinizadores, Biología, y Seguimiento de Especies a largo plazo.')
    st.write(':test_tube: **Ciencias Físicas**: Océanos, Agua, Física, Espacio y Astronomía, Clima y Meteorología, Gestión de Recursos Naturales, Geología y Ciencias de la Tierra, Ciencias Químicas, y Geografía.')
    st.write(':woman-woman-boy: **Ciencias Sociales**: Cultura y Arqueología, Ciencias Sociales, Educación, social, Ciencias Políticas, y Culturas Indígenas.')
    st.write(':computer: **Tecnología**: Informática y Ciencias de la Computación, Transporte, y Sonido.')

    # search = st.text_input(":mag_right: Encuentra un proyecto por el nombre:")

    scopesdf = []
    filteredCS['Scope2'] = filteredCS['Ámbitos del Proyecto']
    for sco in scope:
        filteredCS['Scope2'] = filteredCS.apply(lambda row: scope_in_project(row['Scope2'], sco), axis=1)
        scopesdf.append(filteredCS[filteredCS['Scope2'] == sco])
    
    
    if len(scopesdf) != 0:
        filteredCS = pd.concat(scopesdf)
        filteredCS = filteredCS.drop(['Scope2'], axis=1)
        # if search:
        #     filteredCS['CHECK'] = filteredCS.apply(lambda row: search_project(row['Nombre del Proyecto'], search), axis=1)
        #     filteredCS = filteredCS[filteredCS['CHECK'] == 'YES']
        #     filteredCS = filteredCS.drop('CHECK', axis=1)
        show_df = filteredCS.drop('Project Full Description', axis=1)
        st.dataframe(show_df.sort_index())
    else:
        st.write('Debes escoger al menos una opción.')

    KC = ''
    KC1 = "Desarrollar una actitud responsable a partir de la toma de conciencia de la degradación del medio ambiente basada en el conocimiento de las causas que la provocan, agravan o mejoran, desde una visión sistémica, tanto local como global."
    KC2 = "Identificar los distintos aspectos relacionados con el consumo responsable y de productos de proximidad, valorando sus repercusiones sobre el bien individual y el común, juzgando críticamente las necesidades y los excesos y ejerciendo un control social ante la vulneración de sus derechos como consumidor."
    KC3 = "Desarrollar hábitos de vida saludable a partir de la comprensión del funcionamiento de el organismo y la reflexión crítica sobre los factores internos y externos que inciden, asumiendo la responsabilidad personal en la promoción de la salud pública, incluido el conocimiento de una sexualidad positiva, respetuosa e igualitaria."
    KC4 = "Ejercitar la sensibilidad para detectar situaciones de desigualdad y exclusión desde la comprensión de las causas complejas para desarrollar sentimientos de empatía."
    KC5 = "Desarrollar un compromiso activo con la igualdad de género, la igualdad de trato y la no discriminación, conociendo el recorrido histórico para la consecución de los derechos humanos de todas las personas y colectivos."
    KC6 = "Entender los conflictos como elementos connaturales a la vida en sociedad que deben resolver de forma pacífica y rechazar cualquier expresión de violencia machista, LGTBIfóbica, racista, capacitista o motivada por cualquier otro tipo de situación personal o socioeconómica."
    KC7 = "Analizar de forma crítica y aprovechar las oportunidades de todo tipo que ofrece la sociedad actual, en particular las de la cultura digital, evaluando sus beneficios y riesgos y hacer un uso ético y responsable que contribuya a la mejora de la calidad de vida personal y colectiva."
    KC8 = "Aceptar la incertidumbre como una oportunidad para articular respuestas más creativas, aprendiendo a gestionar la ansiedad que puede comportar."
    KC9 = "Cooperar y convivir en sociedades abiertas y cambiantes, valorar la diversidad personal y cultural como fuente de riqueza y fomentando el interés por otras lenguas y culturas."
    KC10 = "Sentirse parte de un proyecto colectivo, tanto a nivel local como global, desarrollando empatía y generosidad."
    KC11 = "Desarrollar las habilidades que le permitan seguir aprendiendo a lo largo de la vida, desde la confianza en el conocimiento como motor de desarrollo y la valoración crítica de los riesgos y beneficios de este conocimiento."
    listKC = [KC1, KC2, KC3, KC4, KC5, KC6, KC7, KC8, KC9, KC10, KC11]
    shortKC = ['concienciación del medio ambiente', 'consumo de productos locales', 'vida saludable', 'inclusión social', 'género', 'perspectiva social', 'tecnología', 'creatividad', 'cooperación', 'colaborar', 'educación']

    if len(scope) != 0:
        pred = st.selectbox("### En qué quieres basarte para encontrar proyectos similares?", ("Competencias Clave", "Otras"))
        if pred == "Otras":
            KC = st.text_input("Introduce las palabras clave para buscar proyectos similares (por ejemplo: 'animales salvajes'):")
        else:
            selectedKC = st.selectbox("Escoge una competencia clave:", (listKC))
            selectedKC = listKC.index(selectedKC)
            KC = shortKC[selectedKC]

        if KC != '':
            # STEP 1: Preprocess the data
            projectsCS_clean = filteredCS.copy()
            projectsCS_clean['Project Full Description'].apply(build_terms)
            KC = build_terms(KC)

            # STEP 2: Create text embeddings
            vectorizer = TfidfVectorizer()
            text_embeddings = vectorizer.fit_transform(projectsCS_clean['Project Full Description'])
            input_embedding = vectorizer.transform(KC)

            # STEP 3: Calculate similarity (cosine similarity)
            similarities = cosine_similarity(input_embedding, text_embeddings)


            # Step 4: Output CS project recommendations
            num_recommendations = select_max_rec(filteredCS)  # Number of recommended projects to display
            top_indices = similarities.argsort()[0][-num_recommendations:][::-1]  # Sort and get the top indices



            st.write("##### Proyectos recomendados:")
            df = show_df.iloc[top_indices]
            st.dataframe(df)

            wc = create_wordcloud(projectsCS_clean, top_indices)
            wordcloud = WordCloud(max_words=150, background_color="white").generate(', '.join(wc))
            fig, ax = plt.subplots(1, 1, figsize = (12, 8))
            ax.imshow(wordcloud, interpolation = 'bilinear')
            plt.axis('off')
            st.pyplot(fig)

show_characteristics_page()