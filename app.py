# app.py

import streamlit as st

# Configuración general de la página
st.set_page_config(
    page_title="Mis Finanzas",
    page_icon="💰",
    layout="wide"
)

# Navegación en el sidebar
st.sidebar.title("💰 Mis Finanzas")
vista = st.sidebar.radio(
    "Navegación",
    ["Nuevo Registro", "Nueva Deuda", "Dashboard", "Consultas"]
)

# Enrutamiento
if vista == "Dashboard":
    from views.dashboard import mostrar
    mostrar()

elif vista == "Nueva Deuda":
    from views.nueva_deuda import mostrar
    mostrar()

elif vista == "Nuevo Registro":
    from views.nuevo_registro import mostrar
    mostrar()

elif vista == "Consultas":
    from views.consultas import mostrar
    mostrar()