import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from config.settings import SHEET_NAME, TAB_REGISTROS, RANGO_DATOS, COLUMNAS

# ─────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────

def get_sheet(nombre_pestana: str):
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],  # lee desde Secrets
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(nombre_pestana)


# ─────────────────────────────────────────
# LECTURA
# ─────────────────────────────────────────

def get_registros() -> pd.DataFrame:
    """
    Trae la tabla principal de transacciones como DataFrame.
    """
    sheet = get_sheet(TAB_REGISTROS)
    datos_crudos = sheet.get(RANGO_DATOS)

    encabezados = datos_crudos[0]
    filas = datos_crudos[1:]
    registros = [dict(zip(encabezados, fila)) for fila in filas if any(fila)]

    return pd.DataFrame(registros)


def get_celda(nombre_pestana: str, celda: str) -> str:
    """
    Lee el valor de una celda individual.
    Ejemplo: get_celda("Resumen", "B4") → "$1.200.000"
    """
    sheet = get_sheet(nombre_pestana)
    return sheet.acell(celda).value


def get_tabla(nombre_pestana: str, rango: str) -> pd.DataFrame:
    """
    Lee una tabla con encabezados desde cualquier pestaña y rango.
    Ejemplo: get_tabla("Deudas", "A1:C20")
    """
    sheet = get_sheet(nombre_pestana)
    datos = sheet.get(rango)

    if not datos or len(datos) < 2:
        return pd.DataFrame()

    encabezados = datos[0]
    filas = datos[1:]
            
    registros = [dict(zip(encabezados, fila)) for fila in filas if any(fila)]

    return pd.DataFrame(registros)


# ─────────────────────────────────────────
# ESCRITURA
# ─────────────────────────────────────────

def add_record(fecha: str, monto: float, tipo: str,
               descripcion: str, deudor: str = "", factor: float = "") -> bool:
    """
    Agrega una nueva fila al final de la tabla de transacciones.
    Retorna True si fue exitoso, False si hubo error.
    """
    try:
        sheet = get_sheet(TAB_REGISTROS)
        nueva_fila = [fecha, monto, tipo, descripcion, deudor, factor]
        sheet.append_row(nueva_fila, value_input_option="USER_ENTERED")
        return True
    except Exception as e:
        print(f"Error al agregar registro: {e}")
        return False


# ─────────────────────────────────────────
# PRUEBA
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Prueba lectura de registros
    df = get_registros()
    print(f"Registros: {len(df)} filas")
    print(df.head(3))
    
    # Prueba lectura de celda individual — ajusta pestaña y celda
    valor = get_celda("Resumen", "B4")
    print(f"Celda B4: {valor}")

    # Prueba lectura de tabla — ajusta pestaña y rango
    tabla = get_tabla("Cartera", "D2:G7")
    print(tabla)