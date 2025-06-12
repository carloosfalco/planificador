import streamlit as st
import openai
import os

# Configura tu clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")  # Asegúrate de configurar esta variable en tu entorno

def generar_orden_carga():
    st.title("📦 Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden de carga.")

    with st.form("orden_form"):
        cliente = st.text_input("Cliente")
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        fecha_carga = st.date_input("Fecha de carga")
        hora_carga = st.time_input("Hora de carga")
        tipo_mercancia = st.text_input("Tipo de mercancía")
        tipo_camion = st.selectbox("Tipo de camión", ["LONA", "FRIGO"])
        observaciones = st.text_area("Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        prompt = f"""
        Eres un asistente de logística profesional. Redacta una orden de carga en español usando los siguientes datos:

        Cliente: {cliente}
        Origen: {origen}
        Destino: {destino}
        Fecha de carga: {fecha_carga}
        Hora de carga: {hora_carga}
        Tipo de mercancía: {tipo_mercancia}
        Tipo de camión: {tipo_camion}
        Observaciones: {observaciones or 'Ninguna'}

        Redacta un mensaje claro, formal y profesional que pueda enviarse por email o WhatsApp al conductor.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un experto en redacción logística en español."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )

            mensaje_generado = response["choices"][0]["message"]["content"]
            st.markdown("### ✉️ Orden generada:")
            st.text_area("Mensaje", mensaje_generado, height=250)
            st.success("✅ Copia el mensaje para enviarlo al transportista.")

        except Exception as e:
            st.error(f"❌ Error al generar el mensaje: {e}")
