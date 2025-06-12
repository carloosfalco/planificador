import streamlit as st
from asignacion_cargas import mostrar_asignacion_cargas
from rutas import planificador_rutas

st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

menu = st.sidebar.radio("📂 Selecciona una funcionalidad:", ["🚚 Asignación de cargas","📍 Planificador de rutas"])

if menu == "🚚 Asignación de cargas":
   mostrar_asignacion_cargas()
elif menu == "📍 Planificador de rutas":
    planificador_rutas()
