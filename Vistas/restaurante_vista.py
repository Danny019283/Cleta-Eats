import streamlit as st

from DTOs import CrearRestauranteDTO, CrearComboDTO


def mostrar_vista_restaurantes(restaurante_ctrl):
    """Vista principal de gestión de restaurantes."""
    st.header("🍽️ Gestión de Restaurantes")

    tab_registrar, tab_combo, tab_menu, tab_listar = st.tabs([
        "Registrar Restaurante", "Agregar Combo", "Ver Menú", "Restaurantes Registrados"
    ])

    with tab_registrar:
        _formulario_registrar_restaurante(restaurante_ctrl)

    with tab_combo:
        _formulario_agregar_combo(restaurante_ctrl)

    with tab_menu:
        _ver_menu(restaurante_ctrl)

    with tab_listar:
        _lista_restaurantes(restaurante_ctrl)


def _formulario_registrar_restaurante(restaurante_ctrl):
    """Formulario para registrar un nuevo restaurante."""
    st.subheader("Nuevo Restaurante")

    with st.form("form_registrar_restaurante", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del restaurante")
            cedula_juridica = st.number_input("Cédula jurídica", min_value=1, step=1, format="%d")

        with col2:
            direccion = st.text_input("Dirección")
            tipo_comida = st.text_input("Tipo de comida")

        enviado = st.form_submit_button("✅ Registrar Restaurante", use_container_width=True)

        if enviado:
            dto = CrearRestauranteDTO(
                nombre=nombre,
                cedula_juridica=int(cedula_juridica),
                direccion=direccion,
                tipo_de_comida=tipo_comida,
            )
            resultado = restaurante_ctrl.registrar_restaurante(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)


def _formulario_agregar_combo(restaurante_ctrl):
    """Formulario para agregar un combo al menú de un restaurante."""
    st.subheader("Agregar Combo al Menú")

    resultado_rest = restaurante_ctrl.obtener_todos_los_restaurantes()
    restaurantes = resultado_rest.datos if resultado_rest.datos else []

    if not restaurantes:
        st.info("No hay restaurantes registrados.")
        return

    with st.form("form_agregar_combo", clear_on_submit=True):
        opciones_rest = {f"{r.nombre} (CJ: {r.cedula_juridica})": r for r in restaurantes}
        rest_seleccionado = st.selectbox("Restaurante", list(opciones_rest.keys()))
        restaurante = opciones_rest[rest_seleccionado]

        col1, col2 = st.columns(2)
        with col1:
            num_combo = st.number_input("Número de combo (1-9)", min_value=1, max_value=9, step=1)
        with col2:
            nombre_combo = st.text_input("Nombre del combo")

        st.caption("💡 El precio se asigna automáticamente según el número: ₡3000 + (N° × ₡1000)")

        enviado = st.form_submit_button("➕ Agregar Combo", use_container_width=True)

        if enviado:
            dto = CrearComboDTO(num_de_combo=int(num_combo), nombre=nombre_combo)
            resultado = restaurante_ctrl.agregar_combo(restaurante.cedula_juridica, dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)


def _ver_menu(restaurante_ctrl):
    """Muestra el menú de un restaurante seleccionado."""
    st.subheader("Menú del Restaurante")

    resultado_rest = restaurante_ctrl.obtener_todos_los_restaurantes()
    restaurantes = resultado_rest.datos if resultado_rest.datos else []

    if not restaurantes:
        st.info("No hay restaurantes registrados.")
        return

    opciones_rest = {f"{r.nombre} (CJ: {r.cedula_juridica})": r for r in restaurantes}
    rest_seleccionado = st.selectbox(
        "Seleccionar restaurante", list(opciones_rest.keys()), key="menu_select"
    )
    restaurante = opciones_rest[rest_seleccionado]

    resultado = restaurante_ctrl.obtener_menu(restaurante.cedula_juridica)

    if not resultado.exitoso:
        st.error(resultado.mensaje)
        return

    combos = resultado.datos
    if not combos:
        st.info("Este restaurante aún no tiene combos en su menú.")
        return

    for combo in combos:
        st.write(f"🍔 **Combo #{combo.num_de_combo}** — {combo.nombre} — ₡{combo.precio:,.0f}")


def _lista_restaurantes(restaurante_ctrl):
    """Muestra la lista de restaurantes registrados."""
    st.subheader("Restaurantes Registrados")

    resultado = restaurante_ctrl.obtener_todos_los_restaurantes()
    restaurantes = resultado.datos if resultado.datos else []

    if not restaurantes:
        st.info("No hay restaurantes registrados.")
        return

    for rest in restaurantes:
        with st.expander(f"🏪 {rest.nombre} — CJ: {rest.cedula_juridica}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dirección:** {rest.direccion}")
                st.write(f"**Tipo de comida:** {rest.tipo_de_comida}")
            with col2:
                st.write(f"**Pedidos recibidos:** {rest.num_de_pedidos_recibidos}")
                st.write(f"**Monto total vendido:** ₡{rest.monto_total_vendido:,.2f}")
            if rest.menu:
                st.write("**Menú:**")
                for combo in rest.menu:
                    st.write(f"  • Combo #{combo.num_de_combo}: {combo.nombre} — ₡{combo.precio:,.0f}")
