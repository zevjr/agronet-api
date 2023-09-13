"""
## Módulo de Configuração.
Esse módulo é responsável por definir as configurações do serviço.

Attributes:
    environment: Ambiente de execução, podendo ser (dev, prod, test, hml).
    service_name: Define o nome do serviço, por padrão é @maistodos/api.
    log_level: Define o nível de log, por padrão é INFO.
    is_sqlite: Define se o banco de dados é sqlite, por padrão é True.

    database_url: Define a url do banco de dados,
    por padrão é sqlite:///db.db, caso a variavel `is_sqlite` seja True .

    secret_key: Define a chave secreta para geração do token, por padrão é secret.
    algorithm: Define o algoritmo de geração do token, por padrão é HS256.
    token_expire: Define o tempo de expiração do token, por padrão é 30 minutos.

"""
import logging
import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


logger = logging.getLogger(__name__)


def getenv(env: str, default: Any = "") -> str:

    return os.getenv(env, default)


class APISettings(BaseSettings):
    """
    As variaveis de ambiente são definidas no arquivo .env na raiz do projeto.

    """

    environment: str = getenv("ENVIRONMENT", "dev")
    service_name: str = "AgroNet Api"
    log_level: str = getenv("LOG_LEVEL", "INFO")
    is_sqlite: bool = bool(getenv("IS_SQLITE", True))

    secret_key: str = getenv("SECRET_KEY", "secret")
    algorithm: str = getenv("ALGORITHM", "HS256")
    token_expire: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # database settings
    postgres_driver: str = "asyncpg"
    postgres_user: str = getenv("POSTGRES_USER")
    postgres_password: str = getenv("POSTGRES_PASSWORD")
    postgres_server: str = getenv("POSTGRES_SERVER")
    postgres_port: int = int(getenv("POSTGRES_PORT", 5432))
    postgres_db: str = getenv("POSTGRES_DB")

    @property
    def database_url(self) -> str:
        """Create a valid Postgres database url."""
        return f"postgresql+{self.postgres_driver}://"\
        f"{self.postgres_user}:{self.postgres_password}@"\
        f"{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"


    class Config:
        validate_assignment = True


@lru_cache()
def get_api_settings() -> APISettings:
    """
    This function returns a cached instance of the APISettings object.

    Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.

    If you want to change an environment variable and reset the cache (e.g., during testing), this can be done
    using the `lru_cache` instance method `get_api_settings.cache_clear()`.
    """
    return APISettings()
