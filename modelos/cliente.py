"""Módulo que define el modelo de datos para la entidad Cliente."""

from datetime import datetime
from typing import Any, Dict, Optional


class Cliente:
    """Entidad que representa a un cliente en el sistema LeadBot."""

    def __init__(
        self,
        id_cliente: Optional[int] = None,
        nombre: str = "",
        telefono: str = "",
        email: str = "",
        estado: str = "ACTIVO",
        fecha_registro: Optional[datetime] = None,
    ) -> None:
        """Inicializa una instancia de Cliente.

        Args:
            id_cliente: Identificador único del cliente.
            nombre: Nombre completo del cliente.
            telefono: Teléfono de contacto.
            email: Correo electrónico del cliente.
            estado: Estado del cliente ('ACTIVO', 'INACTIVO', etc.).
            fecha_registro: Fecha y hora de registro en el sistema.
        """
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.estado = estado
        self.fecha_registro = fecha_registro

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad Cliente a un diccionario.

        Returns:
            Dict con los datos del cliente serializados.
        """
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "estado": self.estado,
            "fecha_registro": (
                self.fecha_registro.isoformat()
                if isinstance(self.fecha_registro, datetime)
                else self.fecha_registro
            ),
        }

    def __repr__(self) -> str:
        """Representación textual legible de la instancia."""
        return (
            f"Cliente(id_cliente={self.id_cliente}, nombre='{self.nombre}', "
            f"telefono='{self.telefono}', email='{self.email}', "
            f"estado='{self.estado}', fecha_registro={self.fecha_registro})"
        )
