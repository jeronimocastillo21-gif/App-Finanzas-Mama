# app.py

import streamlit as st

from streamlit_google_auth import Authenticate

# Configuración general de la página


authenticator = Authenticate(
    secret_credentials_path="credenciales.json",
    cookie_name="finanzas_app",
    cookie_key=st.secrets["COOKIE_KEY"],
    redirect_uri="https://app-finanzas-mama.streamlit.app/"
)

authenticator.check_authentification()

if not st.session_state.connected:
    st.stop()

# Restringe por correo específico
CORREOS_PERMITIDOS = ["jeronimo.castillo21@gmail.com"]
if st.session_state.user_info["email"] not in CORREOS_PERMITIDOS:
    st.error("No tienes acceso a esta aplicación")
    st.stop()

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