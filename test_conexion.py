import gspread
from google.oauth2.service_account import Credentials

# Los scopes le dicen a Google a qué APIs vas a acceder
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Carga las credenciales desde el archivo JSON
creds = Credentials.from_service_account_file("credenciales.json", scopes=SCOPES)

# Autoriza el cliente de gspread
client = gspread.authorize(creds)

# Abre tu hoja por nombre (debe coincidir exactamente con el nombre en Google Sheets)
sheet = client.open("Finanzas").worksheet("Ingresos/Gastos")

# Detecta la última fila con datos automáticamente
todas_las_filas = sheet.get_all_values()
ultima_fila = len([f for f in todas_las_filas if any(f)])

# Lee solo el rango de tu tabla
datos_crudos = sheet.get(f"A1:G{ultima_fila}")

encabezados = datos_crudos[0]
filas = datos_crudos[1:]
registros = [dict(zip(encabezados, fila)) for fila in filas if any(fila)]

print(f"✅ Registros encontrados: {len(registros)}")
print(registros[:3])