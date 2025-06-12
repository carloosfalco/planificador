import streamlit as st
from transformers import pipeline
from datetime import date, time

# Inicializar el modelo de generación
@st.cache_resource(show_spinner="Cargando modelo de Hugging Face...")
def cargar_modelo():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generador = cargar_modelo()

def generar_orden_carga():
    st.title("🎞️ Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden de carga.")

    with st.form("orden_form"):
        cliente = st.text_input("Cliente")
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        fecha_carga = st.date_input("Fecha de carga", value=date.today())
        hora_carga = st.time_input("Hora de carga", value=time(8, 0))
        tipo_mercancia = st.text_input("Tipo de mercancía")
        tipo_camion = st.selectbox("Tipo de camión", ["LONA", "FRIGO"])
        observaciones = st.text_area("Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        prompt = f"""
        Redacta una orden de carga profesional en español. Los datos son:

        Cliente: {cliente}
        Origen: {origen}
        Destino: {destino}
        Fecha de carga: {fecha_carga}
        Hora de carga: {hora_carga}
        Tipo de mercancía: {tipo_mercancia}
        Tipo de camión: {tipo_camion}
        Observaciones: {observaciones or 'Ninguna'}

        El mensaje debe ser formal y estar dirigido a un conductor, listo para enviar por WhatsApp o email.
        """

        st.info("🧐 Generando mensaje con Hugging Face...")
        try:
            resultado = generador(prompt, max_new_tokens=200)[0]["generated_text"]
            st.markdown("### ✉️ Orden generada:")
            st.text_area("Mensaje", resultado.strip(), height=250)
            st.success("✅ Copia el mensaje para enviarlo al transportista.")
        except Exception as e:
            st.error(f"❌ Error al generar el mensaje: {e}")
