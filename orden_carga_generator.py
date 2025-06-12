import streamlit as st
from datetime import date

def generar_orden_carga():
    st.title("📦 Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden clara y profesional.")

    with st.form("orden_form"):
        cliente = st.text_input("Cliente")
        origen = st.text_input("Origen")
        destino = st.text_input("Destino")
        fecha_carga = st.date_input("📅 Fecha de carga", value=date.today())
        hora_carga = st.time_input("🕒 Hora de carga")
        hora_descarga = st.text_input("🕓 Hora de descarga")
        tipo_mercancia = st.text_input("📦 Tipo de mercancía (opcional)")
        observaciones = st.text_area("📝 Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        mensaje = f"""
Hola, esta es la orden de carga para el día {fecha_carga.strftime('%d/%m/%Y')}:

🚚 Cliente: {cliente}
📍 Origen: {origen}
🎯 Destino: {destino}
⏱ Hora de carga: {hora_carga.strftime('%H:%M')}
📥 Hora de descarga: {hora_descarga}
"""

        if tipo_mercancia.strip():
            mensaje += f"📦 Tipo de mercancía: {tipo_mercancia}\n"

        if observaciones.strip():
            mensaje += f"\n📌 Observaciones: {observaciones.strip()}"
        else:
            mensaje += "\n📌 Sin observaciones adicionales."

        mensaje += "\n\nPor favor, confirma la recepción y disponibilidad lo antes posible."

        st.markdown("### ✉️ Orden generada:")
        st.text_area("Mensaje", value=mensaje.strip(), height=300)
        st.success("✅ Copia el mensaje para enviarlo al transportista.")
