import streamlit as st
from datetime import date
from data.sheets_connector import add_record, actualizar_tabla_deudas
from config.settings import TIPOS_VALIDOS

def mostrar():
    st.title("➕ Nuevo Registro")
    st.write("Ingresa los datos de tu transacción.")

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
            help="Positivo para ingresos, negativo para gastos"
        )
        tipo = st.selectbox("Tipo", options=TIPOS_VALIDOS)

    with col2:
        descripcion = st.text_input("Descripción")
        deudor = st.text_input(
            "Deudor",
            placeholder="Opcional — nombre de la(s) persona(s)",
        )
        factor = st.slider(
            "Factor de deuda",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            help="Porcentaje del monto que corresponde a la deuda (0 = sin deuda)"
        )

    # ─────────────────────────────────────────
    # VALIDACIONES Y ENVÍO
    # ─────────────────────────────────────────

    # Muestra un resumen antes de confirmar
    if monto != 0:
        st.divider()
        st.subheader("Resumen")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Monto", f"${monto:,.0f}")
        col_b.metric("Tipo", tipo)
        col_c.metric("Fecha", str(fecha))

        if deudor and factor > 0:
            valor_deuda = abs(monto) * factor
            st.info(f"💳 Este registro genera una deuda de **${valor_deuda:,.0f}** con {deudor}")

    st.divider()

    # Botón de envío
    if st.button("Guardar registro", type="primary", width="stretch"):
        
        actualizar_tabla_deudas()
        
        # Validaciones
        if monto == 0:
            st.error("❌ El monto no puede ser cero.")

        elif not descripcion:
            st.error("❌ La descripción no puede estar vacía.")

        elif deudor and factor == 0:
            st.warning("⚠️ Ingresaste un deudor pero el factor es 0. ¿Es correcto?")

        else:
            # Formatea la fecha como string para Sheets
            fecha_str = fecha.strftime("%d/%m/%Y")

            exito = add_record(
                fecha=fecha_str,
                monto=monto,
                tipo=tipo,
                descripcion=descripcion,
                deudor=deudor,
                factor=factor if factor != 0 else ""
            )

            if exito:
                st.success("✅ Registro guardado correctamente en Google Sheets.")
                st.balloons()
            else:
                st.error("❌ Hubo un error al guardar. Revisa la consola.")