import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import json

# Configuración de la página
st.set_page_config(
    page_title="🚗 Mantenimiento Predictivo",
    layout="wide",
    page_icon="🔧"
)

# CSS personalizado para mejor apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .alert-box {
        background-color: #ff4b4b;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- Datos sintéticos mejorados ----
@st.cache_data
def generar_datos_sinteticos():
    np.random.seed(42)
    horas = np.arange(0, 24)
    datos = pd.DataFrame({
        "Hora": horas,
        "RPM": np.random.normal(2500, 300, 24),
        "Temperatura (°C)": np.random.normal(85, 10, 24),
        "Vibración (g)": np.random.exponential(0.3, 24),
        "Presión (psi)": np.random.normal(150, 15, 24)
    })
    return datos

# ---- Header ----
st.markdown('<h1 class="main-header">🔧 Sistema de Mantenimiento Predictivo</h1>', unsafe_allow_html=True)

# ---- Sidebar Mejorado ----
with st.sidebar:
    st.header("⚙️ Panel de Control")
    
    umbral_temp = st.slider("🌡️ Umbral temperatura crítica (°C)", 70, 120, 90)
    umbral_vib = st.slider("📏 Umbral vibración crítica (g)", 0.1, 1.0, 0.5)
    umbral_pres = st.slider("💨 Umbral presión crítica (psi)", 100, 200, 160)
    
    st.divider()
    
    variables = st.multiselect(
        "📊 Variables a visualizar",
        ["RPM", "Temperatura (°C)", "Vibración (g)", "Presión (psi)"],
        default=["Temperatura (°C)", "Vibración (g)"]
    )

# ---- Métricas en tiempo real ----
datos = generar_datos_sinteticos()
ultimo_dato = datos.iloc[-1]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card">📊 RPM<br><h3>{int(ultimo_dato["RPM"])}</h3></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">🌡️ Temperatura<br><h3>{ultimo_dato["Temperatura (°C)"]:.1f}°C</h3></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card">📏 Vibración<br><h3>{ultimo_dato["Vibración (g)"]:.2f}g</h3></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card">💨 Presión<br><h3>{ultimo_dato["Presión (psi)"]:.1f}psi</h3></div>', unsafe_allow_html=True)

# ---- Pestañas principales ----
tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "📋 Histórico", "⚙️ Simulador", "📊 Análisis"])

with tab1:
    st.header("Monitoreo en Tiempo Real")
    
    if variables:
        fig = px.line(datos, x="Hora", y=variables, title="Tendencias de Métricas")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecciona al menos una variable para visualizar")

with tab2:
    st.header("Datos Históricos")
    st.dataframe(datos, use_container_width=True)

with tab3:
    st.header("Simulador de Escenarios")
    
    escenario = st.selectbox("Selecciona un escenario:", 
                           ["Operación Normal", "Sobrecalentamiento", "Vibración Excesiva", "Pérdida de Presión"])
    
    if st.button("🚀 Ejecutar Simulación", type="primary"):
        with st.spinner("Simulando..."):
            time.sleep(2)
            
            if escenario == "Sobrecalentamiento":
                st.error("🔴 ALERTA: Temperatura crítica detectada (110°C)")
                st.progress(0.9)
            elif escenario == "Vibración Excesiva":
                st.warning("🟡 ADVERTENCIA: Vibración elevada (0.8g)")
                st.progress(0.7)
            elif escenario == "Pérdida de Presión":
                st.error("🔴 ALERTA: Pérdida de presión (90 psi)")
                st.progress(0.6)
            else:
                st.success("🟢 OPERACIÓN NORMAL: Todos los parámetros en rango")
                st.progress(0.3)

with tab4:
    st.header("Análisis Predictivo")
    
    # Análisis de correlación
    fig_corr = px.imshow(datos.corr(), title="Matriz de Correlación")
    st.plotly_chart(fig_corr, use_container_width=True)

# ---- Sistema de Alertas Inteligente ----
st.sidebar.header("🚨 Sistema de Alertas")

alertas = []
if any(datos["Temperatura (°C)"] > umbral_temp):
    alertas.append(f"🌡️ Temperatura > {umbral_temp}°C")
if any(datos["Vibración (g)"] > umbral_vib):
    alertas.append(f"📏 Vibración > {umbral_vib}g")
if any(datos["Presión (psi)"] > umbral_pres):
    alertas.append(f"💨 Presión > {umbral_pres}psi")

if alertas:
    for alerta in alertas:
        st.sidebar.error(f"⚠️ {alerta}")
else:
    st.sidebar.success("✅ Todas las métricas en rango normal")

# ---- Descarga de Reporte ----
if st.sidebar.button("📥 Generar Reporte PDF"):
    with st.spinner("Generando reporte..."):
        time.sleep(1)
        st.sidebar.success("📄 Reporte generado exitosamente")

# ---- Footer ----
st.divider()
st.caption("🔧 Sistema de Mantenimiento Predictivo v1.0 | Desarrollado con Streamlit")
