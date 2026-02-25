import streamlit as st
import pandas as pd

# 1. Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

# 2. Encabezado con Logo y Titulo
col_titulo, col_logo = st.columns([4, 1])
with col_titulo:
    st.title("Serrano Turismo - Comparador de Planes 2025")
with col_logo:
    logo_url = "https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png"
    st.image(logo_url, width=150)

st.markdown("---")

# 3. Datos Oficiales (Extraidos del PDF)
data = {
    "Programa": [
        "Cordoba 6 dias en bus", "Cordoba 6 dias en avion", 
        "Cordoba 5 dias en bus", "Cordoba 5 dias en avion", 
        "Cordoba 4 dias en avion"
    ],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100], #
    "Total": [690000, 840000, 570000, 720000, 600000], #
    "Contado": [600000, 750000, 495000, 645000, 540000], #
    "Cuota_6": [150000, 182000, 123500, 156000, 130000], #
    "Fija_P4": [45000, 45000, 37500, 37500, 33750], #
    "IPC_18": [28333, 36667, 23333, 31667, 25833], #
    "IPC_17": [30000, 38824, 24706, 33529, 27353], #
    "IPC_16": [31875, 41250, 26250, 35625, 29063]  #
}
df = pd.DataFrame(data)

# 4. Seleccion de Plan Principal
st.subheader("⭐ Selecciona tu Viaje")
opcion = st.selectbox("¿Que plan quieres consultar?", df["Programa"])
v = df[df["Programa"] == opcion].iloc[0]

# Metricas Destacadas
m1, m2, m3, m4 = st.columns(4)
m1.metric("Precio de Lista", f"$ {v['Total
