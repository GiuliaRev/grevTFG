# about.py
import streamlit as st
st. set_page_config(layout="wide", initial_sidebar_state="collapsed")

import base64
from pathlib import Path
from PIL import Image

from new_main import get_base64, set_background



def main():


    wallpaper = (Path(__file__).parents[0]/'wallpaper.png')
    set_background(wallpaper)

    col01, col02, col03, col04, col05, col06 = st.columns(6)

    col01.page_link("pages/about.py", label="Sobre el Proyecto", icon="ℹ️")
    col02.page_link("pages/recommender.py", label="Recomendador", icon="🔍")
    col03.page_link("pages/kc.py", label="Competencias", icon="📚")
    col04.page_link("pages/create_acc.py", label="Crear Cuenta", icon="🆕")
    col05.page_link("pages/new_login.py", label="Login", icon="🔒")
    col06.page_link("pages/forgot_pass.py", label="Contraseña Olvidada", icon="❓")

    st.title(' Extensión de "Sistema de Recomendación de Proyectos de Ciencia Ciudadana Basados en el Currículum de Primaria de Cataluña" ')

    col6, col7 = st.columns(2)

    col6.write("""Este proyecto es un trabajo de final de grado realizado por Cinta Arnau Arasa en el año académico 2022-2023 y **extendido por Giulia Anamaria Reveica en el año académico 2023-2024** , con la ayuda de Patricia Santos y Miriam Calvera como tutoras.""")
    col6.write("""Este proyecto trata de la creación de un sistema de recomendación de proyectos de Ciencia Ciudadana. Los proyectos que conforman la base de datos han sido extraídos de las plataformas de Ciencia Ciudadana "Observatorio de la Ciencia Ciudadana en España" y "Oficina de la Ciència Ciutadana". """)
    
    col6.write("""El objetivo del proyecto es poder recomendar un conjunto de proyectos de Ciencia Ciudadana que puedan trabajarse en las clases de primaria según las necesidades del profesor. 
               La idea principal es poder encontrar y recomendar los proyectos que pueden ayudar a alcanzar las competencias clave de primaria según el currículum de primaria de Cataluña. 
               Opcionalmente, los profesores tienen la posibilidad de encontrar otro tipo de proyectos según sus necesidades, simplemente introduciendo las palabras clave en el buscador. 
               Adicionalmente, se puede realizar un filtrado según los ámbitos de los proyectos que se quieran tener en cuenta para el proceso de recomendación.""")
    
    col6.write("""**Extensión**: Con el fin de ofrecer una experiencia más personalizada, se ha añadido la funcionalidad de crear cuentas de usuario y valorar con una puntuación de 1 a 5 los proyectos que hay en la base de datos. 
               Además, se ha añadido una barra superior con la intención de hacer más fluida la navegación entre las diferentes páginas de la aplicación.""")
    
    col6.write("""En el proceso de creación de la cuenta, el usuario puede introducir todas las competencias y todas las palabras clave que le interesan, de tal manera que estas preferencias estarán asociadas a la cuenta, una vez creada. 
               Esta adición permite ver al mismo tiempo y en la misma pantalla, las recomendaciones para _cada una_ de las preferencias almacenadas, ya sea competencia o palabra clave.""") 
    
    col6.write("""Para estas recomendaciones personalizadas, los proyectos recomendados estarán ordenados según la puntuación global media obtenida, en base a las valoraciones hechas por los usuarios. 
               La información mostrada en las recomendaciones personalizadas será: el título del proyecto, la descripción, el enlace hacia el sitio web y el/los ámbito/s del proyecto.""")  
           
    col6.write("""En cuanto a las valoraciones, existe la posibilidad de editar una valoración ya realizada, al igual que eliminarla, y además visualizar todas las valoraciones que el usuario tiene registradas actualmente. 
               Al hacer una valoración nueva, en la lista de proyectos solo aparecerán los que no han sido valorados aún.""")
    
    col6.write("""En cuanto a las cuentas, en el apartado de ajustes es posible cambiar el nombre de usuario y la contraseña, al igual que eliminar la cuenta y toda la información asociada a esta.
               Adicionalmente, se puede establecer una pregunta de seguridad que se puede utilizar para restablecer la contraseña, en el caso de olvidarla. También se pueden editar las preferencias asociadas a la cuenta """)
    
    col6.write("""Resumidamente, la extensión está pensada como un complemento al recomendador inicial, y está pensada para aquellos usuarios que quieran dar un paso más allá de una búsqueda rápida, 
               tener sus preferencias almacenadas para un plus de comodidad, y tener en cuenta las opiniones de los otros usuarios para los proyectos recomendados. """)

    original_upf = Image.open(Path(__file__).parents[0]/'UPF.png')
    original_cc_ES = Image.open(Path(__file__).parents[0]/'cc_ES.png')
    original_cc_BCN = Image.open(Path(__file__).parents[0]/'aj_BCN2.png')

    col7.image(original_upf)
    col7.image(original_cc_ES)
    col7.image(original_cc_BCN)

if __name__ == "__main__":
    main()