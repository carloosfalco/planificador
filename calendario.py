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

    matriculas_df = cargar_matriculas()

    # Obtener listas
    todos_chofers = sorted(matriculas_df["chófer"].dropna().unique().tolist())
    todas_matriculas = sorted(set(matriculas_df["tractora"].dropna().tolist() + matriculas_df["remolque"].dropna().tolist()))

    # Filtros múltiples
    st.subheader("🔎 Filtros")
    st.session_state.filtro_chofers = st.multiselect("Filtrar por chófer(es)", todos_chofers, default=st.session_state.filtro_chofers)
    st.session_state.filtro_matriculas = st.multiselect("Filtrar por matrícula(s)", todas_matriculas, default=st.session_state.filtro_matriculas)

    eventos_filtrados = []
    for e in st.session_state.eventos:
        coincide_chofer = not st.session_state.filtro_chofers or e.get("chofer") in st.session_state.filtro_chofers
        coincide_matricula = not st.session_state.filtro_matriculas or e.get("tractora") in st.session_state.filtro_matriculas or e.get("remolque") in st.session_state.filtro_matriculas
        if coincide_chofer and coincide_matricula:
            eventos_filtrados.append(e)

    # Mostrar calendario
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

    # Crear o editar evento
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
        tipo = st.selectbox("Tipo de evento", ["Chofer", "Mantenimiento"], index=0 if evento["tipo"] == "Chofer" else 1)

        if tipo == "Chofer":
            choferes = sorted(matriculas_df["chófer"].dropna().unique())
            asociado = st.selectbox("Nombre del chófer", choferes, index=choferes.index(evento["asociado"]) if evento["asociado"] in choferes else 0)
            fila = matriculas_df[matriculas_df["chófer"] == asociado]
            if not fila.empty:
                fila = fila.iloc[0]
                tractora = fila["tractora"]
                remolque = fila["remolque"]
                st.markdown(f"**Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
            else:
                tractora = remolque = ""
        else:
            matriculas = sorted(set(matriculas_df["tractora"].dropna().tolist() + matriculas_df["remolque"].dropna().tolist()))
            asociado = st.selectbox("Matrícula tractora o remolque", matriculas, index=matriculas.index(evento["asociado"]) if evento["asociado"] in matriculas else 0)
            fila = matriculas_df[(matriculas_df["tractora"] == asociado) | (matriculas_df["remolque"] == asociado)]
            if not fila.empty:
                fila = fila.iloc[0]
                tractora = fila["tractora"]
                remolque = fila["remolque"]
                chofer = fila["chófer"]
                st.markdown(f"**Chófer:** {chofer} &nbsp;&nbsp;&nbsp; **Tractora:** {tractora} &nbsp;&nbsp;&nbsp; **Remolque:** {remolque}")
            else:
                tractora = remolque = chofer = ""

        asunto = st.text_input("Asunto", value=evento.get("asunto", ""))
        ubicacion = st.text_input("Ubicación", value=evento.get("ubicacion", ""))
        fecha = st.date_input("Fecha", value=evento.get("fecha", date.today()))

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("💾 Guardar")
        cancelar = col2.form_submit_button("Cancelar")

        if guardar:
            nuevo = {
                "id": evento.get("id", str(uuid.uuid4())),
                "tipo": tipo,
                "asociado": asociado,
                "asunto": asunto,
                "ubicacion": ubicacion,
                "fecha": fecha.isoformat(),
                "chofer": asociado if tipo == "Chofer" else chofer,
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
