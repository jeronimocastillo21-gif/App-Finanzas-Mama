import streamlit as st
import plotly.express as px
from data.sheets_connector import get_celda, get_tabla
from config.settings import RANGO_DEUDAS

def mostrar():
    st.title("📊 Dashboard")

    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

    # ─────────────────────────────────────────
    # SECCIÓN 1 — BALANCE NETO TOTAL
    # ─────────────────────────────────────────

    st.subheader("Balance general")

    balance_neto = get_celda("Resumen", "B11")  # ej: get_celda("Resumen", "B2")

    st.metric(
        label="Balance neto total",
        value=balance_neto
    )

    st.divider()

    # ─────────────────────────────────────────
    # SECCIÓN 2 — BALANCE POR TIPO
    # ─────────────────────────────────────────

    st.subheader("Balance por tipo")

    df_tipos = get_tabla("Resumen", "A1:B10")  # ej: get_tabla("Resumen", "A5:B10")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
    
        st.dataframe(
            df_tipos,
            width="stretch",
            hide_index=True
        )
    
    with col2:
    
        df_tipos["Valor"] = (df_tipos["Valor"].str.replace("$","").str.replace(",","").astype(float))

        # Crear el pie sin textos
        fig = px.pie(
            df_tipos,
            names="Fondos",
            values="Valor",
            title="Distribución de Fondos",
            hole=0.3  # opcional: donut más moderno
        )

        fig.update_traces(
            textinfo="none",  # sin texto dentro
            hovertemplate="<b>%{label}</b><br>Valor: $%{value:,.0f}<br>%{percent}"
        )

        fig.update_layout(
            legend_title="Fondos"
        )

        st.plotly_chart(fig, width = "stretch")

    st.divider()
    
    # ─────────────────────────────────────────
    # SECCIÓN 3 — GASTOS MES ACTUAL TARJETAS
    # ─────────────────────────────────────────

    st.subheader("Gasto de las tarjetas en el mes actual")

    df_tarjetas = get_tabla("Resumen", "A13:C16")  # ej: get_tabla("Resumen", "A5:B10")
    
    st.dataframe(
        df_tarjetas.drop("Total", axis=1),
        width="stretch",
        hide_index=True
    )

    st.divider()
    
    # ─────────────────────────────────────────
    # SECCIÓN 4 — MONEDAS EXTRANJERAS
    # ─────────────────────────────────────────

    st.subheader("Monedas extranjeras")

    df_extranjeras = get_tabla("Resumen", "A18:B20")  # ej: get_tabla("Deudas", "A1:B10")

    # Ajusta los nombres de columnas a los de tu Sheet
    st.dataframe(
        df_extranjeras,
        width="stretch",
        hide_index=True
    )

    # ─────────────────────────────────────────
    # SECCIÓN 5 — DEUDAS PENDIENTES
    # ─────────────────────────────────────────

    st.subheader("Deudas pendientes")

    df_deudas = get_tabla("Resumen", RANGO_DEUDAS)  # ej: get_tabla("Deudas", "A1:B10")

    # Ajusta los nombres de columnas a los de tu Sheet
    st.dataframe(
        df_deudas,
        width="stretch",
        hide_index=True
    )
