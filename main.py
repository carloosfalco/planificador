import streamlit as st
from rutas import planificador_rutas
from orden_carga_generator import generar_instrucciones_ruta  # ✅ nombre correcto del archivo
from calendario import calendario_eventos  # ✅ nuevo módulo del calendario
from matriculas import matriculas

def main():
    st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

    st.sidebar.title("📂 Menú")
    seleccion = st.sidebar.radio("Selecciona una opción", ["Planificador de rutas", "Orden de carga", "Calendario de eventos"])

    if seleccion == "Planificador de rutas":
        planificador_rutas()
    elif seleccion == "Orden de carga":
        generar_instrucciones_ruta()
    elif seleccion == "Calendario de eventos":
        calendario_eventos()
    elif seleccion == "Matrículas":
    matriculas()

if __name__ == "__main__":
    main()
