import streamlit as st
import openrouteservice
import requests
import math
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from PIL import Image

def planificador_rutas():
    # Configuración de la página
    st.set_page_config(page_title="Virosque TMS", page_icon="🚛", layout="wide")

    # Estilo personalizado
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f5;
            }
            .stButton>button {
                background-color: #8D1B2D;
                color: white;
                border-radius: 6px;
                padding: 0.6em 1em;
                border: none;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #a7283d;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo y encabezado
    try:
        logo = Image.open("logo-virosque2-01.png")
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            st.image(logo, width=200)
        with col_title:
            st.markdown("<h1 style='color:#8D1B2D;'>TMS</h1>", unsafe_allow_html=True)
            st.markdown("### Planificador de rutas para camiones", unsafe_allow_html=True)
    except:
        st.warning("⚠️ Logo no encontrado. Asegúrate de que 'logo-virosque2-01.png' está en el directorio correcto.")

    # API Key
    api_key = "5b3ce3597851110001cf6248ec3aedee3fa14ae4b1fd1b2440f2e589"
    client = openrouteservice.Client(key=api_key)

    # Geocodificación
    def geocode(direccion):
        url = "https://api.openrouteservice.org/geocode/search"
        params = {
            "api_key": api_key,
            "text": direccion,
            "boundary.country": "ES",
            "size": 1
        }
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            data = r.json()
            if data["features"]:
                coord = data["features"][0]["geometry"]["coordinates"]
                label = data["features"][0]["properties"]["label"]
                return coord, label
            else:
                return None, None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error HTTP geocodificando '{direccion}': {e}")
            return None, None

    # Conversión de horas decimales
    def horas_y_minutos(valor_horas):
        horas = int(valor_horas)
        minutos = int(round((valor_horas - horas) * 60))
        return f"{horas}h {minutos:02d}min"

    # Entradas del usuario
    col1, col2, col3 = st.columns(3)
    with col1:
        origen = st.text_input("📍 Origen", value="Valencia, España")
    with col2:
        destino = st.text_input("🏁 Destino", value="Madrid, España")
    with col3:
        hora_salida_str = st.time_input("🕒 Hora de salida", value=datetime.strptime("08:00", "%H:%M")).strftime("%H:%M")

    # Paradas intermedias
    stops = st.text_area("➕ Paradas intermedias (una por línea)", placeholder="Ej: Albacete, España\nCuenca, España")

    # Inicialización del estado
    if "mostrar_resultados" not in st.session_state:
        st.session_state.mostrar_resultados = False

    if st.button("🔍 Calcular Ruta"):
        st.session_state.mostrar_resultados = True

    # Resultados
    if st.session_state.mostrar_resultados:
        coord_origen, _ = geocode(origen)
        coord_destino, _ = geocode(destino)

        stops_list = []
        if stops.strip():
            for parada in stops.strip().split("\n"):
                coord, _ = geocode(parada)
                if coord:
                    stops_list.append(coord)
                else:
                    st.warning(f"❌ No se pudo geolocalizar: {parada}")

        if not coord_origen or not coord_destino:
            st.error("❌ No se pudo geolocalizar el origen o destino.")
            return

        coords_totales = [coord_origen] + stops_list + [coord_destino]

        try:
            ruta = client.directions(
                coordinates=coords_totales,
                profile='driving-hgv',
                format='geojson'
            )
        except openrouteservice.exceptions.ApiError as e:
            st.error(f"❌ Error al calcular la ruta: {e}")
            return

        segmentos = ruta['features'][0]['properties']['segments']
        distancia_total = sum(seg["distance"] for seg in segmentos)
        duracion_total = sum(seg["duration"] for seg in segmentos)

        distancia_km = distancia_total / 1000
        duracion_horas = duracion_total / 3600
        descansos = math.floor(duracion_horas / 4.5)
        tiempo_total_h = duracion_horas + descansos * 0.75

        descanso_diario_h = 11 if tiempo_total_h > 13 else 0
        tiempo_total_real_h = tiempo_total_h + descanso_diario_h
        hora_salida = datetime.strptime(hora_salida_str, "%H:%M")
        hora_llegada = hora_salida + timedelta(hours=tiempo_total_real_h)

        tiempo_conduccion_txt = horas_y_minutos(duracion_horas)
        tiempo_total_txt = horas_y_minutos(tiempo_total_h)

        st.markdown("### 📊 Datos de la ruta")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🛣 Distancia", f"{distancia_km:.2f} km")
        col2.metric("🕓 Conducción", tiempo_conduccion_txt)
        col3.metric("⏱ Total (con descansos)", tiempo_total_txt)
        col4.metric("📅 Llegada estimada", hora_llegada.strftime("%H:%M"))

        if tiempo_total_h > 13:
            st.warning(f"⚠️ El viaje excede la jornada máxima (13h). Se ha añadido un descanso obligatorio de 11h.\n⏳ Tiempo total ajustado: {horas_y_minutos(tiempo_total_real_h)}")
        else:
            st.success("🟢 El viaje puede completarse en una sola jornada de trabajo.")

        # Mapa
        linea = ruta["features"][0]["geometry"]["coordinates"]
        linea_latlon = [[p[1], p[0]] for p in linea]
        m = folium.Map(location=linea_latlon[0], zoom_start=6)
        folium.Marker(location=[coord_origen[1], coord_origen[0]], tooltip="📍 Origen").add_to(m)
        for idx, parada in enumerate(stops_list):
            folium.Marker(location=[parada[1], parada[0]], tooltip=f"Parada {idx + 1}").add_to(m)
        folium.Marker(location=[coord_destino[1], coord_destino[0]], tooltip="🏁 Destino").add_to(m)
        folium.PolyLine(linea_latlon, color="blue", weight=5).add_to(m)

        st.markdown("### 🗺️ Ruta estimada en mapa:")
        st_folium(m, width=1200, height=500)
