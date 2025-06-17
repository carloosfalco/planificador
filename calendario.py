import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
import uuid
import pandas as pd
import os

CSV_EVENTOS = "eventos.csv"
CSV_MATRICULAS = "matriculas.csv"

def cargar_eventos():
    if os.path.exists(CSV_EVENTOS):
        df = pd.read_csv(CSV_EVENTOS)
        return df.to_dict(orient="records")
    return []

def guardar_eventos(eventos):
    df = pd.DataFrame(eventos)
    df.to_csv(CSV_EVENTOS, index=False)

def cargar_matriculas():
    if os.path.exists(CSV_MATRICULAS):
        return pd.read_csv(CSV_MATRICULAS)
    return pd.DataFrame(columns=["chófer", "tractora", "remolque"])

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    # Cargar eventos y matrículas
    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()
    if "editando_evento" not in st.session_state:
        st.session_state.editando_evento = None

    matriculas_df = cargar_matriculas()

    # Filtros
    st.subheader("🔎 Filtrar eventos")
    tipos_disponibles = sorted(set(e["tipo"] for e in st.session_state.eventos))
    tipo_filtro = st.selectbox("Tipo de evento", ["Todos"] + tipos_disponibles)

    asociados_filtrables = []
    if tipo_filtro == "Chofer":
        asociados_filtrables = sorted(set(e["asociado"] for e in st.session_state.eventos if e["tipo"] == "Chofer"))
    elif tipo_filtro == "Mantenimiento":
        asociados_filtrables = sorted(set(e["asociado"] for e in st.session_state.eventos if e["tipo"] == "Mantenimiento"))

    asociado_filtro = st.selectbox("Chófer o Matrícula", ["Todos"] + asociados_filtrables) if tipo_filtro != "Todos" else None

    eventos_mostrados = st.session_state.eventos
    if tipo_filtro != "Todos":
        eventos_mostrados = [e for e in eventos_mostrados if e["tipo"] == tipo_filtro]
    if asociado_filtro and asociado_filtro != "Todos":
        eventos_mostrados = [e for e in eventos_mostrados if e["asociado"] == asociado_filtro]

    # Mostrar calendario
    st.subheader("📆 Vista calendario")
    eventos_formateados = []
    for e in eventos_mostrados:
        fecha_obj = pd.to_datetime(e["fecha"])
        eventos_formateados.append({
            "id": e["id"],
            "title": f'{e["asunto"]} ({e["asociado"]})',
            "start": fecha_obj.strftime("%Y-%m-%dT%H:%M:%S"),
            "allDay": True,
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

    # FORMULARIO NUEVO EVENTO
    st.subheader("➕ Crear nuevo evento")

    with st.form("form_evento"):
        tipo = st.selectbox("Tipo de evento", ["Chofer", "Mantenimiento"])

        if tipo == "Chofer":
            choferes = sorted(matriculas_df["chófer"].dropna().unique())
            chofer = st.selectbox("Nombre del chófer", choferes)
            fila = matriculas_df[matriculas_df["chófer"] == chofer].iloc[0]
            tractora = fila["tractora"]
            remolque = fila["remolque"]
            st.markdown(f"**Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
            asociado = chofer

        else:  # Mantenimiento
            todas_matriculas = pd.concat([
                matriculas_df["tractora"].dropna(),
                matriculas_df["remolque"].dropna()
            ]).unique()
            matricula = st.selectbox("Matrícula (tractora o remolque)", sorted(todas_matriculas))

            # Buscar información complementaria
            fila = matriculas_df[
                (matriculas_df["tractora"] == matricula) | (matriculas_df["remolque"] == matricula)
            ]
            if not fila.empty:
                fila = fila.iloc[0]
                chofer = fila["chófer"]
                tractora = fila["tractora"]
                remolque = fila["remolque"]
                st.markdown(f"**Chófer:** {chofer} &nbsp;&nbsp;&nbsp; **Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
            else:
                chofer = "No asignado"
            asociado = matricula

        asunto = st.text_input("Asunto")
        ubicacion = st.text_input("Ubicación")
        fecha = st.date_input("Fecha", value=date.today())
        crear = st.form_submit_button("Crear evento")

        if crear:
            if asunto and ubicacion and asociado:
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
            else:
                st.warning("Completa todos los campos obligatorios.")

    # LISTA DE EVENTOS
    st.subheader("📋 Lista de eventos")
    if not eventos_mostrados:
        st.info("No hay eventos para mostrar.")
    else:
        for e in eventos_mostrados:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(f"📌 **{e['tipo']}** — {e['asociado']} — {e['asunto']} — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("❌ Borrar", key=f"del_{e['id']}"):
                    st.session_state.eventos = [ev for ev in st.session_state.eventos if ev["id"] != e["id"]]
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()

