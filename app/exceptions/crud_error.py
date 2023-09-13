"""
## Modulo que cria as exceções de erro
Módulo que define exceções personalizadas para erros de operações CRUD.
"""

from abc import abstractmethod
import logging

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class CRUDBaseError(HTTPException):
    username: str

    def __init__(self, status=status.HTTP_404_NOT_FOUND) -> None:
        super().__init__(
            status,
            self.erro_message(),
            headers={"X-Username-Error": self.username},
        )

    @abstractmethod
    def erro_message(self):
        ...

class CRUDUpdateError(CRUDBaseError):
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

    def __init__(self, *, obj_id, err=None) -> None:
        self.obj_id = obj_id
        super().__init__()
        logger.error(f"Error updating object {obj_id} from {err}")

    def erro_message(self):
        return f"Not updated, reference object not found, ReferenceObject<{self.obj_id}>"


class CRUDDeleteError(CRUDBaseError):
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

    def __init__(self, *, obj_id, err=None) -> None:
        self.obj_id = obj_id
        super().__init__()
        logger.error(f"Error delete object {obj_id} from {err}")

    def erro_message(self):
        return f"Not deleted, reference object not found, ReferenceObject<{self.obj_id}>"


class CRUDSelectError(CRUDBaseError):
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

    def __init__(self, *, obj_id, err=None) -> None:
        super().__init__()
        self.obj_id = obj_id
        logger.error(f"Error find object {obj_id} from {err}")

    def erro_message(self):
        return f"Not selected, reference object not found, ReferenceObject<{self.obj_id}>"


class CRUDCreateError(CRUDBaseError):
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

    def __init__(self, *, err=None) -> None:
        super().__init__(status.HTTP_409_CONFLICT)
        logger.error(f"Error create object from {err}")

    def erro_message(self):
        return f"Conflict, this card number already exists"
