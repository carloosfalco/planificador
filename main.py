import streamlit as st
from rutas import planificador_rutas
from orden_carga_generator import generar_instrucciones_ruta

# ✅ Esta línea debe ir lo más arriba posible
st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

# Menú
st.sidebar.title("📋 Menú")
seccion = st.sidebar.radio("Selecciona una sección:", [
    "Planificador de Rutas",
    "Instrucciones de Ruta"
])

# Llamadas
if seccion == "Planificador de Rutas":
    planificador_rutas()
elif seccion == "Instrucciones de Ruta":
    generar_instrucciones_ruta()
