import streamlit as st
import pandas as pd

# 1. Configuración de Estética Profesional
st.set_page_config(page_title="Serrano Turismo | Catálogo y Preventa", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .footer-text { font-size: 0.8rem; color: #6c757d; line-height: 1.4; }
    @media print {
        .no-print { display: none !important; }
        .print-only { display: block !important; }
    }
    .print-only { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
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
    seccion = st.selectbox("DETALLES DEL VIAJE", ["Planes y Costos", "Formulario de Preventa", "Hotelería", "Excursiones", "Seguridad"])

    st.markdown("---")
    st.markdown("""<div class="footer-text"><b>Oficinas CABA:</b> Av. Rivadavia 4532 (L. 10)<br><b>Oficinas Leloir:</b> Del Cimarrón 1846 (Of. 4)<br><b>Tel:</b> (011) 4847-6467 / 5609-6283</div>""", unsafe_allow_html=True)

# 4. Lógica de Contenido
df = pd.DataFrame(data_cba if destino == "VILLA CARLOS PAZ" else data_sp)

if seccion == "Planes y Costos":
    st.header(f"Costos y Comparativa - {destino}")
    sel_p = st.selectbox("Plan seleccionado:", df["Programa"])
    v = df[df["Programa"] == sel_p].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Valor Lista", f"$ {v['Total']:,}")
    c2.metric("Pago Contado", f"$ {v['Contado']:,}", f"- $ {v['Total']-v['Contado']:,} Ahorro")
    c3.metric("Reserva / Inscrip.", f"$ {v['Inscripcion']:,}")

    st.subheader("🔍 Comparativa con otras alternativas")
    df_comp = df[df["Programa"] != sel_p].copy()
    df_comp["Dif. Contado"] = df_comp["Contado"] - v["Contado"]
    df_comp["Dif. Lista"] = df_comp["Total"] - v["Total"]
    st.dataframe(df_comp[["Programa", "Total", "Dif. Lista", "Contado", "Dif. Contado"]].style.format({"Total": "$ {:,.0f}", "Contado": "$ {:,.0f}", "Dif. Lista": "{:+,.0f}", "Dif. Contado": "{:+,.0f}"}), use_container_width=True)

elif seccion == "Formulario de Preventa":
    st.header("📝 Formulario de Selección de Plan")
    st.write("Complete los datos para generar el comprobante de preventa.")
    
    with st.form("form_impresion"):
        col1, col2 = st.columns(2)
        with col1:
            nombre_a = st.text_input("Nombre del Alumno")
            apellido_a = st.text_input("Apellido del Alumno")
            dni_a = st.text_input("DNI del Alumno")
        with col2:
            colegio = st.text_input("Colegio / Institución")
            padre = st.text_input("Nombre Padre o Tutor")
            madre = st.text_input("Nombre Madre o Tutora")
        
        plan_elegido = st.selectbox("Plan de Pago Seleccionado", df["Programa"])
        v_p = df[df["Programa"] == plan_elegido].iloc[0]
        
        metodo_pago = st.radio("Modalidad de Pago", ["Contado", "Plan Mixto (Cuotas Fijas + IPC)"])
        
        submit = st.form_submit_button("Generar Vista de Impresión")

    if submit:
        st.success("¡Formulario listo! Use el botón de abajo para imprimir o guardar como PDF.")
        
        # Bloque de impresión (HTML)
        resumen_html = f"""
        <div style="border: 2px solid #333; padding: 20px; font-family: sans-serif;">
            <h2 style="text-align: center; color: #d32f2f;">COMPROBANTE DE PREVENTA 2026/27</h2>
            <hr>
            <h4>DATOS DEL ALUMNO</h4>
            <p><b>Nombre:</b> {nombre_a} {apellido_a} | <b>DNI:</b> {dni_a}</p>
            <p><b>Institución:</b> {colegio}</p>
            <h4>DATOS DE TUTORES</h4>
            <p><b>Padre/Tutor:</b> {padre} | <b>Madre/Tutora:</b> {madre}</p>
            <hr>
            <h4>DETALLE DEL VIAJE: {destino.upper()}</h4>
            <p><b>Plan seleccionado:</b> {plan_elegido}</p>
            <p><b>Modalidad:</b> {metodo_pago}</p>
            <p><b>Inscripción/Reserva:</b> $ {v_p['Inscripcion']:,}</p>
            <p><b>Valor de Referencia:</b> $ {v_p['Contado'] if metodo_pago == 'Contado' else v_p['Total']:,}</p>
            <br><br>
            <div style="display: flex; justify-content: space-between;">
                <div style="border-top: 1px solid #000; width: 40%; text-align: center;"><p>Firma Padre/Madre</p></div>
                <div style="border-top: 1px solid #000; width: 40%; text-align: center;"><p>Serrano Turismo</p></div>
            </div>
        </div>
        """
        st.markdown(resumen_html, unsafe_allow_html=True)
        st.button("🖨️ Click derecho en la página y elija 'Imprimir'", help="O presione Ctrl+P")

elif seccion == "Hotelería":
    st.header("Alojamiento")
    if destino == "VILLA CARLOS PAZ":
        st.write("Hoteles Parque y Capilla del Lago[cite: 1].")
    else:
        st.write("Hotel Turismo San Pedro - La Rueda[cite: 2].")

elif seccion == "Excursiones":
    st.header("Actividades")
    if destino == "VILLA CARLOS PAZ":
        st.write("- Peko's Multiparque [cite: 1]\n- Mundo Cocoguana [cite: 1]")
    else:
        st.write("- La Campiña de Mónica y César [cite: 2]\n- Vuelta al Obligado [cite: 2]")

elif seccion == "Seguridad":
    st.header("Cobertura")
    st.write("Universal Assistance y App Viaxlab.")

# WhatsApp Flotante
msg = f"Hola Martín, envío datos de preventa para {destino}."
st.sidebar.markdown(f"""<a href="https://api.whatsapp.com/send?phone=5491167877990&text={msg.replace(' ', '%20')}" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:10px; cursor:pointer;">Enviar Consulta por WA</button></a>""", unsafe_allow_html=True)
