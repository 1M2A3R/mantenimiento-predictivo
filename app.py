import streamlit as st
import pandas as pd
import numpy as np

st.title("🚗 Simulador de Mantenimiento Predictivo")

# Datos sintéticos
rpm = st.slider("RPM del motor", 800, 5000, 2500)
temperatura = st.slider("Temperatura (°C)", 70, 120, 85)

# Lógica de predicción
if temperatura > 100:
    st.error("🔥 ¡ALERTA! Fallo inminente (Temperatura crítica)")
elif temperatura > 90:
    st.warning("⚠️ Advertencia: Motor en riesgo")
else:
    st.success("✅ Estado normal")

# Gráfico
datos = pd.DataFrame({"RPM": [rpm], "Temperatura": [temperatura]})
st.bar_chart(datos)
