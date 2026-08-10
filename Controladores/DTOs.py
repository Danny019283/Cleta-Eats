"""
DTOs (Data Transfer Objects) para la comunicación entre la vista y los controladores.

Todos los DTOs son inmutables (frozen dataclasses) y representan datos de
entrada/salida entre capas. No almacenan estado mutable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ── DTOs de entrada ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class CrearClienteDTO:
    cedula: int
    contrasenia: str
    nombre: str
    correo: str
    telefono: int
    num_de_tarjeta: int
    direccion: str


@dataclass(frozen=True)
class CambiarEstadoClienteDTO:
    cedula: int
    nuevo_estado: str  # "ACTIVO" o "SUSPENDIDO"


@dataclass(frozen=True)
class CrearRepartidorDTO:
    cedula: int
    contrasenia: str
    nombre: str
    correo: str
    telefono: int
    num_de_tarjeta: int


@dataclass(frozen=True)
class CrearRestauranteDTO:
    nombre: str
    cedula_juridica: int
    direccion: str
    tipo_de_comida: str


@dataclass(frozen=True)
class CrearComboDTO:
    num_de_combo: int
    nombre: str


@dataclass(frozen=True)
class RealizarPedidoDTO:
    cedula_cliente: int
    cedula_juridica_restaurante: int
    numeros_de_combos: List[int] = field(default_factory=list)
    distancia_km: float = 0.0
    es_feriado: bool = False


@dataclass(frozen=True)
class AsignarRepartidorDTO:
    id_pedido: int
    cedula_repartidor: int


@dataclass(frozen=True)
class EntregarPedidoDTO:
    id_pedido: int
    # Opcionales para CU-13 (Calificar al entregar)
    calificar: bool = False
    amabilidad: int = 5
    tiempo_de_respuesta: int = 5
    presentacion: int = 5


@dataclass(frozen=True)
class ActualizarEstadoPedidoDTO:
    id_pedido: int
    nuevo_estado: str  # "EN_CAMINO" o "SUSPENDIDO"


@dataclass(frozen=True)
class QuejaRepartidorDTO:
    cedula_repartidor: int
    motivo: str


@dataclass(frozen=True)
class CalcularPagoDTO:
    cedula_repartidor: int
    es_feriado: bool = False


# ── DTOs de salida (resultados) ──────────────────────────────────────────────


@dataclass(frozen=True)
class ResultadoDTO:
    """Resultado genérico devuelto por los controladores a la vista."""
    exitoso: bool
    mensaje: str
    datos: Optional[object] = None
