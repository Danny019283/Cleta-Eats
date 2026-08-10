import streamlit as st


def mostrar_vista_reportes(cliente_ctrl, pedido_ctrl, repartidor_ctrl):
    """Vista de reportes del sistema."""
    st.header("📊 Reportes")

    col1, col2 = st.columns(2)

    with col1:
        _reporte_cliente_mas_pedidos(cliente_ctrl)
        st.divider()
        _reporte_rest_mas_pedidos(pedido_ctrl)
        st.divider()
        _reporte_rest_menos_pedidos(pedido_ctrl)

    with col2:
        _reporte_monto_total(pedido_ctrl)
        st.divider()
        _reporte_hora_pico(pedido_ctrl)
        st.divider()
        _reporte_pedidos_por_cliente(cliente_ctrl)

    st.divider()
    _reporte_listados_especificos(cliente_ctrl, repartidor_ctrl)


def _reporte_cliente_mas_pedidos(cliente_ctrl):
    """Muestra el cliente con más pedidos."""
    st.subheader("🏆 Cliente con más pedidos")

    if st.button("Consultar", key="btn_cliente_mas"):
        resultado = cliente_ctrl.obtener_cliente_con_mas_pedidos()
        if resultado.exitoso:
            cliente = resultado.datos
            st.success(f"**{cliente.nombre}** (Cédula: {cliente.cedula})")
        else:
            st.warning(resultado.mensaje)


def _reporte_rest_mas_pedidos(pedido_ctrl):
    """Muestra el restaurante con más pedidos."""
    st.subheader("🥇 Restaurante con más pedidos")

    if st.button("Consultar", key="btn_rest_mas"):
        resultado = pedido_ctrl.obtener_restaurante_con_mas_pedidos()
        if resultado.exitoso:
            rest = resultado.datos
            st.success(f"**{rest.nombre}** — Pedidos: {rest.num_de_pedidos_recibidos}")
        else:
            st.warning(resultado.mensaje)


def _reporte_rest_menos_pedidos(pedido_ctrl):
    """Muestra el restaurante con menos pedidos."""
    st.subheader("🥉 Restaurante con menos pedidos")

    if st.button("Consultar", key="btn_rest_menos"):
        resultado = pedido_ctrl.obtener_restaurante_con_menos_pedidos()
        if resultado.exitoso:
            rest = resultado.datos
            st.success(f"**{rest.nombre}** — Pedidos: {rest.num_de_pedidos_recibidos}")
        else:
            st.warning(resultado.mensaje)


def _reporte_monto_total(pedido_ctrl):
    """Muestra el monto total vendido en el sistema."""
    st.subheader("💵 Monto total vendido")

    if st.button("Consultar", key="btn_monto_total"):
        resultado = pedido_ctrl.obtener_monto_total_vendido()
        if resultado.exitoso:
            st.metric("Total del sistema", f"₡{resultado.datos:,.2f}")
        else:
            st.warning(resultado.mensaje)


def _reporte_hora_pico(pedido_ctrl):
    """Muestra la hora pico de pedidos."""
    st.subheader("⏰ Hora pico")

    if st.button("Consultar", key="btn_hora_pico"):
        resultado = pedido_ctrl.obtener_hora_pico()
        if resultado.exitoso:
            st.success(f"**{resultado.datos.strftime('%H:%M')}**")
        else:
            st.warning(resultado.mensaje)


def _reporte_pedidos_por_cliente(cliente_ctrl):
    """Muestra los pedidos de un cliente específico."""
    st.subheader("📋 Pedidos por cliente")

    cedula = st.number_input("Cédula del cliente", min_value=1, step=1, format="%d", key="rep_cedula")

    if st.button("Consultar", key="btn_pedidos_cliente"):
        resultado = cliente_ctrl.obtener_pedidos_por_cliente(int(cedula))
        if resultado.exitoso:
            pedidos = resultado.datos
            if not pedidos:
                st.info("No se encontraron pedidos para este cliente.")
            else:
                st.success(f"Se encontraron {len(pedidos)} pedido(s).")
                for pedido in pedidos:
                    st.write(
                        f"• Pedido #{pedido.id} — {pedido.estado.value} — "
                        f"₡{pedido.factura.total:,.2f}"
                    )
        else:
            st.warning(resultado.mensaje)

def _reporte_listados_especificos(cliente_ctrl, repartidor_ctrl):
    """Muestra listados específicos según requerimientos e, f, g."""
    st.subheader("📝 Listados Específicos")
    
    tab_activos, tab_suspendidos, tab_repartidores = st.tabs([
        "Clientes Activos", "Clientes Suspendidos", "Repartidores (0 Amonestaciones)"
    ])
    
    with tab_activos:
        res = cliente_ctrl.obtener_todos_los_clientes()
        if res.exitoso and res.datos:
            activos = [c for c in res.datos if c.estado.value == "ACTIVO"]
            for c in activos:
                st.write(f"• ID Cédula: {c.cedula} — Nombre: {c.nombre}")
        else:
            st.info("No hay clientes activos.")
            
    with tab_suspendidos:
        res = cliente_ctrl.obtener_todos_los_clientes()
        if res.exitoso and res.datos:
            suspendidos = [c for c in res.datos if c.estado.value == "DESACTIVADO"]
            for c in suspendidos:
                st.write(f"• ID Cédula: {c.cedula} — Nombre: {c.nombre}")
        else:
            st.info("No hay clientes suspendidos.")
            
    with tab_repartidores:
        res = repartidor_ctrl.obtener_todos_los_repartidores()
        if res.exitoso and res.datos:
            limpios = [r for r in res.datos if r.num_de_amonestaciones == 0]
            for r in limpios:
                st.write(f"• ID Cédula: {r.cedula} — Nombre: {r.nombre}")
        else:
            st.info("No hay repartidores con 0 amonestaciones.")
