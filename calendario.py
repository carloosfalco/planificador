import streamlit as st
from datetime import datetime
import uuid

def calendario_eventos():
    st.title("🗓️ Calendario de eventos Virosque")

    # Inicializa eventos en sesión si no existen
    if "eventos" not in st.session_state:
        st.session_state.eventos = []

    st.subheader("📋 Lista de eventos")
    if not st.session_state.eventos:
        st.info("No hay eventos todavía.")
    else:
        for i, evento in enumerate(st.session_state.eventos):
            with st.expander(f"📌 {evento['asunto']} — {evento['fecha'].strftime('%Y-%m-%d')}"):
                st.write(f"**Ubicación:** {evento['ubicacion']}")
                if st.button(f"🗑️ Eliminar evento", key=f"del_{i}"):
                    st.session_state.eventos.pop(i)
                    st.success("Evento eliminado")
                    st.experimental_rerun()

    st.divider()

    st.subheader("➕ Crear nuevo evento")
    with st.form("form_evento"):
        asunto = st.text_input("Asunto")
        ubicacion = st.text_input("Ubicación")
        fecha = st.date_input("Fecha", datetime.now())
        guardar = st.form_submit_button("Guardar")

        if guardar:
            if asunto and ubicacion:
                nuevo = {
                    "id": str(uuid.uuid4()),
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": fecha,
                }
                st.session_state.eventos.append(nuevo)
                st.success("✅ Evento creado")
                st.experimental_rerun()
            else:
                st.warning("⚠️ Todos los campos son obligatorios")
