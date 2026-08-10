import streamlit as st

from DTOs import CrearClienteDTO, RealizarPedidoDTO, CambiarEstadoClienteDTO


def mostrar_vista_clientes(cliente_ctrl, restaurante_ctrl):
    """Vista principal de gestión de clientes."""
    st.header("👤 Gestión de Clientes")

    tab_registrar, tab_pedido, tab_estado, tab_listar = st.tabs([
        "Registrar Cliente", "Realizar Pedido", "Cambiar Estado", "Clientes Registrados"
    ])

    with tab_registrar:
        _formulario_registrar_cliente(cliente_ctrl)

    with tab_pedido:
        _formulario_realizar_pedido(cliente_ctrl, restaurante_ctrl)

    with tab_estado:
        _formulario_cambiar_estado(cliente_ctrl)

    with tab_listar:
        _lista_clientes(cliente_ctrl)


def _formulario_registrar_cliente(cliente_ctrl):
    """Formulario para registrar un nuevo cliente."""
    st.subheader("Nuevo Cliente")

    with st.form("form_registrar_cliente", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            cedula = st.number_input("Cédula", min_value=1, step=1, format="%d")
            nombre = st.text_input("Nombre completo")
            correo = st.text_input("Correo electrónico")
            telefono = st.number_input("Teléfono", min_value=10000000, step=1, format="%d")

        with col2:
            contrasenia = st.text_input("Contraseña", type="password")
            num_tarjeta = st.number_input("Número de tarjeta", min_value=100000000000, step=1, format="%d")
            direccion = st.text_input("Dirección")

        enviado = st.form_submit_button("✅ Registrar Cliente", use_container_width=True)

        if enviado:
            dto = CrearClienteDTO(
                cedula=int(cedula),
                contrasenia=contrasenia,
                nombre=nombre,
                correo=correo,
                telefono=int(telefono),
                num_de_tarjeta=int(num_tarjeta),
                direccion=direccion,
            )
            resultado = cliente_ctrl.registrar_cliente(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)


def _formulario_realizar_pedido(cliente_ctrl, restaurante_ctrl):
    """Formulario para que un cliente realice un pedido."""
    st.subheader("Nuevo Pedido")

    # Obtener restaurantes disponibles para el selector
    res_resultado = restaurante_ctrl.obtener_todos_los_restaurantes()
    restaurantes = res_resultado.datos if res_resultado.datos else []

    if not restaurantes:
        st.info("No hay restaurantes registrados. Registre uno primero.")
        return

    with st.form("form_realizar_pedido"):
        cedula_cliente = st.number_input("Cédula del cliente", min_value=1, step=1, format="%d")

        opciones_rest = {f"{r.nombre} (CJ: {r.cedula_juridica})": r for r in restaurantes}
        rest_seleccionado = st.selectbox("Restaurante", list(opciones_rest.keys()))
        restaurante = opciones_rest[rest_seleccionado]

        # Mostrar combos del menú
        menu_resultado = restaurante_ctrl.obtener_menu(restaurante.cedula_juridica)
        combos_disponibles = menu_resultado.datos if menu_resultado.exitoso and menu_resultado.datos else []

        if combos_disponibles:
            opciones_combos = {
                f"Combo #{c.num_de_combo} - {c.nombre} (₡{c.precio:.0f})": c.num_de_combo
                for c in combos_disponibles
            }
            combos_seleccionados = st.multiselect("Combos del menú", list(opciones_combos.keys()))
            numeros_combos = [opciones_combos[c] for c in combos_seleccionados]
        else:
            st.warning("Este restaurante no tiene combos en su menú.")
            numeros_combos = []

        col1, col2 = st.columns(2)
        with col1:
            distancia = st.number_input("Distancia (km)", min_value=0.0, step=0.5, format="%.1f")
        with col2:
            es_feriado = st.checkbox("¿Es día feriado?")

        enviado = st.form_submit_button("🛒 Realizar Pedido", use_container_width=True)

        if enviado:
            if not numeros_combos:
                st.error("Debe seleccionar al menos un combo.")
            else:
                dto = RealizarPedidoDTO(
                    cedula_cliente=int(cedula_cliente),
                    cedula_juridica_restaurante=restaurante.cedula_juridica,
                    numeros_de_combos=numeros_combos,
                    distancia_km=distancia,
                    es_feriado=es_feriado,
                )
                resultado = cliente_ctrl.realizar_pedido(dto)
                if resultado.exitoso:
                    st.success(resultado.mensaje)
                else:
                    st.error(resultado.mensaje)


def _lista_clientes(cliente_ctrl):
    """Muestra la lista de clientes registrados."""
    st.subheader("Clientes Registrados")

    resultado = cliente_ctrl.obtener_todos_los_clientes()
    clientes = resultado.datos if resultado.datos else []

    if not clientes:
        st.info("No hay clientes registrados.")
        return

    for cliente in clientes:
        with st.expander(f"📋 {cliente.nombre} — Cédula: {cliente.cedula}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Correo:** {cliente.correo}")
                st.write(f"**Teléfono:** {cliente.telefono}")
            with col2:
                st.write(f"**Dirección:** {cliente.direccion}")
                st.write(f"**Estado:** {cliente.estado.value}")

def _formulario_cambiar_estado(cliente_ctrl):
    """Formulario para que un admin cambie el estado de un cliente (CU-03)."""
    st.subheader("Cambiar Estado de Cliente")
    with st.form("form_cambiar_estado_cliente"):
        cedula = st.number_input("Cédula del cliente", min_value=1, step=1, format="%d")
        nuevo_estado = st.selectbox("Nuevo Estado", ["ACTIVO", "SUSPENDIDO"])
        enviado = st.form_submit_button("Actualizar Estado")
        
        if enviado:
            dto = CambiarEstadoClienteDTO(cedula=int(cedula), nuevo_estado=nuevo_estado)
            resultado = cliente_ctrl.cambiar_estado(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)
