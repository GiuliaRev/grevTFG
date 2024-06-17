import streamlit as st

import base64
from pathlib import Path
from PIL import Image

# icon="ℹ️"

#st. set_page_config(layout="wide")
st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity: 0.9;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
set_background(wallpaper)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
col2.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
col3.page_link("pages/kc.py", label="Competencias", icon="📚")
col4.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
col5.page_link("pages/new_login.py", label="Login", icon="🔒")
col6.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

col3.write("## ¡Hola! :wave:")

st.write('#### ¡Bienvenid@ a la página de inicio de este Trabajo de Final de Grado! :dizzy: ')
st.write('###### La barra superior será tu amiga para la navegación en esta aplicación :blush: ')
st.write("Lo que puedes visitar es: ")
st.write('-  ℹ️   Sobre el Proyecto - Explicación del proyecto y en qué consiste.'  )
st.write("-  🔍 Recomendador - Un recomendador de proyectos de Ciencia Ciudadana que pueden servir de inspiración para crear actividades en base a las competencias del Curriculum Catalán de Primaria. ")
st.write("-  📚 Competencias - Las competencias del Curriculum Catalán de Primaria.")
st.write("-  🆕 Crear Cuenta - Donde puedes crear una cuenta para acceder a las funcionalidades completas de esta aplicación. ")
st.write("-  🔒 Login - Donde al introducir tus credenciales podrás visualizar y acceder a más contenido, como por ejemplo valorar los proyectos y ver recomendaciones personalizadas ordenadas en función de las valoraciones de los otros usuarios. ")
st.write ("-  ❓Contraseña Olvidada - Donde puedes crear una nueva contraseña para tu cuenta, si **previamente** has establecido una pregunta de seguridad en los ajustes de la misma. ")


st.write ("##### ¡Esperemos que te guste! :smile:")



