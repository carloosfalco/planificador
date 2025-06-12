import streamlit as st
from datetime import date

def generar_orden_carga():
    st.title("📦 Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden clara y profesional.")

    with st.form("orden_form"):
        chofer = st.text_input("Nombre del chofer")
        cliente = st.text_input("Cliente")

        num_origenes = st.number_input("Número de ubicaciones de carga", min_value=1, max_value=5, value=1)
        origenes = [st.text_input(f"📍 Origen {i+1}") for i in range(num_origenes)]

        num_destinos = st.number_input("Número de ubicaciones de descarga", min_value=1, max_value=5, value=1)
        destinos = [st.text_input(f"🎯 Destino {i+1}") for i in range(num_destinos)]

        fecha_carga = st.date_input("📅 Fecha de carga", value=date.today())
        hora_carga = st.time_input("🕒 Hora de carga")
        hora_descarga = st.text_input("🕓 Hora de descarga")
        tipo_mercancia = st.text_input("📦 Tipo de mercancía (opcional)")
        observaciones = st.text_area("📝 Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        mensaje = f"""
Hola {chofer}, esta es la orden de carga para el día {fecha_carga.strftime('%d/%m/%Y')}:

🚚 Cliente: {cliente}
⏱ Hora de carga: {hora_carga.strftime('%H:%M')}
📥 Hora de descarga: {hora_descarga}

📍 Origen:
""" + "\n".join([f"  - {origen}" for origen in origenes if origen.strip()]) + "\n\n🎯 Destino:\n" + "\n".join([f"  - {destino}" for destino in destinos if destino.strip()])

        if tipo_mercancia.strip():
            mensaje += f"\n\n📦 Tipo de mercancía: {tipo_mercancia.strip()}"

        if observaciones.strip():
            mensaje += f"\n\n📌 {observaciones.strip()}"

        mensaje += "\n\nPor favor, avisa de inmediato si surge algún problema o hay riesgo de retraso."

        mensaje = mensaje.strip()

        st.markdown("### ✉️ Orden generada:")
        st.code(mensaje, language="markdown")
        st.download_button("📥 Copiar o descargar orden", data=mensaje, file_name="orden_carga.txt")

# Para incluir en tu main.py:
# from orden_carga_generator import generar_orden_carga
# generar_orden_carga()

