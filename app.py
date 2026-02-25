import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

st.title("Serrano Turismo - Planes 2025")
st.markdown("Consulta las opciones de pago para tu viaje a Cordoba.")

# Datos extraidos del documento 
data = {
    "Programa": [
        "Cordoba 6 dias en bus", "Cordoba 6 dias en avion", 
        "Cordoba 5 dias en bus", "Cordoba 5 dias en avion", 
        "Cordoba 4 dias en avion"
    ],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100],
    "Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "3_cuotas": [230000, 280000, 190000, 240000, 200000],
    "6_cuotas": [150000, 182000, 123500, 156000, 130000],
    "Fija_P3": [60000, 60000, 50000, 50000, 45000],
    "Fija_P4": [45000, 45000, 37500, 37500, 33750],
    "IPC_18": [28333, 36667, 23333, 31667, 25833],
    "IPC_17": [30000, 38824, 24706, 33529, 27353],
    "IPC_16": [31875, 41250, 26250, 35625, 29063]
}

df = pd.DataFrame(data)

# Sidebar
opcion = st.sidebar.selectbox("Selecciona tu viaje:", df["Programa"])
v = df[df["Programa"] == opcion].iloc[0]

# Metricas
c1, c2, c3 = st.columns(3)
c1.metric("Valor Lista", f"$ {v['Total']:,}")
c2.metric("Pago Contado", f"$ {v['Contado']:,}")
c3.metric("Inscripcion", f"$ {v['Inscripcion']:,}")

st.divider()

t1, t2 = st.tabs(["Cuotas Fijas", "Plan Mixto IPC"])

with t1:
    st.write("### Opciones de cuotas fijas consecutivas ")
    col_a, col_b = st.columns(2)
    col_a.info(f"3 cuotas de: $ {v['3_cuotas']:,}")
    col_b.info(f"6 cuotas de: $ {v['6_cuotas']:,}")

with t2:
    st.write("### Plan Combinado (Fijas + Ajuste IPC) [cite: 4, 9]")
    st.write("Cuotas fijas iniciales mas cuotas ajustables.")
    
    f1, f2 = st.columns(2)
    f1.success(f"Opcion 3 cuotas fijas de: $ {v['Fija_P3']:,}")
    f2.success(f"Opcion 4 cuotas fijas de: $ {v['Fija_P4']:,}")
    
    st.markdown("**Resto ajustable por IPC:**")
    i1, i2, i3 = st.columns(3)
    i1.warning(f"18 cuotas: $ {v['IPC_18']:,}")
    i2.warning(f"17 cuotas: $ {v['IPC_17']:,}")
    i3.warning(f"16 cuotas: $ {v['IPC_16']:,}")

# Reemplaza la ultima linea de tu codigo por esta:
st.sidebar.markdown(f"[Otras opciones de pago segun necesidad de la familia.](https://api.whatsapp.com/send?phone=5491167877990&text=Hola%20Martin%20me%20gustaria%20armar%20un%20plan%20personalizado)")

