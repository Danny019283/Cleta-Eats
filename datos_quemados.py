"""
Datos quemados (seed data) para el sistema CletaEats.
Carga datos de prueba predefinidos en los repositorios.
"""
from __future__ import annotations

from Cliente import Cliente
from Repartidor import Repartidor
from Restaurante import Restaurante
from Combo import Combo
from Factura import Factura
from Pedido import Pedido
from ClasificaionDelRepartidor import CalificacionDelRepartidor
from Enums import EstadoDeCuenta, EstadoDelPedido


def cargar_datos_quemados(cliente_repo, repartidor_repo, restaurante_repo, pedido_repo):
    """Carga datos de prueba quemados en los repositorios."""
    restaurantes = _crear_restaurantes()
    for r in restaurantes:
        restaurante_repo.crear(r)

    clientes = _crear_clientes()
    for c in clientes:
        cliente_repo.crear(c)

    repartidores = _crear_repartidores()
    for r in repartidores:
        repartidor_repo.crear(r)

    _crear_pedidos(clientes, restaurantes, repartidores, pedido_repo)
    _registrar_quejas(repartidores)


# ── Restaurantes (7) con 9 combos cada uno ───────────────────────────────────


def _crear_restaurantes():
    datos = [
        ("Pollo Feliz", 3101000001, "Heredia Centro", "Comida rápida", list(range(1, 10))),
        ("Soda La Abuela", 3101000002, "San José, Barrio Amón", "Comida casera", list(range(1, 10))),
        ("Pizza Planet", 3101000003, "Cartago Centro", "Comida italiana", list(range(1, 10))),
        ("Sushi Express", 3101000004, "Escazú, San Rafael", "Comida japonesa", list(range(1, 10))),
        ("Taco Loco", 3101000005, "Alajuela Centro", "Comida mexicana", list(range(1, 10))),
        ("Burger Kingdom", 3101000006, "Liberia, Guanacaste", "Comida rápida", list(range(1, 10))),
        ("Café Don Pedro", 3101000007, "San Pedro, Montes de Oca", "Cafetería", list(range(1, 10))),
    ]

    nombres_combos = {
        1: "Combo Individual",
        2: "Combo Dúo",
        3: "Combo Familiar",
        4: "Combo Ejecutivo",
        5: "Combo Premium",
        6: "Combo Deluxe",
        7: "Combo Supremo",
        8: "Combo Mega",
        9: "Combo Festival",
    }

    restaurantes = []
    for nombre, cedula, direccion, tipo, nums_combo in datos:
        rest = Restaurante(
            p_nombre=nombre,
            p_cedula_juridica=cedula,
            p_direccion=direccion,
            p_tipo_de_comida=tipo,
        )
        for num in nums_combo:
            rest.agregar_combo(Combo(num, nombres_combos[num]))
        restaurantes.append(rest)

    return restaurantes


# ── Clientes (5) ─────────────────────────────────────────────────────────────


def _crear_clientes():
    datos = [
        (123456789, "clave123", "Ana Rodríguez", "ana@correo.com", 88881111, 411111111111, "Heredia, San Francisco"),
        (234567890, "clave234", "Carlos Mora", "carlos@correo.com", 88882222, 422222222222, "San José, Escazú"),
        (345678901, "clave345", "Laura Jiménez", "laura@correo.com", 88883333, 433333333333, "Cartago, Tres Ríos"),
        (456789012, "clave456", "Diego Vargas", "diego@correo.com", 88884444, 444444444444, "Alajuela, San Ramón"),
        (567890123, "clave567", "María Solano", "maria@correo.com", 88885555, 455555555555, "Heredia, Barva"),
    ]

    return [
        Cliente(
            p_cedula=ced, p_contrasenia=pw, p_nombre=nom, p_correo=correo,
            p_telefono=tel, p_num_de_tarjeta=tarj, p_estado=EstadoDeCuenta.ACTIVO,
            p_direccion=dire,
        )
        for ced, pw, nom, correo, tel, tarj, dire in datos
    ]


