import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Calidad - FELOSOTEC", page_icon="📊", layout="wide"
)

st.title("📊 Indicadores del Sistema de Gestión de Calidad (ISO 9001)")
st.markdown("Panel de control dinámico basado en la matriz de procesos.")

# Subir archivo CSV de datos
archivo_subido = st.file_uploader(
    "Sube tu archivo 'datos_calidad.csv' actualizado", type=["csv"]
)

if archivo_subido is not None:
  df = pd.read_csv(archivo_subido)

  # Filtros laterales
  st.sidebar.header("Filtros de Análisis")
  proceso_seleccionado = st.sidebar.selectbox(
      "Seleccionar Proceso:", options=["Todos"] + list(df["Proceso"].unique())
  )

  if proceso_seleccionado != "Todos":
    df_filtrado = df[df["Proceso"] == proceso_seleccionado]
  else:
    df_filtrado = df

  # Tarjetas de Resumen (KPIs)
  st.subheader("Resumen General de Gestión")
  col1, col2, col3, col4 = st.columns(4)

  total_registros = len(df_filtrado)
  cumplidos = len(df_filtrado[df_filtrado["Estado"] == "Cumplido"])
  eficacia = (
      (cumplidos / total_registros) * 100 if total_registros > 0 else 0
  )

  col1.metric("Total Indicadores Evaluados", total_registros)
  col2.metric("Indicadores Cumplidos", cumplidos)
  col3.metric("Eficacia del SGC", f"{eficacia:.1f}%")
  col4.metric(
      "Proceso Activo",
      proceso_seleccionado if proceso_seleccionado != "Todos" else "General",
  )

  st.markdown("---")

  # Gráfico interactivo
  st.subheader("Desempeño Real vs. Meta")
  fig = px.bar(
      df_filtrado,
      x="Indicador",
      y="Real",
      color="Estado",
      text="Real",
      barmode="group",
      title="Comparativa de Indicadores de Calidad",
      labels={"Real": "Valor Alcanzado", "Indicador": "Indicador SGC"},
  )
  fig.update_traces(textposition="outside")
  fig.update_layout(xaxis_tickangle=-25, height=500)
  st.plotly_chart(fig, use_container_width=True)

  # Tabla detallada
  st.subheader("Detalle de Registros de Calidad")
  st.dataframe(df_filtrado, use_container_width=True)

else:
  st.info(
      "👆 Por favor, sube tu archivo CSV con los datos de tu matriz de calidad"
      " para visualizar el panel interactivo."
  )
