# config/settings.py

# Google Sheets
SHEET_NAME = "Finanzas"        # nombre exacto de tu archivo
TAB_REGISTROS = "Ingresos/Gastos"   # pestaña de transacciones
TAB_DEUDAS = "Resumen"
RANGO_DATOS = "A1:F5000"
RANGO_DEUDAS = "A20:B5000"

# Columnas de tu tabla (deben coincidir exactamente con tus encabezados en Sheets)
COLUMNAS = ["Fecha", "Gastos/Ingresos", "Fuente", "Tipo", "Deudor", "Mult"]

# Valores válidos para el campo "tipo"
TIPOS_VALIDOS = [
    "Ahorros",
    "Cartera",
    "Visa",
    "Master",
    "Bancolombia",
    "Nequi",
    "Global (COP)",
    "Global (USD)",
    "Uala"
    # agrega los que uses
]