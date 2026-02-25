import streamlit as st
import pandas as pd

# Configuración de la interfaz
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

# Título y Estilo
st.title("🚌 Cotizador de Planes - Córdoba 2025")
st.markdown("---")

# Carga de datos (basado en el PDF de Serrano Turismo)
data = {
    "Programa": [
        "Córdoba 6 días en bus", "Córdoba 6 días en avión", 
        "Córdoba 5 días en bus", "Córdoba 5 días en avión", 
        "Córdoba 4 días en avión"
    ],
    "Cuota Inscripción": [10800, 10800, 9000, 9000, 8100],
    "Valor Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "3 cuotas consec.": [230000, 280000, 190000, 240000, 200000],
    "6 cuotas consec.": [150000, 182000, 123500, 156000, 130000],
    "Fija (Plan 3)": [60000, 60000, 50000, 50000, 45000],
    "Fija (Plan 4)": [45000, 45000, 37500, 37500, 33750],
    "IPC 18 cuotas": [28333, 36667, 23333, 31667, 25833],
    "IPC 17 cuotas": [30000, 38824, 24706, 33529, 27353],
    "IPC 16 cuotas": [31875, 41250, 26250, 35625, 29063]
}

df = pd.DataFrame(data)

# --- SIDEBAR: SELECCIÓN ---
st.sidebar.header("Configura tu Viaje")
opcion_viaje = st.sidebar.selectbox("¿Qué viaje prefieres?", df["Programa"])

# Extraer datos de la opción seleccionada
viaje = df[df["Programa"] == opcion_viaje].iloc[0]

# --- DASHBOARD PRINCIPAL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Valor de Lista", f"${viaje['Valor Total']:,}")
with col2:
    st.metric("Pago Contado", f"${viaje['Contado']:,}")
with col3:
    st.metric("Cuota Social/Inscrip.", f"${viaje['Cuota Inscripción']:,}")

st.markdown("### 💳 Alternativas de Pago")

tab1, tab2 = st.tabs(["Cuotas Consecutivas", "Plan Mixto (Fijas + IPC)"])

with tab1:
    c1, c2 = st.columns(2)
    c1.info(f"**3 Cuotas de:** ${viaje['3 cuotas consec.']:,}")
    c2.info(f"**6 Cuotas de:** ${viaje['6 cuotas consec.']:,}")

with tab2:
    st.write("Este plan combina cuotas fijas iniciales con cuotas ajustables por IPC.")
    
    # Cuotas fijas iniciales
    f1, f2 = st.columns(2)
    f1.success(f"Opción A: 3 Cuotas Fijas de ${viaje['Fija (Plan 3']:,}")
    f2.success(f"Opción B: 4 Cuotas Fijas de ${viaje['Fija (Plan 4']:,}")
    
    st.markdown("**Resto financiado con ajuste IPC:**")
    i1, i2, i3 = st.columns(3)
    i1.warning(f"18 Cuotas: ${viaje['IPC 18 cuotas']:,}")
    i2.warning(f"17 Cuotas: ${viaje['IPC 17 cuotas']:,}")
    i3.warning(f"16 Cuotas: ${viaje['IPC 16 cuotas']:,}")

st.sidebar.markdown("---")
st.sidebar.