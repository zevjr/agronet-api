"""
Módulo de Visualizações (Views)
Este módulo é responsável por importar e disponibilizar as rotas (endpoints) para diferentes partes da aplicação.

As rotas importadas incluem:
- Rota de status da aplicação (router_health)
"""

from .health import router as router_health

__all__ = [
    "router_health",
]
