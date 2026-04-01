import streamlit as st
from datetime import date
from data.sheets_connector import add_record, actualizar_tabla_deudas
from config.settings import TIPOS_VALIDOS

def mostrar():
    st.title("➕ Nueva deuda")
    st.write("Ingresa los datos de la deuda.")

    # ─────────────────────────────────────────
    # FORMULARIO
    # ─────────────────────────────────────────

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha", value=date.today())
        monto = st.number_input(
            "Monto",
            value=0,
            step=1000,
            help="Solamente valores positivos"
        )

    with col2:
        descripcion = st.text_input("Descripción")
        deudor = st.text_input(
            "Deudor",
            placeholder="Nombre de la(s) persona(s)",
        )

    # ─────────────────────────────────────────
    # VALIDACIONES Y ENVÍO
    # ─────────────────────────────────────────

    # Muestra un resumen antes de confirmar
    if monto > 0:
        st.divider()
        st.subheader("Resumen")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Monto", f"${monto:,.0f}")
        col_b.metric("Deudor", deudor)
        col_c.metric("Fecha", str(fecha))


    st.divider()

    # Botón de envío
    if st.button("Guardar registro", type="primary", width="stretch"):
        
        if deudor:
            actualizar_tabla_deudas(deudor)
        else:
            st.error("❌ El deudor no puede estar vacío.")
        
        # Validaciones
        if monto == 0:
            st.error("❌ El monto no puede ser cero.")
            
        if monto < 0:
            st.error("❌ El monto no puede ser negativo.")

        elif not descripcion:
            st.error("❌ La descripción no puede estar vacía.")

        else:
            # Formatea la fecha como string para Sheets
            fecha_str = fecha.strftime("%d/%m/%Y")

            exito = add_record(
                fecha=fecha_str,
                monto=-1*monto,
                tipo="",
                descripcion=descripcion,
                deudor=deudor,
                factor=1
            )

            if exito:
                st.success("✅ Registro guardado correctamente en Google Sheets.")
                st.balloons()
            else:
                st.error("❌ Hubo un error al guardar. Revisa la consola.")