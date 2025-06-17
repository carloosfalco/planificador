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
        # Validar duplicados antes de guardar
        if edited_df["chófer"].duplicated().any():
            st.error("❌ No puede haber chóferes duplicados.")
        elif edited_df[["tractora", "remolque"]].stack().duplicated().any():
            st.error("❌ Hay matrículas de tractora o remolque duplicadas.")
        else:
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
            errores = []
            if not chofer or not tractora or not remolque:
                errores.append("Debes completar todos los campos.")

            # Validaciones
            if chofer in df["chófer"].values:
                errores.append("Ya existe un chófer con ese nombre.")

            todas_matriculas = pd.concat([df["tractora"], df["remolque"]]).dropna().unique().tolist()
            if tractora in todas_matriculas:
                errores.append("La matrícula de la tractora ya está registrada.")
            if remolque in todas_matriculas:
                errores.append("La matrícula del remolque ya está registrada.")

            if errores:
                for err in errores:
                    st.error(f"❌ {err}")
            else:
                nuevo = pd.DataFrame([{
                    "chófer": chofer,
                    "tractora": tractora,
                    "remolque": remolque
                }])
                df = pd.concat([df, nuevo], ignore_index=True)
                guardar_matriculas(df)
                st.success("Registro añadido correctamente.")
                st.rerun()
