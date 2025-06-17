import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, timedelta
import uuid

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    if "eventos" not in st.session_state:
        st.session_state.eventos = []

    # Mostrar el calendario visual
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

    # Adaptar eventos
    eventos_calendario = [
        {
            "id": e["id"],
            "title": f'{e["asunto"]} - {e["ubicacion"]}',
            "start": e["fecha"].isoformat(),
            "allDay": True
        }
        for e in st.session_state.eventos
    ]

    returned_events = calendar(
        events=eventos_calendario,
        options=calendar_options,
        key="calendario",
    )

    st.divider()
    st.subheader("➕ Crear evento manual")

    with st.form("form_manual"):
        asunto = st.text_input("Asunto")
        ubicacion = st.text_input("Ubicación")
        fecha = st.date_input("Fecha", datetime.today())
        crear = st.form_submit_button("Crear evento")

        if crear and asunto and ubicacion:
            st.session_state.eventos.append({
                "id": str(uuid.uuid4()),
                "asunto": asunto,
                "ubicacion": ubicacion,
                "fecha": datetime.combine(fecha, datetime.min.time()),
            })
            st.success("Evento añadido")
            st.experimental_rerun()

    # Mostrar eventos
    st.subheader("📋 Lista de eventos")
    for i, e in enumerate(st.session_state.eventos):
        st.markdown(f"**🗓️ {e['fecha'].strftime('%Y-%m-%d')}** — {e['asunto']} ({e['ubicacion']})")
        if st.button("Eliminar", key=f"del_{i}"):
            st.session_state.eventos.pop(i)
            st.experimental_rerun()
