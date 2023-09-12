"""
## Modulo de Checagem
Esse módulo é responsável por disponibilizar a rota de checagem de saúde da aplicação.
"""
import logging

from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def health():
    """
    Retorno unico, podendo variar o padrão de acordo com o serviço consumidor.
    """
    logger.info("api is up!")
    return {"message": "OK"}
