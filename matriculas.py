import streamlit as st
import pandas as pd
import os
from datetime import date

CSV_FILE = "matriculas.csv"
CSV_MOVIMIENTOS = "movimientos.csv"

@st.cache_data
def cargar_matriculas():
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return pd.DataFrame(columns=["chófer", "tractora", "remolque"])
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

def eliminar_csv_matriculas():
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        st.success("Archivo de matrículas eliminado correctamente.")
    else:
        st.info("No hay archivo de matrículas que eliminar.")

def matriculas():
    st.title("🚚 Gestión de Matrículas")

    uploaded_file = st.file_uploader("📤 Subir archivo Excel de matrículas", type=["xlsx"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            guardar_matriculas(df)
            st.success("Archivo cargado correctamente y datos guardados en CSV permanente.")
        except Exception as e:
            st.error(f"Error al procesar el archivo subido: {e}")
    else:
        df = cargar_matriculas()

    st.subheader("📋 Tabla de chóferes y vehículos")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("💾 Guardar cambios"):
        guardar_matriculas(edited_df)
        st.success("Cambios guardados correctamente.")

    st.divider()

    st.subheader("📝 Registrar movimiento de matrículas")
    with st.form("form_movimiento"):
        fecha_mov = st.date_input("📅 Fecha", value=date.today())
        df = cargar_matriculas()
        choferes_disponibles = [""]
        if "chófer" in df.columns:
            choferes_disponibles += df["chófer"].dropna().unique().tolist()

        chofer_mov = st.selectbox("👤 Chófer", options=choferes_disponibles)
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

    st.divider()

    st.subheader("➕ Añadir nuevo registro")
    with st.form("form_nuevo"):
        chofer = st.text_input("Nombre del chófer").strip()
        tractora = st.text_input("Matrícula tractora").strip()
        remolque = st.text_input("Matrícula remolque").strip()
        crear = st.form_submit_button("Añadir")

        if crear:
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

    if os.path.exists(CSV_MOVIMIENTOS):
        st.subheader("📑 Historial de movimientos registrados")
        historial_df = pd.read_csv(CSV_MOVIMIENTOS)
        st.dataframe(historial_df, use_container_width=True)
    else:
        st.info("Aún no se han registrado movimientos.")

    st.divider()

    st.subheader("🗑️ Eliminar archivo de matrículas")
    if st.button("❌ Eliminar archivo CSV de matrículas"):
        eliminar_csv_matriculas()

