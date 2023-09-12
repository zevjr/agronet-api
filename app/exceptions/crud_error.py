"""
## Modulo que cria as exceções de erro
Módulo que define exceções personalizadas para erros de operações CRUD.
"""

import logging

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class CRUDUpdateError(HTTPException):
    """
    Exceção personalizada para erros de atualização em operações CRUD.

    Esta classe herda da classe HTTPException do módulo FastAPI e é usada para indicar que uma
    operação de atualização não foi bem-sucedida devido à ausência do objeto de referência.

    Atributos:
        username (str): O nome de usuário relacionado ao erro.
        obj_id: O identificador do objeto de referência que não foi encontrado.

    Exemplo:
        Para lançar esta exceção em seu código, você pode fazer o seguinte:

        >>> raise CRUDUpdateError(username="john_doe", obj_id=123)
    """

    def __init__(self, username, *, obj_id) -> None:
        super().__init__(
            404,
            f"Not updated, reference object not found, ReferenceObject<{obj_id}>",
            headers={"X-Username-Error": username},
        )


class CRUDDeleteError(HTTPException):
    """
    Exceção personalizada para erros de exclusão em operações CRUD.

    Esta classe herda da classe HTTPException do módulo FastAPI e é usada para indicar que uma
    operação de exclusão não foi bem-sucedida devido à ausência do objeto de referência.

    Atributos:
        username (str): O nome de usuário relacionado ao erro.
        obj_id: O identificador do objeto de referência que não foi encontrado.

    Exemplo:
        Para lançar esta exceção em seu código, você pode fazer o seguinte:

        >>> raise CRUDDeleteError(username="john_doe", obj_id=123)
    """

    def __init__(self, username, *, obj_id) -> None:
        super().__init__(
            404,
            f"Not deleted, reference object not found, ReferenceObject<{obj_id}>",
            headers={"X-Username-Error": username},
        )


class CRUDSelectError(HTTPException):
    """
    Exceção personalizada para erros de seleção em operações CRUD.

    Esta classe herda da classe HTTPException do módulo FastAPI e é usada para indicar que uma
    operação de seleção não foi bem-sucedida devido à ausência do objeto de referência.

    Atributos:
        username (str): O nome de usuário relacionado ao erro.
        obj_id: O identificador do objeto de referência que não foi encontrado.

    Exemplo:
        Para lançar esta exceção em seu código, você pode fazer o seguinte:

        >>> raise CRUDSelectError(username="john_doe", obj_id=123)
    """

    def __init__(self, username, *, obj_id) -> None:
        super().__init__(
            404,
            f"Item not found, ReferenceObject<{obj_id}>",
            headers={"X-Username-Error": username},
        )


class CRUDCreateError(HTTPException):
    """
    Exceção personalizada para erros de criação em operações CRUD.

    Esta classe herda da classe HTTPException do módulo FastAPI e é usada para indicar que uma
    operação de criação não foi bem-sucedida devido a um conflito ou erro específico.

    Atributos:
        username (str): O nome de usuário relacionado ao erro.
        obj_error: O erro específico ou mensagem de conflito relacionado à criação.

    Exemplo:
        Para lançar esta exceção em seu código, você pode fazer o seguinte:

        >>> raise CRUDCreateError(username="john_doe", obj_error="Número de cartão já existe")
    """

    def __init__(self, username, *, obj_error) -> None:
        super().__init__(
            409,
            f"Conflict, this card number already exists, Error={obj_error}",
            headers={"X-Username-Error": username},
        )
