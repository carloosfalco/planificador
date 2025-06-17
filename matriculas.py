import streamlit as st
import pandas as pd
import os

CSV_FILE = "matriculas.csv"

def cargar_matriculas():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["chófer", "tractora", "remolque"])

def guardar_matriculas(df):
    df.to_csv(CSV_FILE, index=False)

def matriculas():
    st.title("🚚 Gestión de Matrículas")

    df = cargar_matriculas()

    st.subheader("📋 Tabla de chóferes y vehículos")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("💾 Guardar cambios"):
        guardar_matriculas(edited_df)
        st.success("Cambios guardados correctamente")

    st.divider()

    st.subheader("➕ Añadir nuevo registro")
    with st.form("form_nuevo"):
        chofer = st.text_input("Nombre del chófer")
        tractora = st.text_input("Matrícula tractora")
        remolque = st.text_input("Matrícula remolque")
        crear = st.form_submit_button("Añadir")

        if crear:
            if chofer and tractora and remolque:
                nuevo = pd.DataFrame([{
                    "chófer": chofer,
                    "tractora": tractora,
                    "remolque": remolque
                }])
                df = pd.concat([df, nuevo], ignore_index=True)
                guardar_matriculas(df)
                st.success("Registro añadido")
                st.rerun()
            else:
                st.warning("Completa todos los campos")
