import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Reporte Ensamble CTG", layout="wide")

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

# Base de datos temporal en la sesión
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Fecha", "Turno", "Categoría", "Detalle", "Firma", "KING", "C200", "C300"])

st.title("📋 Reporte de Novedades Ensamble Motocarros")

# --- DASHBOARD DE METAS ---
st.subheader("🎯 Cumplimiento de Metas Mensuales")
cols_m = st.columns(3)
for i, (mod, meta) in enumerate(METAS.items()):
    col_ref = "KING" if "KING" in mod else ("C200" if "200" in mod else "C300")
    acumulado = st.session_state.db[col_ref].sum() if not st.session_state.db.empty else 0
    with cols_m[i]:
        st.metric(mod, f"{int(acumulado)} / {meta}", f"Restante: {int(meta-acumulado)}")
        st.progress(min(acumulado/meta, 1.0))

st.divider()

# --- FORMULARIO DINÁMICO ---
with st.form("main_form", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    with col_a: turno = st.selectbox("Momento del Reporte", ["Inicio de Turno", "Final de Turno"])
    with col_b: categoria = st.selectbox("Tipo de Novedad", 
                             ["Personas", "Unidades Notificadas", "Ocupación", "Soltrech", 
                              "Desempaque", "Ensamble", "Calidad", "Herramientas", "Ajustes", "Seguridad"])
    
    st.markdown(f"### Detalles de la Categoría: **{categoria}**")
    detalle_final = ""
    u_k, u_2, u_3 = 0, 0, 0

    # LÓGICA DE CAMPOS SEGÚN CATEGORÍA
    if categoria == "Personas":
        asistencia_log = []
        for p in PERSONAL:
            c_p1, c_p2 = st.columns([1, 2])
            with c_p1:
                esta = st.checkbox(f"Presente", value=True, key=f"p_{p}")
            with c_p2:
                if not esta:
                    motivo = st.text_input(f"Motivo ausencia: {p}", key=f"mot_{p}")
                    asistencia_log.append(f"{p}: Ausente ({motivo})")
                else:
                    st.write(f"✅ {p}")
        detalle_final = " | ".join(asistencia_log) if asistencia_log else "Todo el personal presente."

    elif categoria == "Unidades Notificadas":
        cx, cy, cz = st.columns(3)
        u_k = cx.number_input("KING DELUXE", min_value=0, step=1)
        u_2 = cy.number_input("CERONTE 200", min_value=0, step=1)
        u_3 = cz.number_input("CERONTE 300", min_value=0, step=1)
        detalle_final = "Unidades terminadas reportadas."

    elif categoria == "Ocupación":
        q1 = st.number_input("¿Cuántas unidades de King hay almacenadas?", min_value=0)
        q2 = st.number_input("¿Cuántas unidades de Ceronte 300 hay almacenadas?", min_value=0)
        q3 = st.number_input("¿Cuántas unidades de Ceronte 200 hay almacenadas?", min_value=0)
        detalle_final = f"Stock -> King:{q1}, C300:{q2}, C200:{q3}"

    elif categoria == "Soltrech":
        s1 = st.number_input("¿Cuántos motocarros hay en cabina?", min_value=0)
        s2 = st.number_input("¿Cuántos motocarros hay en horno?", min_value=0)
        s3 = st.number_input("¿Cuántos motocarros hay en superficies?", min_value=0)
        s4 = st.number_input("¿Cuántos motocarros hay en reproceso?", min_value=0)
        detalle_final = f"Soltrech -> Cab:{s1}, Horno:{s2}, Sup:{s3}, Rep:{s4}"

    else:
        detalle_final = st.text_area("Comentarios", placeholder="Escriba aquí las novedades del proceso...")

    st.divider()
    firma = st.selectbox("Quién diligencia el reporte (Firma)", PERSONAL)
    
    if st.form_submit_button("Registrar Novedad"):
        nuevo = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Turno": turno,
            "Categoría": categoria,
            "Detalle": detalle_final,
            "Firma": firma,
            "KING": u_k,
            "C200": u_2,
            "C300": u_3
        }
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo])], ignore_index=True)
        st.success("✅ Datos guardados correctamente.")
        st.rerun()

# --- HISTORIAL ---
if not st.session_state.db.empty:
    st.divider()
    st.subheader("📊 Historial Registrado")
    st.dataframe(st.session_state.db, use_container_width=True)
    
    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Descargar CSV", data=csv, file_name=f"reporte_{datetime.now().date()}.csv", mime='text/csv')
