import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date, time
import uuid
import pandas as pd
import os

CSV_FILE = "eventos.csv"

def cargar_eventos():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient="records")
    return []

def guardar_eventos(eventos):
    df = pd.DataFrame(eventos)
    df.to_csv(CSV_FILE, index=False)

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    # Inicialización
    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()
    if "editando_evento" not in st.session_state:
        st.session_state.editando_evento = None

    # Mostrar calendario visual
    eventos_formateados = []
    for e in st.session_state.eventos:
        fecha_obj = pd.to_datetime(e["fecha"])
        eventos_formateados.append({
            "id": e["id"],
            "title": f'{e["asunto"]} - {e["ubicacion"]}',
            "start": fecha_obj.strftime("%Y-%m-%dT%H:%M:%S"),
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

    st.subheader("📆 Vista calendario")
    calendar(events=eventos_formateados, options=calendar_options)

    st.divider()

    # Formulario de creación
    if st.session_state.editando_evento is None:
        st.subheader("➕ Crear nuevo evento")
        with st.form("form_crear"):
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
                        "fecha": fecha.isoformat(),
                    }
                    st.session_state.eventos.append(nuevo_evento)
                    guardar_eventos(st.session_state.eventos)
                    st.success("✅ Evento guardado.")
                    st.rerun()
                else:
                    st.warning("Completa todos los campos.")
    else:
        st.subheader("✏️ Editar evento")
        evento_actual = next((e for e in st.session_state.eventos if e["id"] == st.session_state.editando_evento), None)
        if evento_actual:
            with st.form("form_editar"):
                asunto = st.text_input("Asunto", value=evento_actual["asunto"])
                ubicacion = st.text_input("Ubicación", value=evento_actual["ubicacion"])
                fecha = st.date_input("Fecha", value=pd.to_datetime(evento_actual["fecha"]).date())
                guardar = st.form_submit_button("Guardar cambios")
                cancelar = st.form_submit_button("Cancelar")

                if guardar:
                    evento_actual["asunto"] = asunto
                    evento_actual["ubicacion"] = ubicacion
                    evento_actual["fecha"] = fecha.isoformat()
                    guardar_eventos(st.session_state.eventos)
                    st.success("✅ Evento actualizado.")
                    st.session_state.editando_evento = None
                    st.rerun()
                elif cancelar:
                    st.session_state.editando_evento = None
                    st.rerun()

    st.subheader("📋 Lista de eventos")
    if not st.session_state.eventos:
        st.info("No hay eventos todavía.")
    else:
        for i, e in enumerate(st.session_state.eventos):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(f"📌 **{e['asunto']}** — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("✏️ Editar", key=f"edit_{i}"):
                    st.session_state.editando_evento = e["id"]
                    st.rerun()
            with col3:
                if st.button("❌ Borrar", key=f"del_{i}"):
                    st.session_state.eventos.pop(i)
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()
