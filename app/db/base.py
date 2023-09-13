"""Abstract CRUD Repo definitions."""
import logging
from typing import Generic, List, TypeVar

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.crud_error import CRUDBaseError, CRUDSelectError, CRUDUpdateError

from models import Base


logger = logging.getLogger(__name__)

## ===== Custom Type Hints ===== ##
# sqlalchemy models
ModelType = TypeVar("ModelType", bound=Base)

# pydantic models
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadOptionalSchemaType = TypeVar("ReadOptionalSchemaType", bound=BaseModel)


## ===== CRUD Repo ===== ##
class SQLAlchemyRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadOptionalSchemaType]):
    """Abstract SQLAlchemy repo defining basic database operations.
    
    Basic CRUD methods used by domain models to interact with the
    database are defined here.
    """
    
    model:  ModelType


    def __init__(
        self,
        db: AsyncSession,
        username: str,
    ) -> None:
        self.db = db

        error = CRUDBaseError()
        error.username = username


    ## ===== Basic Crud Operations ===== ##
    async def create(
        self, 
        obj_new: CreateSchemaType,
        ) -> ModelType | None:
        """Commit new object to the database."""
        try:
            db_obj_new = self.model(**obj_new.model_dump())
            self.db.add(db_obj_new)

            await self.db.commit()
            await self.db.refresh(db_obj_new)
            
            logger.info(f"Created new entity: {db_obj_new}.")

            return db_obj_new

        except Exception as e:

            await self.db.rollback()

            logger.exception("Error while uploading new object to database")
            logger.exception(e)

            return None


    async def read_by_id(
        self,
        id: int,
    ) -> ModelType | None:
        """Get object by id or return None."""
        res = await self.db.get(self.model, id)
        
        return res


    async def read_optional(
        self,
        query_schema: ReadOptionalSchemaType,
    ) -> List[ModelType]:
        """Get list of all objects that match with query_schema.
        
        If values in query schema are not provided, they will default to None and
        will not be searched for. To search for None values specifically provide
        desired value set to None.
        """
        filters: dict = query_schema.model_dump(exclude_unset=True)
        stmt = select(self.model).filter_by(**filters).order_by(self.model.id)

        res = await self.db.execute(stmt)

        if not res.scalars().all():
            CRUDSelectError(obj_id=self.model.id)

        return self.model(res.scalars().all())


    async def delete(
        self,
        id: int,
    ) -> ModelType | None:
        """Delete object from db by id or None if object not found in db"""
        res = await self.db.get(self.model, id)
        if res:

            await self.db.delete(res)
            await self.db.commit()

            logger.info("Entitiy: {res} successfully deleted from database.")

        else:
            logger.error(f"Object with id = {id} not found in query")

        return res

    async def update(
        self,
        id: int,
        update_schema: UpdateSchemaType,
    ) -> ModelType:
        """
        Update an object in the database by
        ID or return None if the object is not found.
        """
        db_obj = await self.db.get(self.model, id)
        

        if not db_obj:
            raise CRUDUpdateError(obj_id=id)
        try:
            for field, value in update_schema.model_dump_json.items():
                setattr(db_obj, field, value)
            
            await self.db.commit()
            
            logger.info(f"Updated entity: {db_obj}.")
        except Exception as e:
            await self.db.rollback()
            raise CRUDUpdateError(obj_id=id, err=e)
        
        return db_obj
