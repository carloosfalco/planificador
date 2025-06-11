import streamlit as st
import openrouteservice
import requests
import math
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from PIL import Image

def planificador_rutas():
    # Configuración y estilo
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f5;
            }
            .stButton>button {
                background-color: #8D1B2D;
                color: white;
                border-radius: 6px;
                padding: 0.6em 1em;
                border: none;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #a7283d;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Encabezado
    logo = Image.open("logo-virosque2-01.png")
    st.image(logo, width=250)
    st.markdown("<h1 style='color:#8D1B2D;'>TMS</h1>", unsafe_allow_html=True)
    st.markdown("### Planificador de rutas para camiones", unsafe_allow_html=True)

    # API
    api_key = "5b3ce3597851110001cf6248ec3aedee3fa14ae4b1fd1b2440f2e589"
    client = openrouteservice.Client(key=api_key)

    def geocode(direccion):
        url = "https://api.openrouteservice.org/ge
