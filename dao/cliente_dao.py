"""Módulo de acceso a datos (DAO) para la entidad Cliente."""

import logging
from typing import List, Optional
from mysql.connector import Error

from database.conexion import Conexion
from modelos.cliente import Cliente

logger = logging.getLogger(__name__)


class ClienteDAO:
    """Clase DAO para gestionar las operaciones CRUD de Cliente en MySQL."""

    _TABLA = "clientes"

    @staticmethod
    def crear(cliente: Cliente) -> Optional[int]:
        """Inserta un nuevo cliente en la base de datos y retorna su id generado.

        Args:
            cliente: Objeto Cliente con los datos a persistir.

        Returns:
            int con el ID generado si la inserción fue exitosa, None en caso de error.
        """
        sql = f"""
            INSERT INTO {ClienteDAO._TABLA} (nombre, telefono, email, estado)
            VALUES (%s, %s, %s, %s)
        """
        valores = (cliente.nombre, cliente.telefono, cliente.email, cliente.estado)

        try:
            with Conexion() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, valores)
                    cliente.id_cliente = cursor.lastrowid
                    return cliente.id_cliente
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al crear cliente: %s", e)
            return None

    @staticmethod
    def obtener_por_id(id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su identificador único.

        Args:
            id_cliente: ID del cliente a buscar.

        Returns:
            Instancia de Cliente si se encuentra, None en caso contrario.
        """
        sql = f"""
            SELECT id_cliente, nombre, telefono, email, estado, fecha_registro
            FROM {ClienteDAO._TABLA}
            WHERE id_cliente = %s
        """
        try:
            with Conexion() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, (id_cliente,))
                    fila = cursor.fetchone()
                    if fila:
                        return Cliente(
                            id_cliente=fila["id_cliente"],
                            nombre=fila["nombre"],
                            telefono=fila["telefono"],
                            email=fila["email"],
                            estado=fila["estado"],
                            fecha_registro=fila["fecha_registro"],
                        )
                    return None
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al obtener cliente por ID (%s): %s", id_cliente, e)
            return None

    @staticmethod
    def obtener_por_telefono(telefono: str) -> Optional[Cliente]:
        """Obtiene un cliente a partir de su número de teléfono.

        Args:
            telefono: Número de teléfono a buscar.

        Returns:
            Instancia de Cliente si se encuentra, None en caso contrario.
        """
        sql = f"""
            SELECT id_cliente, nombre, telefono, email, estado, fecha_registro
            FROM {ClienteDAO._TABLA}
            WHERE telefono = %s
        """
        try:
            with Conexion() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, (telefono,))
                    fila = cursor.fetchone()
                    if fila:
                        return Cliente(
                            id_cliente=fila["id_cliente"],
                            nombre=fila["nombre"],
                            telefono=fila["telefono"],
                            email=fila["email"],
                            estado=fila["estado"],
                            fecha_registro=fila["fecha_registro"],
                        )
                    return None
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al obtener cliente por teléfono (%s): %s", telefono, e)
            return None

    @staticmethod
    def listar_todos() -> List[Cliente]:
        """Lista todos los clientes registrados en la base de datos.

        Returns:
            Lista de instancias de Cliente.
        """
        sql = f"""
            SELECT id_cliente, nombre, telefono, email, estado, fecha_registro
            FROM {ClienteDAO._TABLA}
            ORDER BY id_cliente DESC
        """
        clientes: List[Cliente] = []
        try:
            with Conexion() as conexion:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(sql)
                    filas = cursor.fetchall()
                    for fila in filas:
                        clientes.append(
                            Cliente(
                                id_cliente=fila["id_cliente"],
                                nombre=fila["nombre"],
                                telefono=fila["telefono"],
                                email=fila["email"],
                                estado=fila["estado"],
                                fecha_registro=fila["fecha_registro"],
                            )
                        )
            return clientes
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al listar clientes: %s", e)
            return []

    @staticmethod
    def actualizar(cliente: Cliente) -> bool:
        """Actualiza los datos de un cliente existente.

        Args:
            cliente: Objeto Cliente con los datos actualizados (requiere id_cliente).

        Returns:
            True si se actualizó al menos una fila, False en caso contrario.
        """
        if not cliente.id_cliente:
            logger.warning("Intento de actualizar un cliente sin id_cliente.")
            return False

        sql = f"""
            UPDATE {ClienteDAO._TABLA}
            SET nombre = %s, telefono = %s, email = %s, estado = %s
            WHERE id_cliente = %s
        """
        valores = (
            cliente.nombre,
            cliente.telefono,
            cliente.email,
            cliente.estado,
            cliente.id_cliente,
        )

        try:
            with Conexion() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(sql, valores)
                    return cursor.rowcount > 0
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al actualizar cliente (%s): %s", cliente.id_cliente, e)
            return False

    @staticmethod
    def eliminar_logico(id_cliente: int) -> bool:
        """Realiza una eliminación lógica desactivando al cliente (estado = 'INACTIVO').

        Args:
            id_cliente: ID del cliente a desactivar.

        Returns:
            True si se actualizó el estado correctamente, False en caso contrario.
        """
        sql = f"""
            UPDATE {ClienteDAO._TABLA}
            SET estado = 'INACTIVO'
            WHERE id_cliente = %s
        """
        try:
            with Conexion() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(sql, (id_cliente,))
                    return cursor.rowcount > 0
        except (Error, ConnectionError, Exception) as e:
            logger.error("Error al eliminar lógicamente el cliente (%s): %s", id_cliente, e)
            return False
