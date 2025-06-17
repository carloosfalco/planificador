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

    if "eventos" not in st.session_state:
        st.session_state.eventos = cargar_eventos()
    if "editando_evento" not in st.session_state:
        st.session_state.editando_evento = None
    if "filtro_chofers" not in st.session_state:
        st.session_state.filtro_chofers = []
    if "filtro_matriculas" not in st.session_state:
        st.session_state.filtro_matriculas = []
    if "tipo_evento" not in st.session_state:
        st.session_state.tipo_evento = "Chofer"
    if "asociado_seleccionado" not in st.session_state:
        st.session_state.asociado_seleccionado = ""

    matriculas_df = cargar_matriculas()

    todos_chofers = sorted(matriculas_df["chófer"].dropna().unique().tolist())
    todas_matriculas = sorted(set(matriculas_df["tractora"].dropna().tolist() + matriculas_df["remolque"].dropna().tolist()))

    st.subheader("🔎 Filtros")
    st.session_state.filtro_chofers = st.multiselect("Filtrar por chófer(es)", todos_chofers, default=st.session_state.filtro_chofers)
    st.session_state.filtro_matriculas = st.multiselect("Filtrar por matrícula(s)", todas_matriculas, default=st.session_state.filtro_matriculas)

    eventos_filtrados = []
    for e in st.session_state.eventos:
        coincide_chofer = not st.session_state.filtro_chofers or e.get("chofer") in st.session_state.filtro_chofers
        coincide_matricula = not st.session_state.filtro_matriculas or e.get("tractora") in st.session_state.filtro_matriculas or e.get("remolque") in st.session_state.filtro_matriculas
        if coincide_chofer and coincide_matricula:
            eventos_filtrados.append(e)

    st.subheader("📆 Vista calendario")
    eventos_cal = []
    for e in eventos_filtrados:
        eventos_cal.append({
            "id": e["id"],
            "title": f"{e['asunto']} ({e['asociado']})",
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
        evento = {"tipo": "Chofer", "asociado": "", "asunto": "", "ubicacion": "", "fecha": date.today()}
    else:
        st.subheader("✏️ Editar evento")
        modo = "editar"
        evento = next((e for e in st.session_state.eventos if e["id"] == st.session_state.editando_evento), None)
        if evento:
            evento["fecha"] = pd.to_datetime(evento["fecha"]).date()
        else:
            st.session_state.editando_evento = None
            st.rerun()

    with st.form("form_evento"):
        st.session_state.tipo_evento = st.selectbox("Tipo de evento", ["Chofer", "Mantenimiento"], index=0 if evento["tipo"] == "Chofer" else 1)

        if st.session_state.tipo_evento == "Chofer":
            choferes = sorted(matriculas_df["chófer"].dropna().unique())
            st.session_state.asociado_seleccionado = st.selectbox("Nombre del chófer", choferes)
            fila = matriculas_df[matriculas_df["chófer"] == st.session_state.asociado_seleccionado]
            if not fila.empty:
                fila = fila.iloc[0]
                tractora = fila["tractora"]
                remolque = fila["remolque"]
                st.markdown(f"**Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
                chofer = st.session_state.asociado_seleccionado
        else:
            matriculas = sorted(set(matriculas_df["tractora"].dropna().tolist() + matriculas_df["remolque"].dropna().tolist()))
            st.session_state.asociado_seleccionado = st.selectbox("Matrícula tractora o remolque", matriculas)
            fila = matriculas_df[(matriculas_df["tractora"] == st.session_state.asociado_seleccionado) | (matriculas_df["remolque"] == st.session_state.asociado_seleccionado)]
            if not fila.empty:
                fila = fila.iloc[0]
                tractora = fila["tractora"]
                remolque = fila["remolque"]
                chofer = fila["chófer"]
                st.markdown(f"**Chófer:** {chofer} &nbsp;&nbsp;&nbsp; **Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
            else:
                chofer = ""
                tractora = remolque = ""

        asunto = st.text_input("Asunto", value=evento.get("asunto", ""))
        ubicacion = st.text_input("Ubicación", value=evento.get("ubicacion", ""))
        fecha = st.date_input("Fecha", value=evento.get("fecha", date.today()))

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("📅 Guardar")
        cancelar = col2.form_submit_button("Cancelar")

        if guardar:
            if not asunto or not ubicacion or not st.session_state.asociado_seleccionado:
                st.warning("Completa todos los campos obligatorios.")
            else:
                nuevo = {
                    "id": evento.get("id", str(uuid.uuid4())),
                    "tipo": st.session_state.tipo_evento,
                    "asociado": st.session_state.asociado_seleccionado,
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": fecha.isoformat(),
                    "chofer": chofer,
                    "tractora": tractora,
                    "remolque": remolque
                }
                if modo == "crear":
                    st.session_state.eventos.append(nuevo)
                else:
                    for i, e in enumerate(st.session_state.eventos):
                        if e["id"] == nuevo["id"]:
                            st.session_state.eventos[i] = nuevo
                            break
                    st.session_state.editando_evento = None

                guardar_eventos(st.session_state.eventos)
                st.success("✅ Evento guardado correctamente")
                st.rerun()

        elif cancelar:
            st.session_state.editando_evento = None
            st.rerun()

    st.subheader("📋 Lista de eventos")
    if not eventos_filtrados:
        st.info("No hay eventos para mostrar.")
    else:
        for e in eventos_filtrados:
            col1, col2, col3 = st.columns([0.55, 0.2, 0.25])
            with col1:
                if st.button(f"🔍 {e['chofer']}", key=f"filtro_chofer_{e['id']}"):
                    st.session_state.filtro_chofers = [e["chofer"]]
                    st.rerun()
                st.markdown(f"📌 **{e['tipo']}** — {e['asunto']} — {e['ubicacion']} — {e['fecha']}")
            with col2:
                if st.button("✏️ Editar", key=f"edit_{e['id']}"):
                    st.session_state.editando_evento = e["id"]
                    st.rerun()
            with col3:
                if st.button("❌ Borrar", key=f"del_{e['id']}"):
                    st.session_state.eventos = [ev for ev in st.session_state.eventos if ev["id"] != e["id"]]
                    guardar_eventos(st.session_state.eventos)
                    st.rerun()
