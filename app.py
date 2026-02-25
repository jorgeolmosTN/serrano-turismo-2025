import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Estética Profesional
st.set_page_config(page_title="Serrano Turismo | Gestión de Preventa", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .footer-text { font-size: 0.8rem; color: #6c757d; line-height: 1.4; }
    .disclaimer { font-size: 0.75rem; color: #7f8c8d; text-align: justify; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    .faq-text { font-size: 0.9rem; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos (Actualizada con info de folletos)
data_cba = {
    "Programa": ["Córdoba 6 días en bus", "Córdoba 6 días en avión", "Córdoba 5 días en bus", "Córdoba 5 días en avión", "Córdoba 4 días en avión"],
    "Total": [690000, 840000, 570000, 720000, 600000],
    "Contado": [600000, 750000, 495000, 645000, 540000],
    "Fija_P4": [45000, 45000, 37500, 37500, 33750],
    "Inscripcion": [10800, 10800, 9000, 9000, 8100]
}

data_sp = {
    "Programa": ["San Pedro 4 días / 3 noches", "San Pedro 3 días / 2 noches"],
    "Total": [450000, 380000],
    "Contado": [395000, 330000],
    "Fija_P4": [30000, 25000],
    "Inscripcion": [8100, 8100]
}

# 3. Navegación Sidebar
with st.sidebar:
    st.image("https://serranoturismo.com.ar/assets/images/logoserrano-facebook.png", width=180)
    st.markdown("---")
    destino = st.radio("DESTINO", ["VILLA CARLOS PAZ", "SAN PEDRO"])
    st.markdown("---")
    seccion = st.selectbox("MENÚ", ["Planes y Costos", "Ficha de Preventa", "Checklist Documentación", "Información Útil (FAQ)"])
    
    st.markdown("---")
    st.markdown("""<div class="footer-text"><b>CABA:</b> Av. Rivadavia 4532 (L. 10)<br><b>Leloir:</b> Del Cimarrón 1846 (Of. 4)<br><b>WA:</b> (011) 5609-6283</div>""", unsafe_allow_html=True)

# 4. Contenido
df = pd.DataFrame(data_cba if destino == "VILLA CARLOS PAZ" else data_sp)

if seccion == "Planes y Costos":
    st.header(f"Costos y Comparativa - {destino}")
    sel_p = st.selectbox("Plan seleccionado:", df["Programa"])
    v = df[df["Programa"] == sel_p].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Valor Lista", f"$ {v['Total']:,}")
    c2.metric("Pago Contado", f"$ {v['Contado']:,}", f"- $ {v['Total']-v['Contado']:,} Ahorro")
    c3.metric("Reserva / Inscripción", f"$ {v['Inscripcion']:,}")

    st.subheader("🔍 Tabla Comparativa")
    df_comp = df[df["Programa"] != sel_p].copy()
    df_comp["Dif. Contado"] = df_comp["Contado"] - v["Contado"]
    df_comp["Dif. Lista"] = df_comp["Total"] - v["Total"]
    st.dataframe(df_comp[["Programa", "Total", "Dif. Lista", "Contado", "Dif. Contado"]].style.format({"Total": "$ {:,.0f}", "Contado": "$ {:,.0f}", "Dif. Lista": "{:+,.0f}", "Dif. Contado": "{:+,.0f}"}), use_container_width=True)

elif seccion == "Ficha de Preventa":
    st.header("📝 Ficha de Inscripción Preventa")
    with st.form("form_preventa"):
        c1, c2 = st.columns(2)
        with c1:
            nombre_a = st.text_input("Nombre del Alumno")
            dni_a = st.text_input("DNI del Alumno")
            colegio = st.text_input("Colegio")
        with c2:
            apellido_a = st.text_input("Apellido del Alumno")
            padre_madre = st.text_input("Nombre Padre/Madre/Tutor")
            tel_emergencia = st.text_input("Teléfono de Emergencia")
        
        observaciones = st.text_area("Observaciones Médicas / Dietas (Ej: Celíaco, Alérgico a penicilina, etc.)")
        
        plan_elegido = st.selectbox("Plan de Pago Seleccionado", df["Programa"])
        v_p = df[df["Programa"] == plan_elegido].iloc[0]
        metodo_pago = st.radio("Modalidad", ["Contado", "Plan Mixto (Cuotas Fijas + IPC)"])
        
        submit = st.form_submit_button("Generar Ficha")

    if submit:
        st.success("Ficha generada con éxito.")
        resumen_html = f"""
        <div style="border: 2px solid #333; padding: 20px; font-family: sans-serif; background-color: white;">
            <h2 style="text-align: center; color: #d32f2f;">FICHA DE PREVENTA - SERRANO TURISMO</h2>
            <p><b>Alumno:</b> {nombre_a} {apellido_a} | <b>DNI:</b> {dni_a}</p>
            <p><b>Observaciones:</b> {observaciones}</p>
            <hr>
            <h4>VIAJE: {destino.upper()} | Plan: {plan_elegido}</h4>
            <p><b>Modalidad:</b> {metodo_pago} | <b>Inscripción:</b> $ {v_p['Inscripcion']:,}</p>
        </div>
        """
        st.markdown(resumen_html, unsafe_allow_html=True)
        
        # WA link con observaciones
        wa_txt = f"PREVENTA: {nombre_a} {apellido_a}. Colegio: {colegio}. Plan: {plan_elegido}. Obs: {observaciones}."
        st.markdown(f'<a href="https://api.whatsapp.com/send?phone=5491167877990&text={wa_txt.replace(" ", "%20")}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">📲 Enviar Ficha Médica y Plan a Martín</button></a>', unsafe_allow_html=True)

    st.markdown('<div class="disclaimer"><b>DISCLAIMER:</b> La presente ficha es informativa y de preventa. No sustituye el contrato legal de turismo estudiantil[cite: 1, 2].</div>', unsafe_allow_html=True)

elif seccion == "Checklist Documentación":
    st.header("📋 Requisitos para el Viaje")
    st.write("Marque los elementos que ya posee para organizar su carpeta:")
    st.checkbox("DNI Original y actualizado al momento del viaje ")
    st.checkbox("Ficha Médica firmada por pediatra/médico ")
    st.checkbox("Autorización de viaje firmada por padres ante escribano/juez ")
    st.checkbox("Contrato de adhesión firmado [cite: 1]")
    st.info("Toda la documentación debe entregarse en las oficinas de Serrano Turismo 30 días antes de la salida.")

elif seccion == "Información Útil (FAQ)":
    st.header("❓ Preguntas Frecuentes")
    with st.expander("¿Cómo veo las fotos de mi hijo durante el viaje?"):
        st.write("A través de la App **Viaxlab**. Recibirá una pulsera inteligente con tecnología NFC para seguimiento y fotos en tiempo real.")
    with st.expander("¿Qué incluye la pensión completa?"):
        st.write("Desayuno buffet, almuerzo y cena con menú de 3 pasos y gaseosas de primera marca ilimitadas durante las comidas.")
    with st.expander("¿Cuál es la cobertura médica?"):
        st.write("Contamos con **Universal Assistance**, que ofrece asistencia médica completa, farmacia y seguimiento post-viaje.")
