import streamlit as st
from asignacion_cargas import asignacion_cargas
from rutas import planificador_rutas
from orden_carga_generator import generar_orden_carga

# Configuración de la página
st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

# Menú lateral
opcion = st.sidebar.selectbox("Selecciona una funcionalidad", [
    "Asignación de Cargas",
    "Planificador de Rutas"
])

# Mostrar la funcionalidad correspondiente
if opcion == "Asignación de Cargas":
    asignacion_cargas()
elif opcion == "Planificador de Rutas":
    planificador_rutas()
elif opcion == "Orden de Carga":
    generar_orden_carga()
