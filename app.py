import streamlit as st
import pandas as pd

# 1. Configuración de Estética Profesional
st.set_page_config(page_title="Serrano Turismo | Catálogo y Preventa", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .footer-text { font-size: 0.8rem; color: #6c757d; line-height: 1.4; }
    .disclaimer { font-size: 0.75rem; color: #7f8c8d; text-align: justify; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    @media print { .no-print { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos (Villa Carlos Paz y San Pedro)
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
    seccion = st.selectbox("DETALLES DEL VIAJE", ["Planes y Costos", "Formulario de Preventa", "Hotelería", "Excursiones"])
    
    st.markdown("---")
    st.markdown("""<div class="footer-text"><b>CABA:</b> Av. Rivadavia 4532 (L. 10)<br><b>Leloir:</b> Del Cimarrón 1846 (Of. 4)<br><b>WA:</b> (011) 5609-6283</div>""", unsafe_allow_html=True)

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
    st.header("📝 Formulario de Preventa 2026/27")
    st.write("Complete los datos del pasajero y tutores para generar el resumen de inscripción.")
    
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
        
        submit = st.form_submit_button("Generar Resumen para Impresión")

    if submit:
        # Bloque de impresión (HTML)
        resumen_html = f"""
        <div style="border: 2px solid #333; padding: 20px; font-family: sans-serif; background-color: white;">
            <h2 style="text-align: center; color: #d32f2f;">FICHA DE PREVENTA - SERRANO TURISMO</h2>
            <hr>
            <p><b>Alumno:</b> {nombre_a} {apellido_a} | <b>DNI:</b> {dni_a} | <b>Colegio:</b> {colegio}</p>
            <p><b>Tutores:</b> {padre} / {madre}</p>
            <hr>
            <h4>DETALLE DEL VIAJE</h4>
            <p><b>Destino:</b> {destino.upper()} | <b>Programa:</b> {plan_elegido}</p>
            <p><b>Modalidad:</b> {metodo_pago} | <b>Inscripción:</b> $ {v_p['Inscripcion']:,}</p>
            <p><b>Valor Referencial:</b> $ {v_p['Contado'] if metodo_pago == 'Contado' else v_p['Total']:,}</p>
            <br><br>
            <div style="display: flex; justify-content: space-between;">
                <div style="border-top: 1px solid #000; width: 40%; text-align: center;"><p>Firma de Conformidad</p></div>
                <div style="border-top: 1px solid #000; width: 40%; text-align: center;"><p>Serrano Turismo</p></div>
            </div>
        </div>
        """
        st.markdown(resumen_html, unsafe_allow_html=True)
        
        # WhatsApp con datos del formulario
        wa_data = f"PREVENTA: {nombre_a} {apellido_a} ({colegio}). Destino: {destino}. Plan: {plan_elegido}. Modalidad: {metodo_pago}."
        url_wa_form = f"https://api.whatsapp.com/send?phone=5491167877990&text={wa_data.replace(' ', '%20')}"
        st.markdown(f'<a href="{url_wa_form}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; margin-top:10px;">📲 Enviar Ficha a Martín por WhatsApp</button></a>', unsafe_allow_html=True)
        st.caption("Nota: Presione Ctrl+P (Windows) o Cmd+P (Mac) para imprimir esta ficha.")

    # --- DISCLAIMER LEGAL ---
    st.markdown("""
    <div class="disclaimer">
    <b>TÉRMINOS Y CONDICIONES PRELIMINARES:</b><br>
    El presente documento reviste carácter de "Ficha de Preventa" y declaración de interés, no constituyendo por sí mismo un contrato de viaje estudiantil definitivo. 
    La validez del plan de pagos y la reserva de la plaza están sujetas a: 1) La disponibilidad de cupos al momento de la ratificación. 2) La firma del Contrato de Adhesión bajo la normativa vigente de la Ley de Turismo Estudiantil. 3) El pago efectivo de la cuota de inscripción/inscripción detallada. 
    Los valores expresados en el "Plan Mixto" son de carácter referencial y se ajustarán mensualmente según el Índice de Precios al Consumidor (IPC) informado por el INDEC, a partir de la cuota detallada en el plan elegido. Serrano Turismo se reserva el derecho de ajustar itinerarios por razones de fuerza mayor, garantizando siempre la calidad y seguridad de los servicios prestados.
    </div>
    """, unsafe_allow_html=True)

elif seccion == "Hotelería":
    st.header(f"Alojamiento - {destino}")
    if destino == "VILLA CARLOS PAZ":
        st.write("- **Hoteles:** Parque y Capilla del Lago .\n- **Servicios:** Habitaciones con somier, aire acondicionado y baño privado[cite: 3].")
    else:
        st.write("- **Hotel:** Turismo San Pedro (La Rueda) [cite: 2].\n- **Servicios:** Pileta climatizada exclusiva y amplios parques[cite: 2].")

elif seccion == "Excursiones":
    st.header(f"Experiencias - {destino}")
    if destino == "VILLA CARLOS PAZ":
        st.write("- **Parques:** Peko's Multiparque y Mundo Cocoguana [cite: 3].\n- **Noche:** Discotecas exclusivas y fiestas temáticas[cite: 3].")
    else:
        st.write("- **Visitas:** La Campiña de Mónica y César y Vuelta al Obligado [cite: 2].\n- **Aventura:** Navegación por el Delta y safari fotográfico[cite: 2].")
