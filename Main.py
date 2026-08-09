from ClasificaionDelRepartidor import CalificacionDelRepartidor
from Cliente import Cliente
from ClienteServicio import ClienteServicio
from Combo import Combo
from Enums import EstadoDeCuenta, EstadoDelPedido
from Factura import Factura
from Pedido import Pedido
from PedidoServicio import PedidoServicio
from repartidor import Repartidor
from Restaurante import Restaurante


def main():
    #Restaurante y menú
    restaurante = Restaurante(
        p_nombre="Pollo Feliz",
        p_cedula_juridica=3101123456,
        p_direccion="Heredia centro",
        p_tipo_de_comida="rápida",
    )
    restaurante.agregar_combo(Combo(1, "Combo Pollo Individual"))
    restaurante.agregar_combo(Combo(3, "Combo Familiar"))
    restaurante.agregar_combo(Combo(5, "Combo Ejecutivo"))

    # Cliente
    cliente = Cliente(
        p_cedula=123456789,
        p_contrasenia="clave123",
        p_nombre="Ana Rodríguez",
        p_correo="ana@correo.com",
        p_telefono=88881111,
        p_num_de_tarjeta=411111111111,
        p_estado=EstadoDeCuenta.ACTIVO,
        p_direccion="Heredia, San Francisco",
    )

    #Repartidor
    calificacion = CalificacionDelRepartidor(
        p_calificacion=0,
        p_amabilidad=9,
        p_tiempo_de_respuesta=8,
        p_presentacion=9,
        p_num_de_pedidos_hechos=0,
    )
    calificacion.calcular_promedio()

    repartidor = Repartidor(
        p_cedula=987654321,
        p_contrasenia="moto456",
        p_nombre="Beto Vargas",
        p_correo="beto@correo.com",
        p_telefono=87772222,
        p_num_de_tarjeta=511111111111,
        p_estado=EstadoDeCuenta.ACTIVO,
        p_num_de_amonestaciones=0,
        p_calificacion=calificacion,
        p_disponibilidad=True,
    )

    #Pedido 
    factura = Factura()
    factura.agregar_combo(restaurante.menu[0])  # Combo No.1
    factura.agregar_combo(restaurante.menu[1])  # Combo No.3

    pedido = Pedido(
        p_id=1,
        p_cliente=cliente,
        p_repartidor=None,
        p_restaurante=restaurante,
        p_factura=factura,
        p_estado=EstadoDelPedido.EN_PREPARACION,
        p_distancia_km=6.5,
    )

    if ClienteServicio.realizar_pedido(cliente, pedido):
        PedidoServicio.asignar_repartidor(pedido, repartidor)
        pedido.cambiar_estado(EstadoDelPedido.EN_CAMINO)
        PedidoServicio.entregar_pedido(pedido)

    print(pedido)
    print()

    usuarios = [cliente, repartidor]
    for usuario in usuarios:
        print(usuario)


if __name__ == "__main__":
    main()