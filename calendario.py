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
        asociado = evento.get("asociado", "")

        # Visualización y selección dinámica
        if tipo == "Chofer":
            choferes = sorted(matriculas_df["chófer"].dropna().unique())
            if choferes:
                asociado = st.selectbox("Nombre del chófer", choferes, index=choferes.index(asociado) if asociado in choferes else 0)
                fila = matriculas_df[matriculas_df["chófer"] == asociado]
                if not fila.empty:
                    fila = fila.iloc[0]
                    st.markdown(f"**Tractora:** {fila['tractora']} &nbsp;&nbsp;&nbsp; **Remolque:** {fila['remolque']}")
            else:
                st.warning("No hay chóferes registrados.")
        else:
            todas_matriculas = pd.concat([
                matriculas_df["tractora"].dropna(),
                matriculas_df["remolque"].dropna()
            ]).unique()
            if todas_matriculas.any():
                index = list(todas_matriculas).index(asociado) if asociado in todas_matriculas else 0
                asociado = st.selectbox("Matrícula tractora o remolque", sorted(todas_matriculas), index=index)
                fila = matriculas_df[
                    (matriculas_df["tractora"] == asociado) | (matriculas_df["remolque"] == asociado)
                ]
                if not fila.empty:
                    fila = fila.iloc[0]
                    st.markdown(f"**Chófer:** {fila['chófer']} &nbsp;&nbsp;&nbsp; **Tractora:** {fila['tractora']} &nbsp;&nbsp;&nbsp; **Remolque:** {fila['remolque']}")
            else:
                st.warning("No hay matrículas registradas.")

        asunto = st.text_input("Asunto", value=evento.get("asunto", ""))
        ubicacion = st.text_input("Ubicación", value=evento.get("ubicacion", ""))
        fecha = st.date_input("Fecha", value=evento.get("fecha", date.today()))

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("💾 Guardar")
        cancelar = col2.form_submit_button("Cancelar")

        if guardar:
            if asunto and ubicacion and asociado:
                nuevo = {
                    "id": evento.get("id", str(uuid.uuid4())),
                    "tipo": tipo,
                    "asociado": asociado,
                    "asunto": asunto,
                    "ubicacion": ubicacion,
                    "fecha": fecha.isoformat()
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
            else:
                st.warning("Completa todos los campos obligatorios.")
        elif cancelar:
            st.session_state.editando_evento = None
            st.rerun()

    st.subheader("📋 Lista de eventos")
    if not eventos_mostrados:
        st.info("No hay eventos para mostrar.")
    else:
        for e in eventos_mostrados:
            col1, col2, col3 = st.columns([0.65, 0.15, 0.2])
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
