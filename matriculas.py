import streamlit as st
import pandas as pd
import os
from datetime import date

CSV_FILE = "matriculas.csv"
CSV_MOVIMIENTOS = "movimientos.csv"

@st.cache_data

def cargar_matriculas():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["chófer", "tractora", "remolque"])

def guardar_matriculas(df):
    df.to_csv(CSV_FILE, index=False)

def guardar_movimiento(fecha, chofer, deja, coge):
    movimiento = pd.DataFrame([{
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Chófer": chofer,
        "Deja": deja,
        "Coge": coge
    }])
    if os.path.exists(CSV_MOVIMIENTOS):
        historial = pd.read_csv(CSV_MOVIMIENTOS)
        historial = pd.concat([historial, movimiento], ignore_index=True)
    else:
        historial = movimiento
    historial.to_csv(CSV_MOVIMIENTOS, index=False)

def matriculas():
    st.title("🚚 Gestión de Matrículas")

    uploaded_file = st.file_uploader("📤 Subir archivo Excel de matrículas", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        guardar_matriculas(df)
        st.success("Archivo cargado correctamente y datos guardados en CSV.")
    else:
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
        chofer = st.text_input("Nombre del chófer").strip()
        tractora = st.text_input("Matrícula tractora").strip()
        remolque = st.text_input("Matrícula remolque").strip()
        crear = st.form_submit_button("Añadir")

        errores = []

        if crear:
            if chofer and chofer in df["chófer"].dropna().values:
                errores.append("Ya existe un chófer con ese nombre.")

            todas_matriculas = pd.concat([
                df["tractora"].dropna(),
                df["remolque"].dropna()
            ]).unique().tolist()

            if tractora and tractora in todas_matriculas:
                errores.append("La matrícula de la tractora ya está registrada.")
            if remolque and remolque in todas_matriculas:
                errores.append("La matrícula del remolque ya está registrada.")

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

    st.divider()

    st.subheader("📝 Registrar movimiento de matrículas")
    with st.form("form_movimiento"):
        fecha_mov = st.date_input("📅 Fecha", value=date.today())
        chofer_mov = st.selectbox("👤 Chófer", options=[""] + df["chófer"].dropna().unique().tolist())
        deja = st.text_input("🚛 Tractora/Remolque que deja")
        coge = st.text_input("🚚 Tractora/Remolque que coge")
        registrar = st.form_submit_button("Registrar movimiento")

        if registrar:
            guardar_movimiento(fecha_mov, chofer_mov, deja, coge)
            st.success(f"Movimiento registrado:")
            st.markdown(f"- Fecha: {fecha_mov.strftime('%d/%m/%Y')}")
            st.markdown(f"- Chófer: {chofer_mov}")
            st.markdown(f"- Deja: {deja}")
            st.markdown(f"- Coge: {coge}")
