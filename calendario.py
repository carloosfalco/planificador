import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
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

    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()
    if "editando_evento" not in st.session_state:
        st.session_state.editando_evento = None

    # Filtros
    st.subheader("🔎 Filtrar eventos")
    tipos_disponibles = sorted(set(e["tipo"] for e in st.session_state.eventos))
    tipo_filtro = st.selectbox("Tipo de evento", ["Todos"] + tipos_disponibles)

    asociados_filtrables = []
    if tipo_filtro == "Chofer":
        asociados_filtrables = sorted(set(e["asociado"] for e in st.session_state.eventos if e["tipo"] == "Chofer"))
    elif tipo_filtro == "Camión":
        asociados_filtrables = sorted(set(e["asociado"] for e in st.session_state.eventos if e["tipo"] == "Camión"))

    asociado_filtro = st.selectbox("Nombre de chófer o matrícula", ["Todos"] + asociados_filtrables) if tipo_filtro != "Todos" else None

    eventos_mostrados = st.session_state.eventos
    if tipo_filtro != "Todos":
        eventos_mostrados = [e for e in eventos_mostrados if e["tipo"] == tipo_filtro]
    if asociado_filtro and asociado_filtro != "Todos":
        eventos_mostrados = [e for e in eventos_mostrados if e["asociado"] == asociado_filtro]

    # Calendario
    st.subheader("📆 Vista calendario")
    eventos_formateados = []
    for e in eventos_mostrados:
        fecha_obj = pd.to_datetime(e["fecha"])
        color = "#1f77b4" if e["tipo"] == "Chofer" else "#ff7f0e"
        eventos_formateados.append({
            "id": e["id"],
            "title": f'{e["asunto"]} ({e["asociado"]})',
            "start": fecha_obj.strftime("%Y-%m-%dT%H:%M:%S"),
            "allDay": True,
            "color": color
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

    calendar(events=eventos_formateados, options=calendar_options)

    st.divider()

    # Cargar choferes/matrículas desde CSV
    try:
        df_mats = pd.read_csv("matriculas.csv")
        choferes = sorted(df_mats["chófer"].dropna().unique().tolist())
        matriculas = sorted(set(df_mats["tractora"].dropna().tolist() + df_mats["remolque"].dropna().tolist()))
    except:
        choferes = []
        matriculas = []

    if st.session_state.editando_evento is None:
        st.subheader("➕ Crear nuevo evento")
        with st.form("form_crear"):
            tipo = st.selectbox("Tipo de evento", ["Chofer", "Camión"])
            if tipo == "Chofer":
                asociado = st.selectbox("Nombre del chófer", choferes) if choferes else st.text_input("Nombre del chófer")
            else:
                asociado = st.selectbox("Matrícula", matriculas) if matriculas else st.text_input("Matrícula")

            asunto = st.text_input("Asunto")
            ubicacion = st.text_input("Ubicación")
            fecha = st.date_input("Fecha", value=date.today())
            enviar = st.form_submit_button("Crear evento")

            if enviar and asunto and ubicacion and asociado:
                nuevo_evento = {
                    "id": str(uuid.uuid4()),
                    "tipo": tipo,
                    "asociado": asociado,
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": fecha.isoformat(),
                }
                st.session_state.eventos.append(nuevo_evento)
                guardar_eventos(st.session_state.eventos)
                st.success("✅ Evento creado")
                st.rerun()
            elif enviar:
                st.warning("Completa todos los campos.")
    else:
        st.subheader("✏️ Editar evento")
        evento_actual = next((e for e in st.session_state.eventos if e["id"] == st.session_state.editando_evento), None)
        if evento_actual:
            with st.form("form_editar"):
                tipo = st.selectbox("Tipo de evento", ["Chofer", "Camión"], index=0 if evento_actual["tipo"] == "Chofer" else 1)
                asociado = st.text_input("Nombre del chófer" if tipo == "Chofer" else "Matrícula", value=evento_actual["asociado"])
                asunto = st.text_input("Asunto", value=evento_actual["asunto"])
                ubicacion = st.text_input("Ubicación", value=evento_actual["ubicacion"])
                fecha = st.date_input("Fecha", value=pd.to_datetime(evento_actual["fecha"]).date())
                guardar = st.form_submit_button("Guardar cambios")
                cancelar = st.form_submit_button("Cancelar")

                if guardar:
                    evento_actual["tipo"] = tipo
                    evento_actual["asociado"] = asociado
                    evento_actual["asunto"] = asunto
                    evento_actual["ubicacion"] = ubicacion
                    evento_actual["fecha"] = fecha.isoformat()
                    guardar_eventos(st.session_state.eventos)
                    st.success("✅ Evento actualizado")
                    st.session_state.editando_evento = None
                    st.rerun()
                elif cancelar:
                    st.session_state.editando_evento = None
                    st.rerun()

    st.subheader("📋 Lista de eventos")
    if not eventos_mostrados:
        st.info("No hay eventos para mostrar.")
    else:
        for e in eventos_mostrados:
            col1, col2, col3 = st.columns([0.65, 0.17, 0.18])
            with col1:
                st.markdown(f"📌 **{e['tipo']}** — {e['asociado']} — {e['asunto']} — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("✏️ Editar", key=f"edit_{e['id']}"):
                    st.session_state.editando_evento = e["id"]
                    st.rerun()
            with col3:
                if st.button("❌ Borrar", key=f"del_{e['id']}"):
                    st.session_state.eventos = [ev for ev in st.session_state.eventos if ev["id"] != e["id"]]
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()
