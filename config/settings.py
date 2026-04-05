# config/settings.py

# Google Sheets
SHEET_NAME = "Finanzas Mama"        # nombre exacto de tu archivo
TAB_REGISTROS = "Ingresos/Gastos"   # pestaña de transacciones
TAB_DEUDAS = "Resumen"
RANGO_DATOS = "A1:F5000"
RANGO_DEUDAS = "A22:B5000"

# Columnas de tu tabla (deben coincidir exactamente con tus encabezados en Sheets)
COLUMNAS = ["Fecha", "Gastos/Ingresos", "Fuente", "Tipo", "Deudor", "Mult"]

# Valores válidos para el campo "tipo"
TIPOS_VALIDOS = [
    "Ahorros",
    "Efectivo",
    "Coomeva",
    "Falabella",
    "Occidente",
    "Bancolombia",
    "Nequi",
    "Global (COP)",
    "Global (USD)",
    "Uala",
    "Nu",
    "Pibank"
    # agrega los que uses
]