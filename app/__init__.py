"""
## Modulo Inical.
Nesse modulo inicial é onde é criado o app FastAPI,
 e adicionado os middlewares e rotas.

- Para acessar as informações de configuração,
basta importar o módulo `config` e acessar o atributo `settings`.
- As rotas estão disponiveis no módulo `routes`.
"""


import logging
import logging.config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import get_api_settings 
from app.db.db_session import initialize_database
from app.routes import api_router_v1

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Cria o app FastAPI e adiciona os middlewares e rotas.

    """
    app = FastAPI(
        title=get_api_settings().service_name, docs_url="/api/docs", redoc_url="/api/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router_v1, prefix="/api")

    app.on_event("startup")(initialize_database)

    logger.info(f"starting app {get_api_settings().service_name}")

    return app
