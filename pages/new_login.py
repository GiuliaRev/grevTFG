import streamlit as st


from login import authenticate_user, logout
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

st.title("Log In :lock:")

col6, col7 = st.columns(2)


# User Authentication
username = col6.text_input("Usuario")
password = col7.text_input("Contraseña", type="password")

if st.button("Log In :arrow_forward:"):
    if authenticate_user(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        # Redirect to content page
        st.switch_page("pages/new_content.py")
        
    else: st.error("¡Credenciales no coinciden! :confounded:")