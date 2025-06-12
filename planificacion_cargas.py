import pandas as pd
import streamlit as st

# Cargar el archivo con la asignación óptima
def cargar_asignacion():
    asignacion_path = "asignacion_optima_19mayo.xlsx"  # asegúrate de tener este archivo en el mismo directorio
    return pd.read_excel(asignacion_path)

def planificacion():
    st.title("🗂️ Planificación de Rutas y Cargas")

    st.markdown("### 📋 Resultado de asignación óptima para el 19/05/2025")
    asignacion_df = cargar_asignacion()
    st.dataframe(asignacion_df)

    # Permitir descarga de Excel
    with open("asignacion_optima_19mayo.xlsx", "rb") as f:
        st.download_button(
            label="📥 Descargar asignación en Excel",
            data=f,
            file_name="asignacion_optima_19mayo.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
