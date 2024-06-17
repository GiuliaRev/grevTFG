import streamlit as st
st. set_page_config(layout="wide", initial_sidebar_state="collapsed")
import base64
from pathlib import Path
from PIL import Image

from new_main import get_base64, set_background



wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
set_background(wallpaper)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
col2.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
col3.page_link("pages/kc.py", label="Competencias", icon="📚")
col4.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
col5.page_link("pages/new_login.py", label="Login", icon="🔒")
col6.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

st.title("Competencias Clave del Currículum de Primaria de Cataluña")


st.write("### Las competencias clave que se definen en el currículum son las siguientes:")
st.write("1. Desarrollar una actitud responsable a partir de la toma de conciencia de la degradación del medio ambiente basada en el conocimiento de las causas que la provocan, agravan o mejoran, desde una visión sistémica, tanto local como global.")
st.write(" :arrow_right: Resumida como **concienciación del medio ambiente**")
st.write("2. Identificar los distintos aspectos relacionados con el consumo responsable y de productos de proximidad, valorando sus repercusiones sobre el bien individual y el común, juzgando críticamente las necesidades y los excesos y ejerciendo un control social ante la vulneración de sus derechos como consumidor.")
st.write(" :arrow_right: Resumida como **consumo de productos locales**")
st.write("3. Desarrollar hábitos de vida saludable a partir de la comprensión del funcionamiento de el organismo y la reflexión crítica sobre los factores internos y externos que inciden, asumiendo la responsabilidad personal en la promoción de la salud pública, incluido el conocimiento de una sexualidad positiva, respetuosa e igualitaria.")
st.write(" :arrow_right: Resumida como **vida saludable**")
st.write("4. Ejercitar la sensibilidad para detectar situaciones de desigualdad y exclusión desde la comprensión de las causas complejas para desarrollar sentimientos de empatía.")
st.write(" :arrow_right: Resumida como **inclusión social**")
st.write("5. Desarrollar un compromiso activo con la igualdad de género, la igualdad de trato y la no discriminación, conociendo el recorrido histórico para la consecución de los derechos humanos de todas las personas y colectivos.")
st.write(" :arrow_right: Resumida como **género**")
st.write("6. Entender los conflictos como elementos connaturales a la vida en sociedad que deben resolver de forma pacífica y rechazar cualquier expresión de violencia machista, LGTBIfóbica, racista, capacitista o motivada por cualquier otro tipo de situación personal o socioeconómica.")
st.write(" :arrow_right: Resumida como **perspectiva social**")
st.write("7. Analizar de forma crítica y aprovechar las oportunidades de todo tipo que ofrece la sociedad actual, en particular las de la cultura digital, evaluando sus beneficios y riesgos y hacer un uso ético y responsable que contribuya a la mejora de la calidad de vida personal y colectiva.")
st.write(" :arrow_right: Resumida como **tecnología**")
st.write("8. Aceptar la incertidumbre como una oportunidad para articular respuestas más creativas, aprendiendo a gestionar la ansiedad que puede comportar.")
st.write(" :arrow_right: Resumida como **creatividad**")
st.write("9. Cooperar y convivir en sociedades abiertas y cambiantes, valorar la diversidad personal y cultural como fuente de riqueza y fomentando el interés por otras lenguas y culturas.")
st.write(" :arrow_right: Resumida como **cooperación**")
st.write("10. Sentirse parte de un proyecto colectivo, tanto a nivel local como global, desarrollando empatía y generosidad.")
st.write(" :arrow_right: Resumida como **colaborar**")
st.write("11. Desarrollar las habilidades que le permitan seguir aprendiendo a lo largo de la vida, desde la confianza en el conocimiento como motor de desarrollo y la valoración crítica de los riesgos y beneficios de este conocimiento.")
st.write(" :arrow_right: Resumida como **educación**")
