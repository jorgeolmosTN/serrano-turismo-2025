import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

# --- ENCABEZADO CON LOGO A LA DERECHA ---
col_titulo, col_logo = st.columns([4, 1])

with col_titulo:
    st.title("Serrano Turismo - Comparador 2025")

with col_logo:
    # Usamos la URL de la imagen de tu Facebook/Web para asegurar que cargue
    logo_url = "https://serranoturismo.com.ar/wp-content/uploads/2023/02/logo-serrano-turismo.png" 
    st.image(logo_url, width=150)

st.markdown("---")

# Datos del documento 
data = {
    "Programa": [
        "Cordoba 6 dias en bus", "Cordoba 6 dias en avion", 
        "Cordoba 5 dias en bus", "Cordoba 5 dias en avion", 
        "Cordoba 4 dias en avion"
    ],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100],
    "Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "Cuota_6": [150000, 182000, 123500, 156000, 130000],
    "IPC_18": [28333, 36667, 23333, 31667, 25833]
}

df = pd.DataFrame(data)

# --- SECCION SUPERIOR: PLAN ELEGIDO ---
st.subheader("⭐ Tu Plan Seleccionado")
opcion = st.selectbox("Elige el plan que mas te interesa:", df["Programa"])
v = df[df["Programa"] == opcion].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Precio Lista", f"$ {v['Total']:,}")
c2.metric("Precio Contado", f"$ {v['Contado']:,}")
c3.metric("6 Cuotas Fijas", f"$ {v['Cuota_6']:,}")
c4.metric("Cuota Base IPC", f"$ {v['IPC_18']:,}")

st.divider()

# --- SECCION INFERIOR: COMPARATIVA ---
st.subheader("🔍 Comparativa con otras alternativas")

df_otros = df[df["Programa"] != opcion].copy()
df_otros["Dif. Total"] = df_otros["Total"] - v["Total"]
df_otros["Dif. Contado"] = df_otros["Contado"] - v["Contado"]

df_display = df_otros[["Programa", "Total", "Dif. Total", "Contado", "Dif. Contado"]]

# Estilo de tabla con colores para diferencias
st.dataframe(
    df_display.style.format({
        "Total": "$ {:,.0f}", 
        "Contado": "$ {:,.0f}",
        "Dif. Total": "{:+,.0f}",
        "Dif. Contado": "{:+,.0f}"
    }).applymap(
        lambda x: 'color: #d63031' if isinstance(x, (int, float)) and x > 0 
        else 'color: #27ae60' if isinstance(x, (int, float)) and x < 0 
        else '', 
        subset=["Dif. Total", "Dif. Contado"]
    ),
    use_container_width=True
)

st.info("💡 Los valores en verde indican cuanto ahorras respecto al plan seleccionado arriba.")

# Link de WhatsApp con el plan seleccionado [cite: 6]
st.sidebar.markdown("---")
st.sidebar.markdown(f"[¿Dudas? Habla con Martin por WhatsApp](https://api.whatsapp.com/send?phone=5491167877990&text=Hola%20Martin%20vi%20el%20plan%20{opcion.replace(' ', '%20')}%20y%20me%20gustaria%20consultarte)")
