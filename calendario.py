import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date, time
import uuid

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    # Inicialización segura
    if "eventos" not in st.session_state:
        st.session_state.eventos = []

    # Preparar eventos para el calendario
    eventos_formateados = []
    for evento in st.session_state.eventos:
        if isinstance(evento["fecha"], date):
            fecha_datetime = datetime.combine(evento["fecha"], time(0, 0))
        else:
            fecha_datetime = evento["fecha"]
        eventos_formateados.append({
            "id": evento["id"],
            "title": f'{evento["asunto"]} - {evento["ubicacion"]}',
            "start": fecha_datetime.isoformat(),
            "allDay": True
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": False,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        }
    }

    # Mostrar calendario visual
    st.subheader("📆 Vista calendario")
    calendar(events=eventos_formateados, options=calendar_options)

    st.divider()

    # Formulario para añadir eventos
    st.subheader("➕ Crear nuevo evento")
    with st.form("form_evento"):
        asunto = st.text_input("Asunto")
        ubicacion = st.text_input("Ubicación")
        fecha = st.date_input("Fecha", value=date.today())
        enviar = st.form_submit_button("Crear evento")

        if enviar:
            if asunto and ubicacion:
                nuevo_evento = {
                    "id": str(uuid.uuid4()),
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": fecha,
                }
                st.session_state.eventos.append(nuevo_evento)
                st.success("✅ Evento añadido correctamente.")
                st.rerun()
            else:
                st.warning("Por favor, completa todos los campos.")

    # Mostrar lista de eventos
    st.subheader("📋 Eventos creados")
    if not st.session_state.eventos:
        st.info("No hay eventos todavía.")
    else:
        for i, e in enumerate(st.session_state.eventos):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"📌 **{e['asunto']}** — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.eventos.pop(i)
                    st.rerun()
