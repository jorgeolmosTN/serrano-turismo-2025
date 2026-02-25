import streamlit as st
import pandas as pd

# 1. Configuración de Estética Profesional
st.set_page_config(page_title="Serrano Turismo | Catálogo 2026-2027", layout="wide")

# Estilo CSS para minimalismo
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    div[data-testid="stSidebarNav"] { display: none; }
    .footer-text { font-size: 0.8rem; color: #6c757d; line-height: 1.2; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos Integrada
# Villa Carlos Paz [cite: 1, 2, 4]
costos_cba = {
    "Programa": ["Córdoba 6 días en bus", "Córdoba 6 días en avión", "Córdoba 5 días en bus"],
    "Total": [690000, 840000, 570000],
    "Contado": [600000, 750000, 495000],
    "Fija_P4": [45000, 45000, 37500],
    "Inscripcion": [10800, 10800, 9000]
}

# San Pedro [cite: 2, 4] (Valores estimados basados en estructura comercial)
costos_sp = {
    "Programa": ["San Pedro 4 días / 3 noches", "San Pedro 3 días / 2 noches"],
    "Total": [450000, 380000],
    "Contado": [395000, 330000],
    "Fija_P4": [30000, 25000],
    "Inscripcion": [8100, 8100]
}

# 3. Navegación Unificada en Sidebar
with st.sidebar:
    st.image("https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png", width=180)
    st.markdown("---")
    
    # Menú Principal Atado
    opcion_menu = st.radio(
        "EXPLORAR DESTINOS",
        ["VILLA CARLOS PAZ", "SAN PEDRO"],
        index=0
    )
    
    st.markdown("---")
    # Sub-menú dependiente del destino
    seccion = st.selectbox(
        "DETALLES DEL VIAJE",
        ["Planes y Costos", "Hotelería y Gastronomía", "Excursiones", "Transporte y Seguridad"]
    )

    # Información de Contacto Discreta (Footer Sidebar)
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
    <b>Nuestras Oficinas</b><br>
    Av. Rivadavia 4532 - Galería Alefa (local 10)<br>
    C1042AAP - C.A.B.A.<br><br>
    Del Cimarrón 1846 - 1er Piso - Of. 4<br>
    C.P.: 1714 - Parque Leloir Ituzaingo<br><br>
    <b>Teléfonos</b><br>
    (011) 4847-6467<br>
    (011) 5609-6283 (WA)<br><br>
    <b>Mail</b><br>
    info@serranoturismo.com.ar
    </div>
    """, unsafe_allow_html=True)

# 4. Lógica de Contenido
if opcion_menu == "VILLA CARLOS PAZ":
    df = pd.DataFrame(costos_cba)
    
    if seccion == "Planes y Costos":
        st.header("Villa Carlos Paz 2026/27")
        st.subheader("Planes de Financiación")
        sel_p = st.selectbox("Seleccione el programa", df["Programa"])
        v = df[df["Programa"] == sel_p].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Valor Lista", f"$ {v['Total']:,}")
        c2.metric("Pago Contado", f"$ {v['Contado']:,}")
        c3.metric("Reserva / Inscrip.", f"$ {v['Inscripcion']:,}")
        
        st.write(f"**Plan Mixto:** 4 cuotas fijas iniciales de **$ {v['Fija_P4']:,}**[cite: 4].")

    elif seccion == "Hotelería y Gastronomía":
        st.header("Alojamiento Exclusivo")
        st.write("Hoteles Parque y Capilla del Lago.")
        st.markdown("""
        * **Pensión Completa:** Desayuno buffet, almuerzo y cena con menú de 3 pasos.
        * **Bebidas:** Gaseosas de primera marca (Línea Coca Cola) libres en las comidas.
        * **Servicios:** Habitaciones con somier, aire acondicionado y baño privado.
        """)

    elif seccion == "Excursiones":
        st.header("Experiencias Incluidas")
        st.markdown("""
        * **Peko's Multiparque:** Incluye traslados y pasaporte.
        * **Mundo Cocoguana:** Parque acuático y actividades aéreas.
        * **Recreación:** Coordinadores especializados y fiestas temáticas nocturnas.
        """)

elif opcion_menu == "SAN PEDRO":
    df = pd.DataFrame(costos_sp)
    
    if seccion == "Planes y Costos":
        st.header("San Pedro 2026/27")
        sel_p = st.selectbox("Seleccione el programa", df["Programa"])
        v = df[df["Programa"] == sel_p].iloc[0]
        
        c1, c2 = st.columns(2)
        c1.metric("Valor Lista", f"$ {v['Total']:,}")
        c2.metric("Pago Contado", f"$ {v['Contado']:,}")

    elif seccion == "Hotelería y Gastronomía":
        st.header("Hotel de Turismo San Pedro (La Rueda)")
        st.write("Ubicación privilegiada con amplios parques y piletas.")
        st.markdown("""
        * **Pileta Climatizada:** Uso exclusivo para el grupo.
        * **Régimen:** Pensión completa con bebidas de primera marca ilimitadas.
        * **Habitaciones:** Confort superior con aire acondicionado y TV.
        """)

    elif seccion == "Excursiones":
        st.header("Actividades San Pedro")
        st.markdown("""
        * **La Campiña de Mónica y César:** Visita guiada por la plantación y galpón de empaque.
        * **Vuelta al Obligado:** Recorrido histórico por el sitio de la batalla.
        * **Aventura:** Safari fotográfico y navegación por el Delta.
        """)

# Secciones comunes de logística
if seccion == "Transporte y Seguridad":
    st.header("Logística y Seguridad Vial")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Transporte")
        st.write("""
        * Unidades Mix (Semi-cama y Cama) de última generación.
        * GPS y monitoreo satelital las 24 hs.
        * Servicio a bordo y bar disponible.
        """)
    with col_b:
        st.subheader("Seguridad")
        st.write("""
        * Cobertura médica: Universal Assistance.
        * App Viaxlab: Seguimiento en tiempo real para padres.
        * Coordinación permanente con profesionales de educación física.
        """)

# WhatsApp Flotante Contextual
msg = f"Hola Martín, consulto por {opcion_menu} ({seccion})."
st.sidebar.markdown(f"""
    <a href="https://api.whatsapp.com/send?phone=5491167877990&text={msg.replace(' ', '%20')}" target="_blank">
        <button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:10px;">
            Consultar por WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)
