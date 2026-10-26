import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página con diseño ancho
st.set_page_config(
    page_title="Gestión de Calidad - FELOSOTEC", page_icon="📊", layout="wide"
)

# Estilo visual moderno / oscuro estilo NOC
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📊 Sistema de Gestión de Calidad - Panel General")
st.markdown("Control histórico de indicadores: Todos los años y meses.")

# Subir archivo CSV de datos
archivo_subido = st.file_uploader(
    "Sube tu archivo CSV con el histórico de indicadores", type=["csv"]
)

if archivo_subido is not None:
  df = pd.read_csv(archivo_subido, encoding="latin1")

  # Barra de filtros superior (Filtros dinámicos por Año, Mes y Proceso)
  st.markdown("---")
  f1, f2, f3 = st.columns(3)

  with f1:
    anos_disponibles = ["Todos"] + list(df["Ano"].astype(str).unique())
    ano_sel = st.selectbox("📅 Seleccionar Año:", options=anos_disponibles)

  with f2:
    meses_disponibles = ["Todos"] + list(df["Mes"].unique())
    mes_sel = st.selectbox("🗓️ Seleccionar Mes:", options=meses_disponibles)

  with f3:
    procesos_disponibles = ["Todos"] + list(df["Proceso"].unique())
    proceso_sel = st.selectbox(
        "⚙️ Seleccionar Proceso:", options=procesos_disponibles
    )

  # Aplicar filtros al DataFrame
  df_filtrado = df.copy()
  if ano_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Ano"].astype(str) == ano_sel]
  if mes_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mes"] == mes_sel]
  if proceso_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Proceso"] == proceso_sel]

  # Tarjetas de Resumen (KPI Cards superiores)
  st.markdown("### 📌 Indicadores Clave del Periodo")
  c1, c2, c3, c4 = st.columns(4)

  total_registros = len(df_filtrado)
  cumplidos = len(df_filtrado[df_filtrado["Estado"] == "Cumplido"])
  en_riesgo = len(df_filtrado[df_filtrado["Estado"] == "En Riesgo"])
  eficacia = (
      (cumplidos / total_registros) * 100 if total_registros > 0 else 0
  )

  c1.metric("TOTAL REGISTROS", total_registros)
  c2.metric("🟢 CUMPLIDOS", cumplidos)
  c3.metric("🟡 EN RIESGO", en_riesgo)
  c4.metric("📊 EFICACIA GLOBAL", f"{eficacia:.1f}%")

  st.markdown("---")

  # Gráfico de evolución temporal (Todos los meses / años)
  st.subheader("📈 Tendencia Histórica de Indicadores")
  if not df_filtrado.empty:
    fig = px.bar(
        df_filtrado,
        x="Mes",
        y="Real",
        color="Estado",
        barmode="group",
        facet_col="Ano" if "Ano" in df_filtrado.columns else None,
        color_discrete_map={
            "Cumplido": "#28a745",
            "En Riesgo": "#ffc107",
            "No Cumplido": "#dc3545",
        },
        title="Desempeño por Mes y Año",
        labels={"Real": "Valor Alcanzado", "Mes": "Mes"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.warning(
        "No hay datos disponibles para los filtros seleccionados."
    )

  # Tabla detallada inferior (Estilo panel de control)
  st.subheader("📋 Detalle de Registros de Calidad")
  st.dataframe(df_filtrado, use_container_width=True)

else:
  st.info(
      "👆 Por favor, sube tu archivo CSV con el histórico de años y meses para"
      " activar el panel."
  )
