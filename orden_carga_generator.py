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
            mensaje += f"📦 Tipo de mercancía: {tipo_mercancia.strip()}\n"

        if observaciones.strip():
            mensaje += f"\n📌 {observaciones.strip()}"

        mensaje += "\n\nPor favor, avisa de inmediato si surge algún problema o hay riesgo de retraso."

        mensaje = mensaje.strip()

        st.markdown("### ✉️ Orden generada:")
        st.text_area("Mensaje", value=mensaje, height=300, key="orden_texto")

        # Botón para copiar (con JavaScript)
        copy_code = f"""
        <button onclick="navigator.clipboard.writeText(document.getElementById('orden_texto').value)"
                style="background-color:#8D1B2D;color:white;border:none;padding:0.6em 1.2em;
                       border-radius:6px;font-weight:bold;cursor:pointer;margin-top:10px;">
            📋 Copiar orden al portapapeles
        </button>
        """
        st.markdown(copy_code, unsafe_allow_html=True)

        st.success("✅ Orden generada con éxito.")
