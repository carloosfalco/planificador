import streamlit as st
from rutas import planificador_rutas
from asignacion_cargas import asignacion_cargas
from orden_carga_generator import generar_orden_carga

# Configuración de la página
st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

# Menú lateral con botones directos
st.sidebar.title("📋 Menú")
seccion = st.sidebar.radio("Selecciona una sección:", [
    "Planificador de Rutas",
    "Asignación de Cargas",
    "Orden de Carga"
])

# Mostrar la sección seleccionada
if seccion == "Planificador de Rutas":
    planificador_rutas()
elif seccion == "Asignación de Cargas":
    asignacion_cargas()
elif seccion == "Orden de Carga":
    generar_orden_carga()
