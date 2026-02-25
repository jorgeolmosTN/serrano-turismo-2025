import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo 2025", layout="wide")

st.title("Serrano Turismo - Comparador de Planes 2025")

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
st.write("Aqui puedes ver como varia el presupuesto segun el transporte o los dias de estadia.")

# Filtrar los planes NO elegidos
df_otros = df[df["Programa"] != opcion].copy()

# Calcular diferencias respecto al elegido
df_otros["Dif. Total"] = df_otros["Total"] - v["Total"]
df_otros["Dif. Contado"] = df_otros["Contado"] - v["Contado"]

# Formatear para mostrar
df_display = df_otros[["Programa", "Total", "Dif. Total", "Contado", "Dif. Contado"]]

# Mostrar tabla comparativa
st.dataframe(
    df_display.style.format({
        "Total": "$ {:,.0f}", 
        "Contado": "$ {:,.0f}",
        "Dif. Total": "{:+,.0f}",
        "Dif. Contado": "{:+,.0f}"
    }).applymap(lambda x: 'color: red' if isinstance(x, (int, float)) and x > 0 else 'color: green' if isinstance(x, (int, float)) and x < 0 else '', subset=["Dif. Total", "Dif. Contado"]),
    use_container_width=True
)

st.info("💡 Los valores en verde indican cuanto ahorras respecto al plan seleccionado arriba.")

# Link de WhatsApp al final
st.sidebar.markdown(f"---")
st.sidebar.markdown(f"[¿Dudas? Habla con Martin por WhatsApp](https://api.whatsapp.com/send?phone=5491167877990&text=Hola%20Martin%20vi%20el%20plan%20{opcion.replace(' ', '%20')}%20pero%20quiero%20armar%20algo%20personalizado)")
