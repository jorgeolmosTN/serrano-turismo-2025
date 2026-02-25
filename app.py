import streamlit as st
import pandas as pd

# 1. Configuración de Estética Profesional
st.set_page_config(page_title="Serrano Turismo | Catálogo 2026-2027", layout="wide")

# Estilo CSS para minimalismo y profesionalismo
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .footer-text { font-size: 0.8rem; color: #6c757d; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos Unificada
# Villa Carlos Paz 
data_cba = {
    "Programa": ["Córdoba 6 días en bus", "Córdoba 6 días en avión", "Córdoba 5 días en bus", "Córdoba 5 días en avión", "Córdoba 4 días en avión"],
    "Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "Fija_P4": [45000, 45000, 37500, 37500, 33750],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100]
}

# San Pedro [cite: 2]
data_sp = {
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
    
    destino = st.radio("DESTINO", ["VILLA CARLOS PAZ", "SAN PEDRO"])
    st.markdown("---")
    seccion = st.selectbox("DETALLES DEL VIAJE", ["Planes y Costos", "Hotelería y Gastronomía", "Excursiones", "Transporte y Seguridad"])

    # Footer Sidebar Discreto
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
    <b>Nuestras Oficinas</b><br>
    Av. Rivadavia 4532 - Galería Alefa (local 10)<br>
    C1042AAP - C.A.B.A.<br>
    Del Cimarrón 1846 - 1er Piso - Of. 4<br>
    C.P.: 1714 - Parque Leloir Ituzaingo<br><br>
    <b>Teléfonos</b><br>
    (011) 4847-6467 / (011) 5609-6283 (WA)<br><br>
    <b>Mail</b><br>
    info@serranoturismo.com.ar
    </div>
    """, unsafe_allow_html=True)

# 4. Lógica de Contenido
if destino == "VILLA CARLOS PAZ":
    df = pd.DataFrame(data_cba)
    pdf_info = "SERRANO-VCP 2026-2027.pdf"
elif destino == "SAN PEDRO":
    df = pd.DataFrame(data_sp)
    pdf_info = "San Pedro 2026-2027.pdf"

# Secciones Dinámicas
if seccion == "Planes y Costos":
    st.header(f"Costos y Comparativa - {destino}")
    sel_p = st.selectbox("Plan seleccionado:", df["Programa"])
    v = df[df["Programa"] == sel_p].iloc[0]
    
    # Métricas Principales 
    c1, c2, c3 = st.columns(3)
    c1.metric("Valor Lista", f"$ {v['Total']:,}")
    c2.metric("Pago Contado", f"$ {v['Contado']:,}", f"- $ {v['Total']-v['Contado']:,} Ahorro")
    c3.metric("Reserva / Inscrip.", f"$ {v['Inscripcion']:,}")

    st.divider()

    # --- RESTAURACIÓN DE LA COMPARATIVA ---
    st.subheader("🔍 Comparativa con otras alternativas")
    df_comp = df[df["Programa"] != sel_p].copy()
    df_comp["Dif. Contado"] = df_comp["Contado"] - v["Contado"]
    df_comp["Dif. Lista"] = df_comp["Total"] - v["Total"]
    
    df_resumen = df_comp[["Programa", "Total", "Dif. Lista", "Contado", "Dif. Contado"]]
    
    st.dataframe(
        df_resumen.style.format({
            "Total": "$ {:,.0f}", "Contado": "$ {:,.0f}",
            "Dif. Lista": "{:+,.0f}", "Dif. Contado": "{:+,.0f}"
        }).applymap(
            lambda x: 'background-color: #f8d7da; color: #721c24' if isinstance(x, (int, float)) and x > 0 
            else 'background-color: #d4edda; color: #155724' if isinstance(x, (int, float)) and x < 0 
            else '', subset=["Dif. Lista", "Dif. Contado"]
        ), use_container_width=True
    )
    st.caption("Los valores en verde indican opciones más económicas respecto a tu selección.")

elif seccion == "Hotelería y Gastronomía":
    st.header("Alojamiento y Pensión Completa")
    if destino == "VILLA CARLOS PAZ":
        st.write("**Hoteles:** Parque y Capilla del Lago. [cite: 2]")
        st.markdown("* **Pensión Completa:** Desayuno buffet, almuerzo y cena con menú de 3 pasos. [cite: 2]\n* **Bebidas:** Gaseosas de primera marca libres en las comidas. [cite: 2]")
    else:
        st.write("**Hotel:** Turismo San Pedro (La Rueda). [cite: 2]")
        st.markdown("* **Pileta Climatizada:** Uso exclusivo. [cite: 2]\n* **Pensión Completa:** Incluye bebidas ilimitadas de primera marca. [cite: 2]")

elif seccion == "Excursiones":
    st.header("Experiencias Incluidas")
    if destino == "VILLA CARLOS PAZ":
        st.markdown("* **Peko's Multiparque:** Traslados y pasaporte incluidos. [cite: 2]\n* **Mundo Cocoguana:** Parque acuático y actividades aéreas. [cite: 2]")
    else:
        st.markdown("* **La Campiña de Mónica y César:** Visita guiada. [cite: 2]\n* **Vuelta al Obligado:** Recorrido histórico. [cite: 2]")

elif seccion == "Transporte y Seguridad":
    st.header("Seguridad y Logística")
    st.write("* **Transporte:** Unidades Mix (Semi-cama y Cama) con GPS. [cite: 2]\n* **Asistencia:** Universal Assistance y App Viaxlab para padres. [cite: 2]")

# Botón de WhatsApp dinámico
msg = f"Hola Martín, consulto por {destino} ({sel_p if 'sel_p' in locals() else seccion})."
st.sidebar.markdown(f"""
    <a href="https://api.whatsapp.com/send?phone=5491167877990&text={msg.replace(' ', '%20')}" target="_blank">
        <button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:10px; cursor:pointer;">
            Consultar por WhatsApp
        </button>
    </a>
    """, unsafe_allow_html=True)
