import streamlit as st
from datetime import date
from data.sheets_connector import get_celda, get_tabla, get_registros
from config.settings import TIPOS_VALIDOS

def num_to_col(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def col_to_num(col):
    result = 0
    for c in col:
        result = result * 26 + (ord(c.upper()) - 64)
    return result

def mostrar():
    st.title("🔍 Consultas")
    
    
    granularidad = st.radio(
        "Consultar por",
        options=["Año", "Mes", "Fecha"],
        horizontal=True
    )

    # FILTRO 2 — Período (depende del filtro 1)
    col1, col2, col3 = st.columns(3)

    with col1:
        anio_i = int(get_celda("Módulo_fechas","B2"))
        anio_f = int(get_celda("Módulo_fechas","B5"))
        anios = list(range(anio_i,anio_f+1))
        anio = st.selectbox("Año", options=anios)  # ej: [2023, 2024, 2025]
        meses = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
        meses_completo = meses.copy()
        if anio == anios[0]:
            meses = meses[2:]
        elif anio == anios[-1]:
            mes_actual = int(get_celda("Módulo_fechas","B4"))-1
            meses = meses[0:mes_actual]

    with col2:
        if granularidad == "Mes" or granularidad == "Fecha":
            mes = st.selectbox("Mes", options=meses)
        # Si es "Año", esta columna queda vacía intencionalmente

    with col3:
        if granularidad == "Fecha":
            fecha = st.selectbox("Fecha", options=list(range(1,32)))
        
    # FILTRO 3 — Tipo
    tipo = st.selectbox(
        "Tipo",
        options=["General"] + TIPOS_VALIDOS
    )

    # ─────────────────────────────────────────
    # CONSULTA
    # ─────────────────────────────────────────

    if st.button("Consultar", type="primary", width="stretch"):

        # Construye los parámetros según los filtros
        if granularidad == "Año":
            periodo = str(anio)
        elif granularidad == "Mes":
            periodo = f"{mes}/{anio}"
        else:
            periodo = f"{fecha}/{mes}/{anio}"

        # Trae la tabla correspondiente desde Sheets
        # Aquí defines el rango según tu estructura real
        if granularidad != "Fecha":
            if tipo == "General":
                pestaña = "Ingresos/Gastos"
                col_in = 9
            else:
                pestaña = tipo
                col_in = 4
            
            col = col_in + 5*(anio-2025)
            col_i = num_to_col(col)
            col += 3
            col_f = num_to_col(col)
            
            df = get_tabla(pestaña, f"{col_i}2:{col_f}15")
            if granularidad == "Mes":
                df = df[df["Mes"]==mes]
            else:
                df = df[df["Mes"].isin(meses+["Total"])]
                
        else:
            df = get_registros()
            mes_in = meses_completo.index(mes)+1
            if len(str(fecha)) == 2 and len(str(mes_in)) == 2:
                dat = f"{fecha}/{mes_in}/{anio}"
            elif len(str(fecha)) == 2:
                dat = f"{fecha}/0{mes_in}/{anio}"
            elif len(str(mes_in)) == 2:
                dat = f"0{fecha}/{mes_in}/{anio}"
            else:
                dat = f"0{fecha}/0{mes_in}/{anio}"

            df = df[df["Fecha"]==dat]
            if tipo != "General":
                df = df[df["Fuente"]==tipo]

        # ─────────────────────────────────────────
        # RESULTADOS
        # ─────────────────────────────────────────

        st.divider()
        st.subheader(f"Resultados — {periodo}")

        st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )
    
    
