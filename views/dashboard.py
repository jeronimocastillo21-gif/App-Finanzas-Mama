import streamlit as st
from data.sheets_connector import get_celda, get_tabla

def mostrar():
    st.title("📊 Dashboard")

    if st.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()

    # ─────────────────────────────────────────
    # SECCIÓN 1 — BALANCE NETO TOTAL
    # ─────────────────────────────────────────

    st.subheader("Balance general")

    balance_neto = get_celda("Resumen", "B7")  # ej: get_celda("Resumen", "B2")

    st.metric(
        label="Balance neto total",
        value=balance_neto
    )

    st.divider()

    # ─────────────────────────────────────────
    # SECCIÓN 2 — BALANCE POR TIPO
    # ─────────────────────────────────────────

    st.subheader("Balance por tipo")

    df_tipos = get_tabla("Resumen", "A1:B6")  # ej: get_tabla("Resumen", "A5:B10")
    print(df_tipos)
    
    st.dataframe(
        df_tipos,
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    
    # ─────────────────────────────────────────
    # SECCIÓN 3 — MONEDAS EXTRANJERAS
    # ─────────────────────────────────────────

    st.subheader("Monedas extranjeras")

    df_extranjeras = get_tabla("Resumen", "A13:B16")  # ej: get_tabla("Deudas", "A1:B10")

    # Ajusta los nombres de columnas a los de tu Sheet
    st.dataframe(
        df_extranjeras,
        use_container_width=True,
        hide_index=True
    )

    # ─────────────────────────────────────────
    # SECCIÓN 4 — DEUDAS PENDIENTES
    # ─────────────────────────────────────────

    st.subheader("Deudas pendientes")

    df_deudas = get_tabla("Resumen", "A18:B20")  # ej: get_tabla("Deudas", "A1:B10")

    # Ajusta los nombres de columnas a los de tu Sheet
    st.dataframe(
        df_deudas,
        use_container_width=True,
        hide_index=True
    )