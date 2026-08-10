import streamlit as st

from DTOs import AsignarRepartidorDTO, EntregarPedidoDTO, ActualizarEstadoPedidoDTO


def mostrar_vista_pedidos(pedido_ctrl, repartidor_ctrl):
    """Vista principal de gestión de pedidos."""
    st.header("📦 Gestión de Pedidos")

    tab_asignar, tab_estado, tab_entregar, tab_listar = st.tabs([
        "Asignar Repartidor", "Actualizar Estado", "Entregar Pedido", "Pedidos Registrados"
    ])

    with tab_asignar:
        _formulario_asignar_repartidor(pedido_ctrl, repartidor_ctrl)

    with tab_estado:
        _formulario_actualizar_estado(pedido_ctrl)

    with tab_entregar:
        _formulario_entregar_pedido(pedido_ctrl)

    with tab_listar:
        _lista_pedidos(pedido_ctrl)


def _formulario_asignar_repartidor(pedido_ctrl, repartidor_ctrl):
    """Formulario para asignar un repartidor a un pedido."""
    st.subheader("Asignar Repartidor")

    resultado_pedidos = pedido_ctrl.obtener_todos_los_pedidos()
    pedidos = resultado_pedidos.datos if resultado_pedidos.datos else []
    pedidos_sin_repartidor = [p for p in pedidos if not p.tiene_repartidor()]

    resultado_repartidores = repartidor_ctrl.obtener_todos_los_repartidores()
    repartidores = resultado_repartidores.datos if resultado_repartidores.datos else []

    if not pedidos_sin_repartidor:
        st.info("No hay pedidos sin repartidor asignado.")
        return

    if not repartidores:
        st.info("No hay repartidores registrados.")
        return

    col_manual, col_auto = st.columns(2)

    with col_manual:
        st.write("**Asignación manual**")
        with st.form("form_asignar_repartidor"):
            opciones_pedidos = {
                f"Pedido #{p.id} — {p.cliente.nombre}": p for p in pedidos_sin_repartidor
            }
            pedido_sel = st.selectbox("Pedido", list(opciones_pedidos.keys()))
            pedido = opciones_pedidos[pedido_sel]

            opciones_rep = {
                f"{r.nombre} (Cédula: {r.cedula})": r for r in repartidores
            }
            rep_sel = st.selectbox("Repartidor", list(opciones_rep.keys()))
            repartidor = opciones_rep[rep_sel]

            enviado = st.form_submit_button("🔗 Asignar", use_container_width=True)

            if enviado:
                dto = AsignarRepartidorDTO(
                    id_pedido=pedido.id,
                    cedula_repartidor=repartidor.cedula,
                )
                resultado = pedido_ctrl.asignar_repartidor(dto)
                if resultado.exitoso:
                    st.success(resultado.mensaje)
                else:
                    st.error(resultado.mensaje)

    with col_auto:
        st.write("**Asignación automática**")
        with st.form("form_asignar_auto"):
            opciones_pedidos_auto = {
                f"Pedido #{p.id} — {p.cliente.nombre}": p for p in pedidos_sin_repartidor
            }
            pedido_sel_auto = st.selectbox("Pedido", list(opciones_pedidos_auto.keys()), key="auto_pedido")
            pedido_auto = opciones_pedidos_auto[pedido_sel_auto]

            enviado_auto = st.form_submit_button("⚡ Asignar automáticamente", use_container_width=True)

            if enviado_auto:
                resultado = pedido_ctrl.asignar_repartidor_automatico(pedido_auto.id)
                if resultado.exitoso:
                    st.success(resultado.mensaje)
                else:
                    st.error(resultado.mensaje)


