import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date, time
import uuid
import pandas as pd
import os

CSV_FILE = "eventos.csv"

# Función para cargar eventos desde CSV
def cargar_eventos():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient="records")
    return []

# Función para guardar eventos en CSV
def guardar_eventos(eventos):
    df = pd.DataFrame(eventos)
    df.to_csv(CSV_FILE, index=False)

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    # Inicializar eventos con persistencia
    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()

    # Convertir fechas a datetime
    eventos_formateados = []
    for e in st.session_state.eventos:
        fecha_obj = pd.to_datetime(e["fecha"])
        eventos_formateados.append({
            "id": e["id"],
            "title": f'{e["asunto"]} - {e["ubicacion"]}',
            "start": fecha_obj.strftime("%Y-%m-%dT%H:%M:%S"),
            "allDay": True
        })

    # Mostrar calendario
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
                    "fecha": fecha.isoformat(),
                }
                st.session_state.eventos.append(nuevo_evento)
                guardar_eventos(st.session_state.eventos)
                st.success("✅ Evento guardado correctamente.")
                st.rerun()
            else:
                st.warning("Completa todos los campos.")

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
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()

