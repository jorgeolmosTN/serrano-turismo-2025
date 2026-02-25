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
m1.metric("Precio de Lista", f"$ {v['Total']:,}")
m2.metric("Precio Contado", f"$ {v['Contado']:,}", f"- $ {v['Total'] - v['Contado']:,} Ahorro")
m3.metric("Inscripcion", f"$ {v['Inscripcion']:,}")
m4.metric("Cuota Base IPC", f"$ {v['IPC_18']:,}")

st.divider()

# 5. Seccion de Tabs: Detalle y Cronograma
tab_detalles, tab_comparativa = st.tabs(["📅 Detalle del Plan", "🔍 Comparar con otros Planes"])

with tab_detalles:
    col_info, col_graf = st.columns([1, 1])
    
    with col_info:
        st.write("### Estructura de Pago (Ejemplo Abr-Nov)") # 
        st.write(f"1. **Cuota Social/Inscripcion:** $ {v['Inscripcion']:,}") # 
        st.write(f"2. **4 Cuotas Fijas (Abr a Jul):** $ {v['Fija_P4']:,} c/u") # [cite: 4, 9]
        st.write(f"3. **Resto (Ago a Nov):** Cuotas desde $ {v['IPC_16']:,} ajustadas por IPC") # [cite: 4, 9]
        
    with col_graf:
        st.write("### Visualizacion del Gasto Mensual")
        # Grafico simple ilustrando la transicion de fija a variable
        meses = ["Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"]
        montos = [v['Fija_P4']]*4 + [v['IPC_16']]*4
        chart_data = pd.DataFrame({"Mes": meses, "Monto Estimado": montos})
        st.bar_chart(chart_data.set_index("Mes"))

with tab_comparativa:
    st.write("### Diferencias respecto a tu seleccion")
    df_comp = df[df["Programa"] != opcion].copy()
    df_comp["Diferencia Total"] = df_comp["Total"] - v["Total"]
    df_comp["Diferencia Contado"] = df_comp["Contado"] - v["Contado"]
    
    df_resumen = df_comp[["Programa", "Total", "Diferencia Total", "Contado", "Diferencia Contado"]]
    
    st.dataframe(
        df_resumen.style.format({
            "Total": "$ {:,.0f}", "Contado": "$ {:,.0f}",
            "Diferencia Total": "{:+,.0f}", "Diferencia Contado": "{:+,.0f}"
        }).applymap(
            lambda x: 'background-color: #f8d7da; color: #721c24' if isinstance(x, (int, float)) and x > 0 
            else 'background-color: #d4edda; color: #155724' if isinstance(x, (int, float)) and x < 0 
            else '', subset=["Diferencia Total", "Diferencia Contado"]
        ), use_container_width=True
    )
    st.caption("Los valores en verde indican opciones mas economicas que la seleccionada.")

# 6. Barra Lateral (Sidebar)
mensaje_wa = f"Hola Martin, vi el plan {opcion} en el comparador y me interesa recibir mas informacion."
url_wa = f"https://api.whatsapp.com/send?phone=5491167877990&text={mensaje_wa.replace(' ', '%20')}"

st.sidebar.image(logo_url, width=100)
st.sidebar.markdown("---")
st.sidebar.markdown(f"### [📲 Consultar por WhatsApp]({url_wa})")
st.sidebar.write("Nota: Se pueden realizar otras opciones de pago de acuerdo a la necesidad de cada familia.") # [cite: 6]

