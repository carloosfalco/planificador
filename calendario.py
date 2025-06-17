import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
import uuid
import pandas as pd
import os

CSV_EVENTOS = "eventos2.csv"
CSV_MATRICULAS = "matriculas.csv"

COLUMNAS_EVENTOS = ["id", "Tipo", "Chófer", "Tractora", "Remolque", "asunto", "ubicacion", "fecha"]

def cargar_eventos():
    if os.path.exists(CSV_EVENTOS):
        df = pd.read_csv(CSV_EVENTOS)
        return df.to_dict(orient="records")
    return []

def guardar_eventos(eventos):
    # Asegurar que cada evento tiene todas las columnas necesarias
    eventos_limpios = []
    for e in eventos:
        evento = {col: e.get(col, "") for col in COLUMNAS_EVENTOS}
        eventos_limpios.append(evento)
    df = pd.DataFrame(eventos_limpios)
    df.to_csv(CSV_EVENTOS, index=False)

def cargar_matriculas():
    if os.path.exists(CSV_MATRICULAS):
        return pd.read_csv(CSV_MATRICULAS)
    return pd.DataFrame(columns=["chófer", "tractora", "remolque"])

def calendario_eventos():
    st.title("🗓️ Calendario interactivo Virosque")

    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()
    if "editando_evento" not in st.session_state:
        st.session_state.editando_evento = None
    if "filtro_chofers" not in st.session_state:
        st.session_state.filtro_chofers = []
    if "filtro_matriculas" not in st.session_state:
        st.session_state.filtro_matriculas = []

    matriculas_df = cargar_matriculas()

    todos_chofers = sorted(matriculas_df["chófer"].dropna().unique().tolist())
    todas_matriculas = sorted(set(matriculas_df["tractora"].dropna().tolist() + matriculas_df["remolque"].dropna().tolist()))

    st.subheader("🔎 Filtros")
    st.session_state.filtro_chofers = st.multiselect("Filtrar por chófer(es)", todos_chofers, default=st.session_state.filtro_chofers)
    st.session_state.filtro_matriculas = st.multiselect("Filtrar por matrícula(s)", todas_matriculas, default=st.session_state.filtro_matriculas)

    eventos_filtrados = []
    for e in st.session_state.eventos:
        coincide_chofer = not st.session_state.filtro_chofers or e.get("Chófer") in st.session_state.filtro_chofers
        coincide_matricula = not st.session_state.filtro_matriculas or e.get("Tractora") in st.session_state.filtro_matriculas or e.get("Remolque") in st.session_state.filtro_matriculas
        if coincide_chofer and coincide_matricula:
            eventos_filtrados.append(e)

    st.subheader("📆 Vista calendario")
    eventos_cal = []
    for e in eventos_filtrados:
        eventos_cal.append({
            "id": e["id"],
            "title": f"{e['asunto']} ({e['Chófer']}{e['tractora']})",
            "start": pd.to_datetime(e["fecha"]).strftime("%Y-%m-%dT%H:%M:%S"),
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
    calendar(events=eventos_cal, options=calendar_options)
    st.divider()

    if st.session_state.editando_evento is None:
        st.subheader("➕ Crear nuevo evento")
        modo = "crear"
        evento = {"Tipo": "Chofer", "asunto": "", "ubicacion": "", "fecha": date.today()}
    else:
        st.subheader("✏️ Editar evento")
        modo = "editar"
        evento = next((e for e in st.session_state.eventos if e["id"] == st.session_state.editando_evento), None)
        if evento:
            evento["fecha"] = pd.to_datetime(evento["fecha"]).date()
        else:
            st.session_state.editando_evento = None
            st.rerun()

    tipo = st.selectbox("Tipo de evento", ["Chofer", "Mantenimiento"], index=0 if evento["Tipo"] == "Chofer" else 1)

    if tipo == "Chofer":
        chofer = st.selectbox("Nombre del chófer", todos_chofers)
        fila = matriculas_df[matriculas_df["chófer"] == chofer]
        if not fila.empty:
            fila = fila.iloc[0]
            tractora = fila["tractora"]
            remolque = fila["remolque"]
            st.markdown(f"**Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
        else:
            tractora = remolque = ""
    else:
        matricula = st.selectbox("Matrícula tractora o remolque", todas_matriculas)
        fila = matriculas_df[(matriculas_df["tractora"] == matricula) | (matriculas_df["remolque"] == matricula)]
        if not fila.empty:
            fila = fila.iloc[0]
            chofer = fila["chófer"]
            tractora = fila["tractora"]
            remolque = fila["remolque"]
            st.markdown(f"**Chófer:** {chofer} &nbsp;&nbsp;&nbsp; **Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
        else:
            chofer = tractora = remolque = ""

    asunto = st.text_input("Asunto", value=evento.get("asunto", ""))
    ubicacion = st.text_input("Ubicación", value=evento.get("ubicacion", ""))
    fecha = st.date_input("Fecha", value=evento.get("fecha", date.today()))

    if st.button("💾 Guardar evento"):
        if not asunto or not ubicacion:
            st.warning("⚠️ Por favor, completa todos los campos obligatorios.")
        else:
            nuevo_evento = {
                "id": evento.get("id", str(uuid.uuid4())),
                "Tipo": tipo,
                "Chófer": chofer,
                "Tractora": tractora,
                "Remolque": remolque,
                "asunto": asunto,
                "ubicacion": ubicacion,
                "fecha": fecha.isoformat()
            }
            if modo == "crear":
                st.session_state.eventos.append(nuevo_evento)
            else:
                for i, e in enumerate(st.session_state.eventos):
                    if e["id"] == nuevo_evento["id"]:
                        st.session_state.eventos[i] = nuevo_evento
                        break
                st.session_state.editando_evento = None

            guardar_eventos(st.session_state.eventos)
            st.success("✅ Evento guardado correctamente")
            st.rerun()

    st.subheader("📋 Lista de eventos")
    if not eventos_filtrados:
        st.info("No hay eventos para mostrar.")
    else:
        for e in eventos_filtrados:
            col1, col2, col3 = st.columns([0.55, 0.2, 0.25])
            with col1:
                if st.button(f"🔍 {e['Chófer']}", key=f"filtro_chofer_{e['id']}"):
                    st.session_state.filtro_chofers = [e["Chófer"]]
                    st.rerun()
                st.markdown(f"📌 **{e['Tipo']}** — {e['asunto']} — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("✏️ Editar", key=f"edit_{e['id']}"):
                    st.session_state.editando_evento = e["id"]
                    st.rerun()
            with col3:
                if st.button("❌ Borrar", key=f"del_{e['id']}"):
                    st.session_state.eventos = [ev for ev in st.session_state.eventos if ev["id"] != e["id"]]
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()
