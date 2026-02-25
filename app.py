import streamlit as st
import pandas as pd

# 1. Configuracion de la pagina
st.set_page_config(page_title="Catálogo Serrano Turismo 2025", layout="wide")

# Logo compartido en todos los menus
logo_url = "https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png"

# 2. Datos de Costos (del primer PDF)
data_costos = {
    "Programa": ["Cordoba 6 dias en bus", "Cordoba 6 dias en avion", "Cordoba 5 dias en bus", "Cordoba 5 dias en avion", "Cordoba 4 dias en avion"],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100],
    "Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "Cuota_6": [150000, 182000, 123500, 156000, 130000],
    "Fija_P4": [45000, 45000, 37500, 37500, 33750],
    "IPC_16": [31875, 41250, 26250, 35625, 29063]
}
df = pd.DataFrame(data_costos)

# 3. Menu Lateral
st.sidebar.image(logo_url, width=150)
st.sidebar.title("Navegacion")
menu = st.sidebar.radio(
    "Selecciona una seccion:",
    ["💰 Costos y Comparativa", "🏨 Hoteleria", "🚌 Transporte", "🛡️ Servicios y Cobertura"]
)

st.sidebar.markdown("---")

# 4. Logica de Secciones
if menu == "💰 Costos y Comparativa":
    st.title("Comparador de Planes 2025")
    opcion = st.selectbox("¿Que plan quieres consultar?", df["Programa"])
    v = df[df["Programa"] == opcion].iloc[0]

    m1, m2, m3 = st.columns(3)
    m1.metric("Precio Lista", f"$ {v['Total']:,}")
    m2.metric("Precio Contado", f"$ {v['Contado']:,}", f"- $ {v['Total'] - v['Contado']:,} Ahorro")
    m3.metric("Inscripcion", f"$ {v['Inscripcion']:,}")

    st.divider()
    
    t1, t2 = st.tabs(["📊 Detalle de Cuotas", "🔍 Comparativa"])
    with t1:
        st.write(f"### Estructura de Pago: {opcion}")
        st.write(f"- **Cuotas Fijas (4 meses):** $ {v['Fija_P4']:,}")
        st.write(f"- **Cuotas base IPC (desde):** $ {v['IPC_16']:,}")
        meses = ["Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"]
        montos = [v['Fija_P4']]*4 + [v['IPC_16']]*4
        st.bar_chart(pd.DataFrame({"Monto": montos}, index=meses))
    
    with t2:
        df_comp = df[df["Programa"] != opcion].copy()
        df_comp["Dif. Contado"] = df_comp["Contado"] - v["Contado"]
        st.dataframe(df_comp[["Programa", "Contado", "Dif. Contado"]].style.format({"Contado": "$ {:,.0f}", "Dif. Contado": "{:+,.0f}"}))

elif menu == "🏨 Hoteleria":
    st.title("Hoteleria Exclusiva en Villa Carlos Paz")
    st.write("Serrano Turismo ofrece hoteles exclusivos con todas las comodidades.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hotel Parque")
        st.image("https://www.parquehotelcba.com.ar/images/galeria/hotel/01.jpg", caption="Piletas y recreacion") # URL ejemplo
        st.write("- Habitaciones triples y cuadruples con somier.\n- Aire acondicionado y baño privado.\n- Comedor restaurante con cocina casera.")
    
    with col2:
        st.subheader("Hotel Capilla del Lago")
        st.write("- Ubicacion privilegiada.\n- Amplios espacios verdes.\n- SUM y Teatro/Disco propio.")
        st.info("Todos los hoteles cuentan con guardavidas permanentes y seguridad.")

elif menu == "🚌 Transporte":
    st.title("Transporte y Logistica")
    st.subheader("Buses de Ultima Generacion")
    st.write("""
    - Unidades con aire acondicionado, musica y DVD.
    - Baño y bar a bordo con refrigerios.
    - Monitoreo permanente via satelite (GPS).
    - Viaje integramente por autopista 9 (Sin rebotes).
    """)
    st.subheader("Opcion Aerea")
    st.write("Vuelos de ida y regreso con Aerolineas Argentinas + transfer in/out en destino.")

elif menu == "🛡️ Servicios y Cobertura":
    st.title("Seguridad y Cobertura Medica")
    st.write("Tu tranquilidad es nuestra prioridad.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Cobertura Medica (Universal Assistance)")
        st.write("- Asistencia medica completa y farmacia.\n- Seguimiento post-viaje.\n- Pulsera de seguimiento VIAXLAB APP.")
    
    with c2:
        st.markdown("### Coordinacion")
        st.write("- Personal estable y directivo en destino.\n- Profesores de Educacion Fisica y Recreologos.\n- Coordinacion las 24 hs.")

# Pie de pagina con Link de WhatsApp Dinamico
mensaje_wa = f"Hola Martin, estoy viendo la seccion {menu} y tengo una consulta."
url_wa = f"https://api.whatsapp.com/send?phone=5491167877990&text={mensaje_wa.replace(' ', '%20')}"
st.sidebar.markdown(f"### [📲 Consultar por WhatsApp]({url_wa})")

