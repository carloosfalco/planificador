import streamlit as st
from datetime import datetime
from transformers import pipeline
from functools import lru_cache

@st.cache_resource
def cargar_modelo():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generador = cargar_modelo()

def generar_orden_carga():
    st.title("📦 Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden de carga.")

    with st.form("orden_form"):
        chofer = st.text_input("Nombre del chofer")
        cliente = st.text_input("Cliente")
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        fecha_carga = st.date_input("Fecha de carga")
        hora_carga = st.time_input("Hora de carga")
        hora_descarga = st.text_input("Hora de descarga")
        tipo_mercancia = st.text_input("Tipo de mercancía")
        tipo_camion = st.selectbox("Tipo de camión", ["LONA", "FRIGO"])  # No se usará en el texto final
        observaciones = st.text_area("Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        fecha_carga_str = fecha_carga.strftime("%d/%m/%Y")

        # Construcción del mensaje
        mensaje = f"Hola {chofer},\n\n"
        mensaje += f"Tienes asignada una carga para el cliente {cliente}.\n"
        mensaje += f"📍 Origen: {origen}\n"
        mensaje += f"🏁 Destino: {destino}\n"
        mensaje += f"📅 Fecha de carga: {fecha_carga_str}\n"
        mensaje += f"🕒 Hora de carga: {hora_carga.strftime('%H:%M')}\n"
        mensaje += f"🕓 Hora de descarga: {hora_descarga}\n"
        if tipo_mercancia.strip():
            mensaje += f"📦 Tipo de mercancía: {tipo_mercancia}\n"
        if observaciones.strip():
            mensaje += f"📝 Observaciones: {observaciones}\n"
        mensaje += "\nPor favor, confirma la recepción de esta orden y avisa si surge algún problema o retraso."

        # Mostrar mensaje con botón de copia nativo
        st.markdown("### ✉️ Orden generada:")
        st.code(mensaje, language="markdown")
        st.success("✅ Orden generada con éxito")

