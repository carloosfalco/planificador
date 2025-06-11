import streamlit as st
import pandas as pd

def asignacion_cargas():
    st.title("🔄 Asignación automática de cargas")

    # Cargas simuladas
    cargas = pd.DataFrame([
        {"ID": "C001", "Cliente": "Mercadona", "Destino": "Valencia", "Tipo camión requerido": "Frigorífico"},
        {"ID": "C002", "Cliente": "Lidl", "Destino": "Madrid", "Tipo camión requerido": "Lona"},
        {"ID": "C003", "Cliente": "Mercadona", "Destino": "Sevilla", "Tipo camión requerido": "Frigorífico"},
    ])

    # Camiones disponibles
    camiones = pd.DataFrame([
        {"ID": "T001", "Tipo": "Frigorífico", "Ubicación": "Valencia", "Disponible": True, "Tacógrafo OK": True, "Descanso completado": True, "Finde libre": False},
        {"ID": "T002", "Tipo": "Lona", "Ubicación": "Madrid", "Disponible": True, "Tacógrafo OK": True, "Descanso completado": True, "Finde libre": False},
        {"ID": "T003", "Tipo": "Frigorífico", "Ubicación": "Barcelona", "Disponible": False, "Tacógrafo OK": True, "Descanso completado": True, "Finde libre": True},
    ])

    # Asignación
    asignaciones = []
    for _, carga in cargas.iterrows():
        asignado = "❌ No disponible"
        for idx, camion in camiones.iterrows():
            if (
                camion["Tipo"] == carga["Tipo camión requerido"]
                and camion["Disponible"]
                and camion["Tacógrafo OK"]
                and camion["Descanso completado"]
            ):
                asignado = camion["ID"]
                camiones.at[idx, "Disponible"] = False
                break
        asignaciones.append(asignado)

    cargas["Camión asignado"] = asignaciones

    st.markdown("### 📦 Resultado de asignación")
    st.dataframe(cargas, use_container_width=True)
