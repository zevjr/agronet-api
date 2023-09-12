"""
# Modulo de Roteamento
Item usado para flexibliizar o roteamento da aplicação,
e a criação de novas versões de API.
"""

from .v1 import api_router as api_router_v1

__all__ = [
    "api_router_v1",
]
