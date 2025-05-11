import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  # Para gráficos interactivos

# Configuración de la página
st.set_page_config(page_title="📊 Mantenimiento Predictivo Avanzado", layout="wide")

# Título
st.title("🚗 Simulador de Mantenimiento Predictivo")
st.markdown("---")

# 1. Datos sintéticos (simulación de sensores)
np.random.seed(42)
horas = np.arange(0, 24)
rpm = np.random.normal(2500, 300, 24)
temperatura = np.random.normal(85, 10, 24)
vibracion = np.random.exponential(0.3, 24)

df = pd.DataFrame({
    "Hora": horas,
    "RPM": rpm,
    "Temperatura (°C)": temperatura,
    "Vibración (g)": vibracion
})

# 2. Controles interactivos
st.sidebar.header("🔧 Configuración")
temp_umbral = st.sidebar.slider("Umbral de temperatura crítica (°C)", 80, 120, 100)
vib_umbral = st.sidebar.slider("Umbral de vibración crítica (g)", 0.1, 1.0, 0.5)

# 3. Gráficas interactivas con Plotly
col1, col2 = st.columns(2)

with col1:
    st.header("📈 RPM vs. Temperatura")
    fig1 = px.scatter(
        df, x="Hora", y="RPM", color="Temperatura (°C)",
        color_continuous_scale="reds",
        title="Relación RPM/Temperatura por Hora"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.header("📉 Vibración del Motor")
    fig2 = px.line(
        df, x="Hora", y="Vibración (g)",
        title="Vibración a lo largo del tiempo",
        markers=True
    )
    fig2.add_hline(y=vib_umbral, line_dash="dash", line_color="red")
    st.plotly_chart(fig2, use_container_width=True)

# 4. Alertas basadas en umbrales
st.markdown("---")
st.header("🚨 Alertas en Tiempo Real")

alerta_temp = (df["Temperatura (°C)"] > temp_umbral).any()
alerta_vib = (df["Vibración (g)"] > vib_umbral).any()

if alerta_temp and alerta_vib:
    st.error("🔥🚨 *CRÍTICO*: Temperatura y vibración exceden umbrales")
elif alerta_temp:
    st.error("🔥 *ALERTA*: Temperatura crítica detectada")
elif alerta_vib:
    st.warning("⚠️ *ADVERTENCIA*: Vibración elevada")
else:
    st.success("✅ *NORMAL*: Todos los parámetros están dentro de rangos seguros")

# 5. Gráfico de correlación adicional
st.header("📊 Correlación entre Variables")
fig3 = px.scatter_matrix(
    df, dimensions=["RPM", "Temperatura (°C)", "Vibración (g)"],
    color="Hora", title="Matriz de Correlación"
)
st.plotly_chart(fig3, use_container_width=True)
