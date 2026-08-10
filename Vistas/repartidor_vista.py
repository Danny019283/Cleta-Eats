import streamlit as st

from DTOs import CrearRepartidorDTO, QuejaRepartidorDTO, CalcularPagoDTO


def mostrar_vista_repartidores(repartidor_ctrl):
    """Vista principal de gestión de repartidores."""
    st.header("🚴 Gestión de Repartidores")

    tab_registrar, tab_queja, tab_pago, tab_listar = st.tabs([
        "Registrar Repartidor", "Registrar Queja", "Calcular Pago", "Repartidores Registrados"
    ])

    with tab_registrar:
        _formulario_registrar_repartidor(repartidor_ctrl)

    with tab_queja:
        _formulario_registrar_queja(repartidor_ctrl)

    with tab_pago:
        _formulario_calcular_pago(repartidor_ctrl)

    with tab_listar:
        _lista_repartidores(repartidor_ctrl)


def _formulario_registrar_repartidor(repartidor_ctrl):
    """Formulario para registrar un nuevo repartidor."""
    st.subheader("Nuevo Repartidor")

    with st.form("form_registrar_repartidor", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            cedula = st.number_input("Cédula", min_value=1, step=1, format="%d")
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo electrónico")
            telefono = st.number_input("Teléfono", min_value=10000000, step=1, format="%d")

        with col2:
            contrasenia = st.text_input("Contraseña", type="password")
            num_tarjeta = st.number_input("Número de tarjeta", min_value=100000000000, step=1, format="%d")

        enviado = st.form_submit_button("✅ Registrar Repartidor", use_container_width=True)

        if enviado:
            dto = CrearRepartidorDTO(
                cedula=int(cedula),
                contrasenia=contrasenia,
                nombre=nombre,
                correo=correo,
                telefono=int(telefono),
                num_de_tarjeta=int(num_tarjeta)
            )
            resultado = repartidor_ctrl.registrar_repartidor(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)


def _formulario_registrar_queja(repartidor_ctrl):
    """Formulario para registrar una queja contra un repartidor."""
    st.subheader("Registrar Queja")

    resultado_rep = repartidor_ctrl.obtener_todos_los_repartidores()
    repartidores = resultado_rep.datos if resultado_rep.datos else []

    if not repartidores:
        st.info("No hay repartidores registrados.")
        return

    with st.form("form_registrar_queja", clear_on_submit=True):
        opciones = {f"{r.nombre} (Cédula: {r.cedula})": r for r in repartidores}
        rep_sel = st.selectbox("Repartidor", list(opciones.keys()))
        repartidor = opciones[rep_sel]

        motivo = st.text_area("Motivo de la queja")

        enviado = st.form_submit_button("⚠️ Registrar Queja", use_container_width=True)

        if enviado:
            if not motivo.strip():
                st.error("Debe indicar el motivo de la queja.")
            else:
                dto = QuejaRepartidorDTO(
                    cedula_repartidor=repartidor.cedula,
                    motivo=motivo,
                )
                resultado = repartidor_ctrl.registrar_queja(dto)
                if resultado.exitoso:
                    st.success(resultado.mensaje)
                else:
                    st.error(resultado.mensaje)


def _formulario_calcular_pago(repartidor_ctrl):
    """Formulario para calcular el pago diario de un repartidor."""
    st.subheader("Calcular Pago Diario")

    resultado_rep = repartidor_ctrl.obtener_todos_los_repartidores()
    repartidores = resultado_rep.datos if resultado_rep.datos else []

    if not repartidores:
        st.info("No hay repartidores registrados.")
        return

    with st.form("form_calcular_pago"):
        opciones = {f"{r.nombre} (Cédula: {r.cedula})": r for r in repartidores}
        rep_sel = st.selectbox("Repartidor", list(opciones.keys()))
        repartidor = opciones[rep_sel]

        es_feriado = st.checkbox("¿Es día feriado?")

        enviado = st.form_submit_button("💰 Calcular Pago", use_container_width=True)

        if enviado:
            dto = CalcularPagoDTO(
                cedula_repartidor=repartidor.cedula,
                es_feriado=es_feriado,
            )
            resultado = repartidor_ctrl.calcular_pago_diario(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
                st.metric("Pago del día", f"₡{resultado.datos:,.2f}")
            else:
                st.error(resultado.mensaje)


def _lista_repartidores(repartidor_ctrl):
    """Muestra la lista de repartidores registrados."""
    st.subheader("Repartidores Registrados")

    resultado = repartidor_ctrl.obtener_todos_los_repartidores()
    repartidores = resultado.datos if resultado.datos else []

    if not repartidores:
        st.info("No hay repartidores registrados.")
        return

    for rep in repartidores:
        disponible = "✅ Disponible" if rep.disponibilidad else "❌ No disponible"
        with st.expander(f"🚴 {rep.nombre} — Cédula: {rep.cedula} — {disponible}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Correo:** {rep.correo}")
                st.write(f"**Teléfono:** {rep.telefono}")
                st.write(f"**Estado:** {rep.estado.value}")
            with col2:
                st.write(f"**Amonestaciones:** {rep.num_de_amonestaciones}")
                st.write(f"**Calificación:** {rep.calificacion.calificacion}")
                st.write(f"**Km recorridos hoy:** {rep.km_recorridos_hoy}")

            # Mostrar quejas si existen
            resultado_quejas = repartidor_ctrl.obtener_quejas(rep.cedula)
            if resultado_quejas.exitoso and resultado_quejas.datos:
                st.write("**Quejas:**")
                for queja in resultado_quejas.datos:
                    st.write(f"  • {queja}")