# ── Repartidores (3) ─────────────────────────────────────────────────────────


def _crear_repartidores():
    datos = [
        (987654321, "moto456", "Beto Vargas", "beto@correo.com", 87771111, 511111111111, 9, 8, 9),
        (876543210, "moto789", "José Ramírez", "jose@correo.com", 87772222, 522222222222, 7, 7, 8),
        (765432109, "moto012", "Sofía Hernández", "sofia@correo.com", 87773333, 533333333333, 8, 9, 7),
    ]

    repartidores = []
    for ced, pw, nom, correo, tel, tarj, amb, tiempo, pres in datos:
        calif = CalificacionDelRepartidor(
            p_calificacion=0,
            p_amabilidad=amb,
            p_tiempo_de_respuesta=tiempo,
            p_presentacion=pres,
            p_num_de_pedidos_hechos=0,
        )
        # No se llama calcular_promedio() al crear; se evalúa al entregar pedido
        rep = Repartidor(
            p_cedula=ced, p_contrasenia=pw, p_nombre=nom, p_correo=correo,
            p_telefono=tel, p_num_de_tarjeta=tarj, p_estado=EstadoDeCuenta.ACTIVO,
            p_num_de_amonestaciones=0, p_calificacion=calif, p_disponibilidad=True,
        )
        repartidores.append(rep)

    return repartidores


# ── Pedidos (5) con facturas calculadas ──────────────────────────────────────


def _crear_pedidos(clientes, restaurantes, repartidores, pedido_repo):
    ana, carlos, laura, diego, maria = clientes
    pollo, soda, pizza, sushi, taco, burger, cafe = restaurantes
    beto, jose, sofia = repartidores

    pedidos_config = [
        # (id, cliente, restaurante, combos_indices, distancia, feriado)
        (1, ana, pollo, [0, 1], 3.5, False),
        (2, carlos, pizza, [0, 1], 5.0, False),
        (3, laura, sushi, [0, 1], 7.0, True),
        (4, diego, taco, [0, 1], 2.0, False),
        (5, maria, cafe, [0, 1], 4.5, False),
    ]

    for pid, cliente, rest, combo_idx, dist, feriado in pedidos_config:
        factura = Factura()
        for idx in combo_idx:
            factura.agregar_combo(rest.menu[idx])

        factura.calcular_subtotal()
        factura.calcular_costo_del_transporte(dist, feriado)
        factura.calcular_iva()
        factura.calcular_total()

        pedido = Pedido(
            p_id=pid,
            p_cliente=cliente,
            p_repartidor=None,
            p_restaurante=rest,
            p_factura=factura,
            p_estado=EstadoDelPedido.EN_PREPARACION,
            p_distancia_km=dist,
            p_es_feriado=feriado,
        )

        rest.registrar_pedido(factura.total)
        cliente.agregar_pedido_al_historial(pedido)
        pedido_repo.crear(pedido)

    # Asignar repartidor al pedido 2 (Carlos → Pizza Planet → Beto)
    pedido2 = pedido_repo.obtener_por_id(2)
    pedido2.asignar_repartidor_interno(beto)
    beto.actualizar_disponibilidad(False)

    # Asignar repartidor al pedido 3 (Laura → Sushi Express → José)
    pedido3 = pedido_repo.obtener_por_id(3)
    pedido3.asignar_repartidor_interno(jose)
    jose.actualizar_disponibilidad(False)


# ── Quejas (3) ───────────────────────────────────────────────────────────────


def _registrar_quejas(repartidores):
    _beto, jose, _sofia = repartidores

    jose.incrementar_amonestacion("Llegó tarde a la entrega")
    jose.incrementar_amonestacion("Pedido entregado frío")
    jose.incrementar_amonestacion("Mala actitud con el cliente")
