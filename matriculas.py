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
        choferes_duplicados = edited_df["chófer"].dropna().duplicated().any()
        matriculas_total = pd.concat([
            edited_df["tractora"].dropna(),
            edited_df["remolque"].dropna()
        ])
        matriculas_duplicadas = matriculas_total.duplicated().any()

        if choferes_duplicados:
            st.error("❌ No puede haber chóferes duplicados.")
        elif matriculas_duplicadas:
            st.error("❌ No puede haber matrículas de tractora o remolque duplicadas.")
        else:
            guardar_matriculas(edited_df)
            st.success("Cambios guardados correctamente.")

    st.divider()

    st.subheader("➕ Añadir nuevo registro")
    with st.form("form_nuevo"):
        chofer = st.text_input("Nombre del chófer (opcional si es tractora/remolque libre)").strip()
        tractora = st.text_input("Matrícula tractora (opcional)").strip()
        remolque = st.text_input("Matrícula remolque (opcional)").strip()
        crear = st.form_submit_button("Añadir")

        errores = []

        if crear:
            # Validar chofer duplicado si está definido
            if chofer and chofer in df["chófer"].dropna().values:
                errores.append("Ya existe un chófer con ese nombre.")

            # Validar duplicados de matrículas
            todas_matriculas = pd.concat([
                df["tractora"].dropna(),
                df["remolque"].dropna()
            ]).unique().tolist()

            if tractora and tractora in todas_matriculas:
                errores.append("La matrícula de la tractora ya está registrada.")
            if remolque and remolque in todas_matriculas:
                errores.append("La matrícula del remolque ya está registrada.")

            # Al menos uno de los tres campos debe tener valor
            if not chofer and not tractora and not remolque:
                errores.append("Debes rellenar al menos un campo.")

            if errores:
                for err in errores:
                    st.error(f"❌ {err}")
            else:
                nuevo = pd.DataFrame([{
                    "chófer": chofer if chofer else None,
                    "tractora": tractora if tractora else None,
                    "remolque": remolque if remolque else None
                }])
                df = pd.concat([df, nuevo], ignore_index=True)
                guardar_matriculas(df)
                st.success("Registro añadido correctamente.")
                st.rerun()
