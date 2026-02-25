import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

# --- ENCABEZADO CON LOGO ---
col_titulo, col_logo = st.columns([4, 1])

with col_titulo:
    st.title("Serrano Turismo - Comparador 2025")

with col_logo:
    # Usando el link directo proporcionado
    logo_url = "https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png"
    st.image(logo_url, width=150)

st.markdown("---")

# Datos oficiales del plan 2025
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
opcion = st.selectbox("Elige el plan que mas te interesa para comparar:", df["Programa"])
v = df[df["Programa"] == opcion].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Precio Lista", f"$ {v['Total']:,}")
c2.metric("Precio Contado", f"$ {v['Contado']:,}")
c3.metric("6 Cuotas Fijas", f"$ {v['Cuota_6']:,}")
c4.metric("Inscripcion", f"$ {v['Inscripcion']:,}")

st.divider()

# --- SECCION INFERIOR: TABLA DE DIFERENCIAS ---
st.subheader("🔍 ¿Como se compara con otros planes?")
st.write("Diferencias calculadas respecto a tu seleccion actual:")

# Crear copia para comparativa
df_comp = df[df["Programa"] != opcion].copy()

# Calcular diferencias (Elegido - Otro) para mostrar cuanto mas o menos cuesta
df_comp["Diferencia Total"] = df_comp["Total"] - v["Total"]
df_comp["Diferencia Contado"] = df_comp["Contado"] - v["Contado"]

# Seleccion de columnas para mostrar
df_mostrar = df_comp[["Programa", "Total", "Diferencia Total", "Contado", "Diferencia Contado"]]

# Formateo visual
st.dataframe(
    df_mostrar.style.format({
        "Total": "$ {:,.0f}", 
        "Contado": "$ {:,.0f}",
        "Diferencia Total": "{:+,.0f}",
        "Diferencia Contado": "{:+,.0f}"
    }).applymap(
        lambda x: 'background-color: #f8d7da; color: #721c24' if isinstance(x, (int, float)) and x > 0 
        else 'background-color: #d4edda; color: #155724' if isinstance(x, (int, float)) and x < 0 
        else '', 
        subset=["Diferencia Total", "Diferencia Contado"]
    ),
    use_container_width=True
)

st.info("💡 Los valores en verde indican planes mas economicos que el seleccionado arriba.")

# Link de WhatsApp dinamico
mensaje_wa = f"Hola Martin, estuve viendo el plan {opcion} en el comparador y me gustaria recibir mas info."
url_wa = f"https://api.whatsapp.com/send?phone=5491167877990&text={mensaje_wa.replace(' ', '%20')}"

st.sidebar.markdown("---")
st.sidebar.markdown(f"### [📲 Consultar por WhatsApp]({url_wa})")
st.sidebar.write("Nota: Se pueden realizar otras opciones de pago de acuerdo a la necesidad de cada familia.") [cite: 6]

