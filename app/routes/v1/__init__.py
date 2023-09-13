"""
## Modulo de Rotas V1

## V1: API inicial

Attributes:
    api_router (method): Router da API v1.

Args:
    router_health (method): Rota de health check.
"""
import logging

from fastapi import APIRouter
from .views import router_health


logger = logging.getLogger(__name__)

api_router = APIRouter()

api_router.include_router(
    router_health,
    prefix="/v1/health",
    tags=["health"],
)
