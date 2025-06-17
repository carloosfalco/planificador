import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import uuid

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    # Inicializar eventos
    if "eventos" not in st.session_state:
        st.session_state.eventos = []

    # Mostrar calendario visual
    st.subheader("📆 Vista calendario")

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": True,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        }
    }

    eventos_calendario = [
        {
            "id": e["id"],
            "title": f'{e["asunto"]} - {e["ubicacion"]}',
            "start": e["fecha"].strftime("%Y-%m-%dT%H:%M:%S"),  # formato correcto
            "allDay": True
        }
        for e in st.session_state.eventos
    ]

    calendar(events=eventos_calendario, options=calendar_options, key="calendario")

    st.divider()
    st.subheader("➕ Crear nuevo evento")

    with st.form("form_manual"):
        asunto = st.text_input("Asunto")
        ubicacion = st.text_input("Ubicación")
        fecha = st.date_input("Fecha", datetime.today())
        guardar = st.form_submit_button("Crear evento")

        if guardar:
            if asunto and ubicacion:
                nuevo_evento = {
                    "id": str(uuid.uuid4()),
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": datetime.combine(fecha, datetime.min.time()),  # fecha completa
                }
                st.session_state.eventos.append(nuevo_evento)
                st.success("✅ Evento añadido correctamente. Recargando...")
                st.experimental_rerun()
            else:
                st.warning("❗ Rellena todos los campos.")

    st.subheader("📋 Lista de eventos")
    for i, e in enumerate(st.session_state.eventos):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"📌 **{e['asunto']}** — {e['ubicacion']} — {e['fecha'].strftime('%Y-%m-%d')}")
        with col2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.eventos.pop(i)
                st.experimental_rerun()
