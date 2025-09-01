from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class TaskModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = Field(default=False)
    creation_date: datetime = Field(default_factory=datetime.now)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "title": "Completar proyecto FastAPI",
                "description": "Implementar API REST para gestión de tareas",
                "completed": False
            }
        }
    }


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Nueva tarea",
                "description": "Descripción opcional de la tarea"
            }
        }
    }


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Tarea actualizada",
                "description": "Descripción actualizada",
                "completed": True
            }
        }
    }


class TaskResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: Optional[str] = None
    completed: bool
    creation_date: datetime

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Completar proyecto FastAPI",
                "description": "Implementar API REST para gestión de tareas",
                "completed": False,
                "creation_date": "2023-10-01T10:30:00"
            }
        }
    }