def _formulario_entregar_pedido(pedido_ctrl):
    """Formulario para marcar un pedido como entregado."""
    st.subheader("Entregar Pedido")

    resultado_pedidos = pedido_ctrl.obtener_todos_los_pedidos()
    pedidos = resultado_pedidos.datos if resultado_pedidos.datos else []
    pedidos_en_camino = [p for p in pedidos if p.estado.value == "EN_CAMINO"]

    if not pedidos_en_camino:
        st.info("No hay pedidos 'EN CAMINO' pendientes de entrega.")
        return

    with st.form("form_entregar_pedido"):
        opciones = {
            f"Pedido #{p.id} — {p.cliente.nombre} ({p.estado.value})": p
            for p in pedidos_en_camino
        }
        pedido_sel = st.selectbox("Seleccionar pedido", list(opciones.keys()))
        pedido = opciones[pedido_sel]

        st.markdown("---")
        st.write("¿Desea calificar al repartidor?")
        calificar = st.checkbox("Sí, deseo evaluar el servicio")
        
        amabilidad = 5
        tiempo = 5
        presentacion = 5
        
        if calificar:
            amabilidad = st.slider("Amabilidad", 1, 10, 5)
            tiempo = st.slider("Tiempo de respuesta", 1, 10, 5)
            presentacion = st.slider("Presentación", 1, 10, 5)

        enviado = st.form_submit_button("📬 Marcar como entregado", use_container_width=True)

        if enviado:
            dto = EntregarPedidoDTO(
                id_pedido=pedido.id,
                calificar=calificar,
                amabilidad=amabilidad,
                tiempo_de_respuesta=tiempo,
                presentacion=presentacion
            )
            resultado = pedido_ctrl.entregar_pedido(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)

def _formulario_actualizar_estado(pedido_ctrl):
    """Formulario para cambiar el estado de un pedido (CU-11)."""
    st.subheader("Actualizar Estado de Pedido")
    
    resultado_pedidos = pedido_ctrl.obtener_todos_los_pedidos()
    pedidos = resultado_pedidos.datos if resultado_pedidos.datos else []
    # Solo mostrar pedidos que no estén entregados ni suspendidos
    pedidos_actualizables = [p for p in pedidos if p.estado.value in ["EN_PREPARACION", "EN_CAMINO"]]
    
    if not pedidos_actualizables:
        st.info("No hay pedidos activos para cambiar de estado.")
        return
        
    with st.form("form_actualizar_estado_pedido"):
        opciones = {
            f"Pedido #{p.id} — {p.cliente.nombre} ({p.estado.value})": p
            for p in pedidos_actualizables
        }
        pedido_sel = st.selectbox("Seleccionar pedido", list(opciones.keys()))
        pedido = opciones[pedido_sel]
        
        nuevo_estado = st.selectbox("Nuevo Estado", ["EN_CAMINO", "SUSPENDIDO"])
        
        enviado = st.form_submit_button("Actualizar Estado")
        
        if enviado:
            dto = ActualizarEstadoPedidoDTO(id_pedido=pedido.id, nuevo_estado=nuevo_estado)
            resultado = pedido_ctrl.actualizar_estado(dto)
            if resultado.exitoso:
                st.success(resultado.mensaje)
            else:
                st.error(resultado.mensaje)


def _lista_pedidos(pedido_ctrl):
    """Muestra la lista de todos los pedidos."""
    st.subheader("Pedidos Registrados")

    resultado = pedido_ctrl.obtener_todos_los_pedidos()
    pedidos = resultado.datos if resultado.datos else []

    if not pedidos:
        st.info("No hay pedidos registrados.")
        return

    for pedido in pedidos:
        estado_emoji = {
            "EN_PREPARACION": "🟡",
            "EN_CAMINO": "🔵",
            "ENTREGADO": "🟢",
            "SUSPENDIDO": "🔴",
        }
        emoji = estado_emoji.get(pedido.estado.value, "⚪")

        with st.expander(f"{emoji} Pedido #{pedido.id} — {pedido.estado.value}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Cliente:** {pedido.cliente.nombre}")
                repartidor_nombre = pedido.repartidor.nombre if pedido.tiene_repartidor() else "Sin asignar"
                st.write(f"**Repartidor:** {repartidor_nombre}")
                st.write(f"**Restaurante:** {pedido.restaurante.nombre}")
            with col2:
                st.write(f"**Distancia:** {pedido.distancia_km} km")
                st.write(f"**Feriado:** {'Sí' if pedido.es_feriado else 'No'}")
                st.write(f"**Hora del pedido:** {pedido.hora_pedido.strftime('%H:%M:%S')}")
            if pedido.factura:
                st.write(f"**Total factura:** ₡{pedido.factura.total:,.2f}")
