import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard de Calidad", page_icon="📊", layout="wide"
)

st.title("📊 Indicadores del Sistema de Gestión de Calidad")

# Subir el archivo CSV directamente en la web
archivo_subido = st.file_uploader(
    "Sube tu archivo 'datos_calidad.csv'", type=["csv"]
)

if archivo_subido is not None:
  df = pd.read_csv(archivo_subido)

  # Filtros
  proceso = st.selectbox(
      "Seleccionar Proceso:", options=["Todos"] + list(df["Proceso"].unique())
  )
  if proceso != "Todos":
    df = df[df["Proceso"] == proceso]

  # Métricas superiores
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Registros", len(df))
  col2.metric("Cumplidos", len(df[df["Estado"] == "Cumplido"]))
  col3.metric(
      "Eficacia",
      f"{(len(df[df['Estado'] == 'Cumplido']) / len(df) * 100):.1f}%"
      if len(df) > 0
      else "0%",
  )

  st.markdown("---")

  # Gráfico
  fig = px.bar(
      df,
      x="Mes",
      y="Real",
      color="Indicador",
      barmode="group",
      title="Desempeño por Indicador",
  )
  st.plotly_chart(fig, use_container_width=True)

  # Tabla
  st.dataframe(df)
else:
  st.info(
      "Por favor, sube el archivo 'datos_calidad.csv' que descargaste de Google"
      " Sheets para ver el dashboard."
  )
