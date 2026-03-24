import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="CTG Motocarros Cloud", layout="wide")

METAS = {"KING DELUXE": 120, "CERONTE 200": 80, "CERONTE 300": 60}
PERSONAL = [
    "ADRIAN ANAYA AVILA", "ALBERTO PAUTT CARABALLO", "ALVAREZ SANES LUIS FERNANDO",
    "ALVIS OVIEDO JERELYN SOFIA", "BRANDON PADILLA TORRES", "BRANDT MENDOZA IAN CARLOS",
    "CALY TORRES DANIEL ANTONIO", "CANTILLO CANO LUIS DAVID", "CARABALLO CERVANTES YORDI",
    "CARMELO JOSE LLERENA PEREZ", "CASSIANI HERRERA YOSEFER DE JESUS", "CASTILLO PATERNINA HAROLD",
    "CASTRO MIRANDA SANTIAGO", "CASTRO VELASQUEZ JOSE ALEJANDRO", "COWAN PEREIRA DUVAN ORLANDO",
    "DURANGO CAMPO JESUS", "FONTALVO PEREZ LUIS EDUARDO", "GARAY RAMIREZ ANDRES",
    "HARRINSSON DEL RIO GARCIA", "HURTADO BARRERA CARLOS RAFAEL", "HURTADO ZUÑIGA JUAN CAMILO",
    "IZQUIERDO FERIA EDER LUIS", "JIMENEZ VALDELAMAR MILTON ENRIQUE", "JOHANN DAVID LAZA SANTOS",
    "MACIAS LUNA ANDRES FELIPE", "MARRUGO CARRILLO RAUL", "MATOREL CARDONA LUIS MARIO",
    "MATURANA MEZA CARLOS MARIO", "MAZA RODRIGUEZ MAURO ENRIQUE", "MORENO JIMENEZ FABIO",
    "NEIRA MARIN JANER ANDREY", "ORTIZ CANO JHON JAIRO", "PAJARO CARDENAS NILSON",
    "PEÑA GUTIERREZ ELKIN ANTONIO", "PEÑAFIEL SIMANCAS MARTIN JOSE", "RODRIGUEZ BANQUETT ROGER",
    "SANTOYA OVIEDO LUIS MIGUEL", "TORRES TORRES CRISTIAN ANDRES", "VISBAL RIOS LUIS ENRIQUE"
]

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Fecha", "Turno", "Categoría", "Detalle", "Firma", "KING", "C200", "C300"])

# --- INTERFAZ ---
st.title("📋 Gestión de Ensamble - Motocarros CTG")

# Dashboard de Metas
st.subheader("🎯 Progreso Mensual")
cols = st.columns(3)
for i, (mod, meta) in enumerate(METAS.items()):
    col_ref = "KING" if "KING" in mod else ("C200" if "200" in mod else "C300")
    acumulado = st.session_state.db[col_ref].sum() if not st.session_state.db.empty else 0
    with cols[i]:
        st.metric(mod, f"{int(acumulado)}/{meta}", f"-{int(meta-acumulado)}")
        st.progress(min(acumulado/meta, 1.0))

st.divider()

# Formulario
with st.form("registro"):
    c1, c2 = st.columns(2)
    turno = c1.selectbox("Turno", ["Inicio", "Fin"])
    cat = c2.selectbox("Categoría", ["Unidades Notificadas", "Personas", "Calidad", "Soltrech", "Otros"])
    
    u_k, u_2, u_3 = 0, 0, 0
    det = ""

    if cat == "Unidades Notificadas":
        cx, cy, cz = st.columns(3)
        u_k = cx.number_input("KING", min_value=0)
        u_2 = cy.number_input("C200", min_value=0)
        u_3 = cz.number_input("C300", min_value=0)
    elif cat == "Personas":
        presentes = 0
        for p in PERSONAL:
            if st.checkbox(p, value=True): presentes += 1
        det = f"Ausentismo: {((len(PERSONAL)-presentes)/len(PERSONAL))*100:.1f}%"
    else:
        det = st.text_area("Comentarios")

    firma = st.selectbox("Firma", PERSONAL)
    if st.form_submit_button("Guardar Reporte"):
        nuevo = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Turno": turno, "Categoría": cat, 
                 "Detalle": det, "Firma": firma, "KING": u_k, "C200": u_2, "C300": u_3}
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo])], ignore_index=True)
        st.success("Registrado correctamente")

# Historial y Descarga
if not st.session_state.db.empty:
    st.divider()
    st.subheader("📊 Historial del Día")
    st.dataframe(st.session_state.db)
    
    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Descargar Excel (CSV)", data=csv, file_name="reporte_ctg.csv", mime='text/csv')