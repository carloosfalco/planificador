import streamlit as st
from rutas import planificador_rutas
from orden import orden_carga
from calendario import calendario_eventos  # 👈 nuevo módulo importado

def main():
    st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

    st.sidebar.title("📂 Menú")
    seleccion = st.sidebar.radio("Selecciona una opción", ["Planificador de rutas", "Orden de carga", "Calendario de eventos"])  # 👈 añadida opción

    if seleccion == "Planificador de rutas":
        planificador_rutas()
    elif seleccion == "Orden de carga":
        orden_carga()
    elif seleccion == "Calendario de eventos":  # 👈 nuevo bloque
        calendario_eventos()

if __name__ == "__main__":
    main()
