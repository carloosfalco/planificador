import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def planificacion():
    st.title("📦 Planificación de Cargas")
    
    st.markdown("Esta sección asigna cargas automáticamente a camiones disponibles evitando cruces de tipo y optimizando disponibilidad, precio y kms.")

    file = "Optimización Cargas.xlsx"
    df_cargas = pd.read_excel(file, sheet_name="Cargas1")
    df_camiones = pd.read_excel(file, sheet_name="CAMIONES")

    geolocator = Nominatim(user_agent="planificador")

    def geocode_ciudad(ciudad):
        try:
            location = geolocator.geocode(ciudad + ", España")
            return (location.latitude, location.longitude)
        except:
            return (None, None)

    df_camiones['coords'] = df_camiones['POSICION DIA 19/05/25'].apply(geocode_ciudad)
    df_cargas['coords_carga'] = df_cargas['LOCALIDAD CARGA'].apply(geocode_ciudad)

    asignaciones = []
    camiones_asignados = set()

    for i, carga in df_cargas.iterrows():
        tipo_necesario = carga['TIPO CAMION']
        precio = carga['precio'] if isinstance(carga['precio'], (int, float)) else 0
        destino = carga['LOCALIDAD DESCARGA']
        coords_destino = geocode_ciudad(destino)
        hora_limite = carga['hora_carga']

        if not carga['coords_carga'] or None in carga['coords_carga']:
            continue

        candidatos = df_camiones[~df_camiones['CAMION'].isin(camiones_asignados)].copy()

        if tipo_necesario == "FRIGO":
            candidatos = candidatos[candidatos['TIPO CAMION'] == "FRIGO"]
        elif tipo_necesario == "LONA":
            candidatos = candidatos[candidatos['TIPO CAMION'] == "LONA"]
        else:
            candidatos = candidatos[candidatos['TIPO CAMION'].isin(["LONA", "FRIGO"])]

        mejor = None
        mejor_punt = -np.inf

        for j, camion in candidatos.iterrows():
            if not camion['coords'] or None in camion['coords']:
                continue

            dist = geodesic(camion['coords'], carga['coords_carga']).km
            if dist > 500:  # umbral de cercanía razonable
                continue

            punt = precio - dist  # simple beneficio estimado
            if punt > mejor_punt:
                mejor = camion
                mejor_punt = punt

        if mejor is not None:
            asignaciones.append({
                'CAMION': mejor['CAMION'],
                'TIPO CAMION': mejor['TIPO CAMION'],
                'LOCALIDAD INICIO': mejor['POSICION DIA 19/05/25'],
                'CARGA': carga['cliente pagador'],
                'CARGA_DESDE': carga['LOCALIDAD CARGA'],
                'CARGA_HASTA': carga['LOCALIDAD DESCARGA'],
                'PRECIO': precio,
                'DISTANCIA APROX. (KM)': round(geodesic(mejor['coords'], carga['coords_carga']).km, 2)
            })
            camiones_asignados.add(mejor['CAMION'])

    df_asignacion = pd.DataFrame(asignaciones)

    if df_asignacion.empty:
        st.warning("No se pudo realizar ninguna asignación. Verifica los datos.")
    else:
        st.success("Asignación realizada con éxito:")
        st.dataframe(df_asignacion, use_container_width=True)

        csv = df_asignacion.to_csv(index=False).encode('utf-8')
        st.download_button("🕃 Descargar asignación CSV", csv, "asignacion_optima.csv", "text/csv")
