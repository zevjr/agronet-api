"""
## Modulo de Autenticação e Autorização
Nesse Módulo é onde é definido as funções de autenticação e autorização.
Esse modulo foi construido em separa, para facilitar a reutilização
 em outras partes do projetos,
alem de ficar mais organizado e visivel, facilitando a manutenção.
"""
import logging
from datetime import datetime, timedelta

from fastapi import Header, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import BaseModel

from app.config import get_api_settings

logger = logging.getLogger(__name__)


class Token(BaseModel):
    access_token: str
    token_type: str


class Auth(BaseModel):
    username: str


def raise_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"token": "Bearer"},
    )


def raise_expired_token():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Cria um token de acesso usando os dados do usuário e o tempo de expiração fornecidos.

     Esta função gera um token de acesso JSON Web Token (JWT) usando os dados do usuário fornecidos
     e um tempo de expiração opcional. Se nenhum prazo de expiração for fornecido, o token será
     expiram após 15 minutos por padrão.

    Args:
        data (dict): Um dicionário contendo dados específicos do usuário a serem codificados no token.
        expires_delta (timedelta | None, optional): O intervalo de tempo após o qual o token irá expirar.

    Se None, o token expirará após 15 minutos por padrão. (Padrão: None)

    Returns:
        value (str): O token de acesso JWT codificado.

    Example:
        user_data = {"user_id": 123, "username": "example_user"}
        token = create_access_token(user_data, expires_delta=timedelta(hours=2))
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, get_api_settings().secret_key, algorithm=get_api_settings().algorithm
    )
    return encoded_jwt


def get_current_username(token: str = Header()):
    """
    Verifica a validade de um token de acesso.

    Esta função verifica a validade de um token de acesso fornecido. O token é decodificado
    usando a chave secreta configurada e o algoritmo especificado nas configurações do projeto.

    Args:
        token (str, optional): O token de acesso a ser verificado. Padrão é obtido do cabeçalho da requisição.

    Returns:
        value (str): O nome de usuário associado ao token, se o token for válido.

    Raises:
        TokenInvalido: Se o token não for válido ou estiver ausente.

    Example:
        try:
            username = check_token(token)
            print(f"Token válido para o usuário: {username}")
        except TokenInvalido:
            print("Token inválido ou ausente")
    """
    payload: dict = {}
    try:
        payload = jwt.decode(
            token, get_api_settings().secret_key, algorithms=[get_api_settings().algorithm]
        )
    except ExpiredSignatureError:
        raise_expired_token()
    except JWTError:
        raise_exception()

    username = payload.get("sub", None)
    if username is None or {}:
        raise_exception()

    return username
