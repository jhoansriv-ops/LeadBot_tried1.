"""Módulo de vista interactiva por consola para la entidad Cliente."""

import os
import logging
from typing import Optional

from dao import ClienteDAO
from modelos import Cliente

logger = logging.getLogger(__name__)

# ─── Colores ANSI ────────────────────────────────────────────────────────────
_VERDE = "\033[92m"
_ROJO  = "\033[91m"
_CYAN  = "\033[96m"
_BOLD  = "\033[1m"
_DIM   = "\033[2m"
_RESET = "\033[0m"


def _ok(msg: str) -> None:
    """Imprime un mensaje de éxito con prefijo [OK] en verde."""
    print(f"  {_VERDE}[OK]{_RESET} {msg}")


def _err(msg: str) -> None:
    """Imprime un mensaje de error con prefijo [ERROR] en rojo."""
    print(f"  {_ROJO}[ERROR]{_RESET} {msg}")


def _info(msg: str) -> None:
    """Imprime un mensaje informativo con prefijo [INFO] en cyan."""
    print(f"  {_CYAN}[INFO]{_RESET} {msg}")


def _limpiar_pantalla() -> None:
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def _leer_texto(prompt: str, requerido: bool = True) -> Optional[str]:
    """Solicita un texto al usuario, permitiendo cancelar con 'q'."""
    while True:
        valor = input(f"  {prompt} (o 'q' para cancelar): ").strip()
        if valor.lower() == "q":
            _info("Operación cancelada por el usuario.")
            return None
        if requerido and not valor:
            _err("Este campo no puede estar vacío. Intente de nuevo.")
            continue
        return valor


def _leer_entero(prompt: str) -> Optional[int]:
    """Solicita un numero entero al usuario, permitiendo cancelar con 'q'."""
    while True:
        valor = input(f"  {prompt} (o 'q' para cancelar): ").strip()
        if valor.lower() == "q":
            _info("Operacion cancelada por el usuario.")
            return None
        if not valor.isdigit():
            _err("Ingrese un numero entero valido.")
            continue
        return int(valor)


def _imprimir_cliente(cliente: Cliente, titulo: str = "Datos del Cliente") -> None:
    """Imprime los datos de un cliente en formato tabulado."""
    print(f"\n  {_BOLD}{titulo}{_RESET}")
    print(f"  {'-' * 50}")
    print(f"  {'ID:':<20} {cliente.id_cliente}")
    print(f"  {'Nombre:':<20} {cliente.nombre}")
    print(f"  {'Telefono:':<20} {cliente.telefono}")
    print(f"  {'Email:':<20} {cliente.email}")
    print(f"  {'Estado:':<20} {cliente.estado}")
    print(f"  {'Fecha Registro:':<20} {cliente.fecha_registro}")
    print(f"  {'-' * 50}")


def _imprimir_encabezado(titulo: str) -> None:
    """Imprime el encabezado de cada seccion del menu."""
    print(f"\n  {_BOLD}{_CYAN}{'=' * 55}{_RESET}")
    print(f"  {_BOLD}{_CYAN}  {titulo.upper()}{_RESET}")
    print(f"  {_BOLD}{_CYAN}{'=' * 55}{_RESET}\n")


# --- Opciones del menu -------------------------------------------------------

def _registrar_cliente() -> None:
    """Solicita datos y crea un nuevo cliente en la base de datos."""
    _imprimir_encabezado("Registrar Nuevo Cliente")

    nombre = _leer_texto("Nombre completo")
    if nombre is None:
        return

    telefono = _leer_texto("Telefono")
    if telefono is None:
        return

    email = _leer_texto("Email", requerido=False)
    if email is None:
        return

    nuevo_cliente = Cliente(nombre=nombre, telefono=telefono, email=email or "")
    id_generado = ClienteDAO.crear(nuevo_cliente)

    if id_generado:
        _ok(f"Cliente registrado con exito. ID asignado: {_BOLD}{id_generado}{_RESET}")
    else:
        _err(
            "No fue posible registrar el cliente en MySQL. "
            "Revise los logs o verifique que el telefono no este duplicado."
        )




def _consultar_por_id() -> None:
    """Busca y muestra un cliente por su ID."""
    _imprimir_encabezado("Consultar Cliente por ID")

    id_cliente = _leer_entero("Ingrese el ID del cliente")
    if id_cliente is None:
        return

    cliente = ClienteDAO.obtener_por_id(id_cliente)
    if cliente:
        _imprimir_cliente(cliente, titulo="Cliente Encontrado")
    else:
        _err(f"No se encontro ningun cliente con ID {id_cliente}.")


def _consultar_por_telefono() -> None:
    """Busca y muestra un cliente por numero de telefono."""
    _imprimir_encabezado("Consultar Cliente por Telefono")

    telefono = _leer_texto("Ingrese el telefono del cliente")
    if telefono is None:
        return

    cliente = ClienteDAO.obtener_por_telefono(telefono)
    if cliente:
        _imprimir_cliente(cliente, titulo="Cliente Encontrado")
    else:
        _err(f"No se encontro ningun cliente con telefono '{telefono}'.")


