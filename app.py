# app.py

import streamlit as st

# Configuración general de la página


def check_login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Acceso restringido")

        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            usuarios = st.secrets["usuarios"]
            if usuario in usuarios and usuarios[usuario] == password:
                st.session_state.authenticated = True
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
        st.stop()
        
check_login()

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