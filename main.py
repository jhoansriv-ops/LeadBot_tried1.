"""Punto de entrada principal de LeadBot."""

import logging
from vistas import cliente_vista

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

if __name__ == "__main__":
    cliente_vista.iniciar()