def _listar_todos() -> None:
    """Muestra en tabla todos los clientes registrados."""
    _imprimir_encabezado("Listado de Todos los Clientes")

    clientes = ClienteDAO.listar_todos()
    if not clientes:
        _info("No hay clientes registrados en la base de datos.")
        return

    _ok(f"Total de clientes encontrados: {len(clientes)}\n")
    encabezado = f"  {'ID':<6} {'Nombre':<30} {'Telefono':<18} {'Email':<28} {'Estado'}"
    print(f"  {_BOLD}{encabezado}{_RESET}")
    print(f"  {'-' * 95}")
    for cli in clientes:
        fila = (
            f"  {cli.id_cliente:<6} {cli.nombre:<30} {cli.telefono:<18} "
            f"{cli.email:<28} {cli.estado}"
        )
        color = _DIM if cli.estado == "INACTIVO" else ""
        print(f"{color}{fila}{_RESET}")
    print(f"  {'-' * 95}")


def _actualizar_cliente() -> None:
    """Actualiza los datos de un cliente existente."""
    _imprimir_encabezado("Actualizar Datos de un Cliente")

    id_cliente = _leer_entero("Ingrese el ID del cliente a actualizar")
    if id_cliente is None:
        return

    cliente = ClienteDAO.obtener_por_id(id_cliente)
    if not cliente:
        _err(f"No se encontro ningun cliente con ID {id_cliente}.")
        return

    _imprimir_cliente(cliente, titulo="Datos Actuales")
    print(f"\n  {_DIM}Presione Enter para conservar el valor actual.{_RESET}\n")

    nombre_nuevo = input(f"  Nuevo nombre [{cliente.nombre}]: ").strip()
    telefono_nuevo = input(f"  Nuevo telefono [{cliente.telefono}]: ").strip()
    email_nuevo = input(f"  Nuevo email [{cliente.email}]: ").strip()

    cliente.nombre = nombre_nuevo if nombre_nuevo else cliente.nombre
    cliente.telefono = telefono_nuevo if telefono_nuevo else cliente.telefono
    cliente.email = email_nuevo if email_nuevo else cliente.email

    actualizado = ClienteDAO.actualizar(cliente)
    if actualizado:
        _ok("Datos del cliente actualizados correctamente.")
        _imprimir_cliente(cliente, titulo="Datos Actualizados")
    else:
        _err("No fue posible actualizar el cliente. Intente de nuevo.")


def _inactivar_cliente() -> None:
    """Realiza la eliminacion logica (estado = INACTIVO) de un cliente."""
    _imprimir_encabezado("Inactivar Cliente (Borrado Logico)")

    id_cliente = _leer_entero("Ingrese el ID del cliente a inactivar")
    if id_cliente is None:
        return

    cliente = ClienteDAO.obtener_por_id(id_cliente)
    if not cliente:
        _err(f"No se encontro ningun cliente con ID {id_cliente}.")
        return

    if cliente.estado == "INACTIVO":
        _info(f"El cliente '{cliente.nombre}' ya se encuentra INACTIVO.")
        return

    _imprimir_cliente(cliente, titulo="Cliente a Inactivar")
    confirmar = input(
        f"\n  {_ROJO}Confirma inactivar al cliente '{cliente.nombre}'? "
        f"(s/n){_RESET}: "
    ).strip().lower()

    if confirmar != "s":
        _info("Operacion cancelada. El cliente no fue modificado.")
        return

    eliminado = ClienteDAO.eliminar_logico(id_cliente)
    if eliminado:
        _ok(f"Cliente '{cliente.nombre}' marcado como INACTIVO correctamente.")
    else:
        _err("No fue posible inactivar el cliente. Intente de nuevo.")


# --- Menu principal ----------------------------------------------------------

def _mostrar_menu() -> None:
    """Imprime el menu principal del modulo Cliente."""
    print(f"\n  {_BOLD}{'=' * 55}{_RESET}")
    print(f"  {_BOLD}{'   LEADBOT - GESTION DE CLIENTES':^55}{_RESET}")
    print(f"  {_BOLD}{'=' * 55}{_RESET}")
    print(f"  {_CYAN}  [1]{_RESET} Registrar nuevo cliente")
    print(f"  {_CYAN}  [2]{_RESET} Consultar cliente por ID")
    print(f"  {_CYAN}  [3]{_RESET} Consultar cliente por telefono")
    print(f"  {_CYAN}  [4]{_RESET} Listar todos los clientes")
    print(f"  {_CYAN}  [5]{_RESET} Actualizar datos de un cliente")
    print(f"  {_CYAN}  [6]{_RESET} Inactivar cliente (borrado logico)")
    print(f"  {_ROJO}  [0]{_RESET} Salir")
    print(f"  {'-' * 55}")


_ACCIONES = {
    "1": _registrar_cliente,
    "2": _consultar_por_id,
    "3": _consultar_por_telefono,
    "4": _listar_todos,
    "5": _actualizar_cliente,
    "6": _inactivar_cliente,
}


def iniciar() -> None:
    """Punto de entrada del modulo Cliente. Inicia el bucle de menu principal."""
    while True:
        _mostrar_menu()
        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "0":
            print(f"\n  {_BOLD}Hasta luego. Cerrando LeadBot...{_RESET}\n")
            break

        accion = _ACCIONES.get(opcion)
        if accion:
            try:
                accion()
            except (KeyboardInterrupt, EOFError):
                print()
                _info("Interrupcion recibida. Volviendo al menu principal.")
        else:
            _err(f"Opcion '{opcion}' no reconocida. Ingrese un numero del 0 al 6.")

        input(f"\n  {_DIM}Presione Enter para continuar...{_RESET}")

