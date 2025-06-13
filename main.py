import streamlit as st
from rutas import planificador_rutas
from generador_ruta import generar_instrucciones_ruta

# Configuración de la página
st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

# Menú lateral con botones directos
st.sidebar.title("📋 Menú")
seccion = st.sidebar.radio("Selecciona una sección:", [
    "Planificador de Rutas",
    "Instrucciones de Ruta"
])

# Mostrar la sección seleccionada
if seccion == "Planificador de Rutas":
    planificador_rutas()
elif seccion == "Instrucciones de Ruta":
    generar_instrucciones_ruta()
