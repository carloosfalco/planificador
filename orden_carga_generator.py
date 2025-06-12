import streamlit as st
from datetime import date

def generar_orden_carga():
    st.title("📦 Generador de Orden de Carga")
    st.markdown("Completa los siguientes datos para generar una orden clara y profesional.")

    with st.form("orden_form"):
        chofer = st.text_input("Nombre del chofer")
        fecha_carga = st.date_input("📅 Fecha de carga", value=date.today())
        num_origenes = st.number_input("Número de ubicaciones de carga", min_value=1, max_value=5, value=1)
        origenes = [st.text_input(f"📍 Origen {i+1}") for i in range(num_origenes)]

        num_destinos = st.number_input("Número de ubicaciones de descarga", min_value=1, max_value=5, value=1)
        destinos = [st.text_input(f"🎯 Destino {i+1}") for i in range(num_destinos)]

        hora_carga = st.time_input("🕒 Hora de carga")
        hora_descarga = st.text_input("🕓 Hora de descarga")
        tipo_mercancia = st.text_input("📦 Tipo de mercancía (opcional)")
        observaciones = st.text_area("📝 Observaciones (opcional)")

        submitted = st.form_submit_button("Generar orden")

    if submitted:
        mensaje = f"""Hola {chofer}, esta es la orden de carga para el día {fecha_carga.strftime('%d/%m/%Y')}:

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
        st.text_area("Mensaje generado", mensaje, height=300, key="mensaje_generado")

        # Botón de copiar con JavaScript
        copy_js = f"""
            <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    console.log('Texto copiado al portapapeles');
                }}, function(err) {{
                    console.error('Error al copiar:', err);
                }});
            }}
            </script>
            <button onclick="copyToClipboard(`{mensaje}`)">📋 Copiar mensaje</button>
        """

        st.markdown(copy_js, unsafe_allow_html=True)
        st.success("✅ Orden generada con éxito.")
