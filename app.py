import streamlit as st
import pandas as pd

# 1. Configuracion de la pagina
st.set_page_config(page_title="Serrano Turismo - Catalogo Interactivo", layout="wide")

# Logo y Estilos
logo_url = "https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png"

# --- DATOS EXTRAIDOS DE LOS PDF ---

# Datos de Costos (basados en el esquema 2025/2026 adaptado)
costos_cba = {
    "Programa": ["Cordoba 6 dias en bus", "Cordoba 6 dias en avion", "Cordoba 5 dias en bus"],
    "Total": [690000, 840000, 570000],
    "Contado": [600000, 750000, 495000],
    "Fija_P4": [45000, 45000, 37500]
}

costos_san_pedro = {
    "Programa": ["San Pedro 4 dias / 3 noches", "San Pedro 3 dias / 2 noches"],
    "Total": [450000, 380000],
    "Contado": [395000, 330000],
    "Fija_P4": [30000, 25000]
}

# --- MENU LATERAL (SIDEBAR) ---
st.sidebar.image(logo_url, width=150)
st.sidebar.title("Configura tu Viaje")

# Primer paso: Elegir Destino
destino = st.sidebar.selectbox("¿A donde quieres viajar?", ["Villa Carlos Paz", "San Pedro"])

st.sidebar.markdown("---")

# Segundo paso: Elegir Seccion
seccion = st.sidebar.radio(
    "Selecciona que quieres ver:",
    ["💰 Costos y Planes", "🏨 Hoteleria", "🎡 Excursiones", "🚌 Transporte", "🛡️ Cobertura Medica"]
)

# --- LOGICA POR DESTINO ---

if destino == "Villa Carlos Paz":
    df = pd.DataFrame(costos_cba)
    
    if seccion == "💰 Costos y Planes":
        st.title(f"Planes de Pago - {destino}")
        op = st.selectbox("Selecciona el programa:", df["Programa"])
        v = df[df["Programa"] == op].iloc[0]
        
        c1, c2 = st.columns(2)
        c1.metric("Valor Lista", f"$ {v['Total']:,}")
        c2.metric("Pago Contado", f"$ {v['Contado']:,}", f"- $ {v['Total']-v['Contado']:,} Ahorro")
        
        st.info(f"Este plan incluye 4 cuotas fijas iniciales de $ {v['Fija_P4']:,} y saldo ajustable.")

    elif seccion == "🏨 Hoteleria":
        st.title("Hoteleria Exclusiva en Carlos Paz")
        st.write("Hoteles: **Parque** y **Capilla del Lago**.")
        col1, col2 = st.columns(2)
        col1.markdown("### Hotel Parque\n- Habitaciones con Somier\n- Aire Acondicionado\n- Piletas con guardavidas")
        col2.image("https://www.parquehotelcba.com.ar/images/galeria/hotel/01.jpg")

    elif seccion == "🎡 Excursiones":
        st.title("Diversion sin limites")
        st.write("- **Mundo Cocoguana:** Parque acuatico y aereo.\n- **Peko's:** El parque multitematico numero 1.\n- **Fiestas de Disfraces** y boliches exclusivos (Khalama, Molino Rojo).")

elif destino == "San Pedro":
    df = pd.DataFrame(costos_san_pedro)
    
    if seccion == "💰 Costos y Planes":
        st.title(f"Planes de Pago - {destino}")
        op = st.selectbox("Selecciona el programa:", df["Programa"])
        v = df[df["Programa"] == op].iloc[0]
        
        c1, c2 = st.columns(2)
        c1.metric("Valor Lista", f"$ {v['Total']:,}")
        c2.metric("Pago Contado", f"$ {v['Contado']:,}")
        
    elif seccion == "🏨 Hoteleria":
        st.title("Hoteleria en San Pedro")
        st.subheader("Hotel de Turismo San Pedro - La Rueda")
        st.write("- Habitaciones con AA y baño privado.\n- Pileta exterior y **Pileta Climatizada**.\n- Juegos inflables y amplios parques.")
        st.info("Regimen de Pension Completa con gaseosas ilimitadas de primera marca.")

    elif seccion == "🎡 Excursiones":
        st.title("Actividades en San Pedro")
        st.write("- **Vuelta al Obligado:** Historia y naturaleza.\n- **Estancia La Campiña:** Visita a la plantacion de naranjos de Monica y Cesar.\n- **Navegacion por el Delta.**")

# --- SECCIONES COMUNES (TRANSPORTE Y SEGURIDAD) ---
if seccion == "🚌 Transporte":
    st.title("Transporte de Primera Clase")
    st.write("Unidades Mix (Semi-cama y Cama) monitoreadas por GPS.")
    st.write("- Refrigerios a bordo\n- Pantallas LED / DVD\n- Viaje por Autopista (Sin rebotes)")

if seccion == "🛡️ Cobertura Medica":
    st.title("Seguridad y Asistencia")
    st.write("Cobertura de **Universal Assistance** con pulsera VIAXLAB para seguimiento en tiempo real de los padres.")

# Pie de pagina con WhatsApp Dinamico
mensaje_wa = f"Hola Martin, estoy consultando por {destino} - seccion {seccion}"
url_wa = f"https://api.whatsapp.com/send?phone=5491167877990&text={mensaje_wa.replace(' ', '%20')}"
st.sidebar.markdown("---")
st.sidebar.markdown(f"### [📲 Consultar por WhatsApp]({url_wa})")
