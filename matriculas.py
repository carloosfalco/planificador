import streamlit as st
import pandas as pd
import os
from datetime import date

CSV_MATRICULAS = "matriculas.csv"
CSV_CHOFERES = "choferes.csv"
CSV_MOVIMIENTOS = "movimientos.csv"

@st.cache_data
def cargar_csv(nombre, columnas):
    if os.path.exists(nombre):
        try:
            return pd.read_csv(nombre)
        except Exception as e:
            st.error(f"Error al leer {nombre}: {e}")
    return pd.DataFrame(columns=columnas)

def guardar_csv(df, nombre):
    df.to_csv(nombre, index=False)

def guardar_movimiento(fecha, chofer, tractora, marca, remolque, tipo_remolque, jefe):
    movimiento = pd.DataFrame([{
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Chófer": chofer,
        "Tractora": tractora,
        "Marca Tractora": marca,
        "Remolque": remolque,
        "Tipo Remolque": tipo_remolque,
        "Jefe de tráfico": jefe
    }])
    if os.path.exists(CSV_MOVIMIENTOS):
        historial = pd.read_csv(CSV_MOVIMIENTOS)
        historial = pd.concat([historial, movimiento], ignore_index=True)
    else:
        historial = movimiento
    historial.to_csv(CSV_MOVIMIENTOS, index=False)

def eliminar_csv(nombre):
    if os.path.exists(nombre):
        os.remove(nombre)
        st.success(f"Archivo {nombre} eliminado correctamente.")
    else:
        st.info(f"No hay archivo {nombre} que eliminar.")

def matriculas():
    st.title("🚚 Gestión de Chóferes, Vehículos y Responsables")

    st.subheader("📋 Choferes y Asignaciones")
    df_choferes = cargar_csv(CSV_CHOFERES, [
        "chófer", "tractora", "marca", "remolque", "tipo_remolque", "jefe_trafico"])
    marcas_posibles = ["DAF", "FORD", "MAN", "MERCEDES", "SCANIA", "VOLVO"]
    jefes_trafico = [
        "TAMARA", "ANA", "ALVARO", "PATRICIA", "CRISTOFER", "DAVID",
        "FERMIN", "RAUL", "CESAR", "CARMELO", "PABLO", "JULIO", "GIUSEPPE", "CESAR"]

    edited_choferes = st.data_editor(df_choferes, num_rows="dynamic", use_container_width=True,
        column_config={
            "marca": st.column_config.SelectboxColumn("Marca", options=marcas_posibles),
            "jefe_trafico": st.column_config.SelectboxColumn("Jefe de tráfico", options=jefes_trafico)
        })

    if st.button("💾 Guardar choferes y asignaciones"):
        guardar_csv(edited_choferes, CSV_CHOFERES)
        st.success("Cambios en choferes guardados.")

    st.divider()

    st.subheader("📝 Registrar cambio de tractora/remolque")
    with st.form("form_cambio"):
        fecha = st.date_input("📅 Fecha del cambio", value=date.today())
        df = cargar_csv(CSV_CHOFERES, ["chófer", "tractora", "marca", "remolque", "tipo_remolque", "jefe_trafico"])
        choferes_disponibles = df["chófer"].dropna().unique().tolist()
        chofer = st.selectbox("👤 Chófer", options=choferes_disponibles)
        tractora_nueva = st.text_input("🚛 Nueva tractora")
        marca_actual = df[df["chófer"] == chofer]["marca"].values[0] if chofer in df["chófer"].values else ""
        remolque_nuevo = st.text_input("🚚 Nuevo remolque")
        tipo_remolque = st.selectbox("📦 Tipo de remolque", options=["", "Lona", "Frigo"])
        registrar = st.form_submit_button("Registrar cambio")

        if registrar:
            idx = df[df["chófer"] == chofer].index[0]
            jefe = df.loc[idx, "jefe_trafico"]
            guardar_movimiento(fecha, chofer, tractora_nueva, marca_actual, remolque_nuevo, tipo_remolque, jefe)
            df.at[idx, "tractora"] = tractora_nueva
            df.at[idx, "remolque"] = remolque_nuevo
            df.at[idx, "tipo_remolque"] = tipo_remolque
            guardar_csv(df, CSV_CHOFERES)
            st.success("Cambio registrado y base de datos actualizada.")

    st.divider()

    st.subheader("🔎 Consultar por matrícula de remolque")
    consulta_remolque = st.text_input("🔍 Introduce matrícula del remolque")
    if consulta_remolque:
        df = cargar_csv(CSV_CHOFERES, ["chófer", "tractora", "marca", "remolque", "tipo_remolque", "jefe_trafico"])
        resultado = df[df["remolque"] == consulta_remolque.upper()]
        if not resultado.empty:
            row = resultado.iloc[0]
            st.markdown(f"**Chófer:** {row['chófer']}")
            st.markdown(f"**Tractora:** {row['tractora']} ({row['marca']})")
            st.markdown(f"**Tipo Remolque:** {row['tipo_remolque']}")
            st.markdown(f"**Jefe de tráfico:** {row['jefe_trafico']}")
        else:
            st.warning("No se encontró ningún registro con esa matrícula de remolque.")

    st.divider()

    if os.path.exists(CSV_MOVIMIENTOS):
        st.subheader("📑 Historial de cambios registrados")
        historial_df = pd.read_csv(CSV_MOVIMIENTOS)
        st.dataframe(historial_df, use_container_width=True)
    else:
        st.info("Aún no se han registrado cambios.")

    st.divider()

    st.subheader("🗑️ Eliminar archivos")
    if st.button("❌ Eliminar archivo CSV de choferes"):
        eliminar_csv(CSV_CHOFERES)
    if st.button("❌ Eliminar archivo CSV de movimientos"):
        eliminar_csv(CSV_MOVIMIENTOS)
