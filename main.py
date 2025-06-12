import streamlit as st
from asignacion_cargas import asignacion_cargas
from rutas import planificador_rutas
from planificacion_cargas import planificacion

# Configuración de la página
st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

# Menú lateral
opcion = st.sidebar.selectbox("Selecciona una funcionalidad", [
    "Asignación de Cargas",
    "Planificador de Rutas",
    "Planificación Óptima"
])

# Mostrar la funcionalidad correspondiente
if opcion == "Asignación de Cargas":
    asignacion_cargas()
elif opcion == "Planificador de Rutas":
    planificador_rutas()
elif opcion == "Planificación Óptima":
    planificacion()
