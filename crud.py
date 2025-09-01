from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from models import TaskModel, TaskCreate, TaskUpdate, TaskResponse
from database import get_collection

class TaskCRUD:
    def __init__(self):
        self.collection: Optional[AsyncIOMotorCollection] = None
    
    async def get_collection(self):
        if self.collection is None:
            self.collection = await get_collection()
        return self.collection

    async def create_task(self, task: TaskCreate) -> TaskResponse:
        collection = await self.get_collection()
        task_dict = task.model_dump()
        task_dict["completed"] = False
        task_dict["creation_date"] = datetime.now()
        
        result = await collection.insert_one(task_dict)
        created_task = await collection.find_one({"_id": result.inserted_id})
        
        # Convertir ObjectId a string para la respuesta
        created_task["_id"] = str(created_task["_id"])
        return TaskResponse(**created_task)

    async def get_all_tasks(self) -> List[TaskResponse]:
        collection = await self.get_collection()
        tasks = []
        async for task in collection.find():
            # Convertir ObjectId a string para la respuesta
            task["_id"] = str(task["_id"])
            tasks.append(TaskResponse(**task))
        return tasks

    async def get_task_by_id(self, task_id: str) -> Optional[TaskResponse]:
        collection = await self.get_collection()
        if not ObjectId.is_valid(task_id):
            return None
        
        task = await collection.find_one({"_id": ObjectId(task_id)})
        if task:
            # Convertir ObjectId a string para la respuesta
            task["_id"] = str(task["_id"])
            return TaskResponse(**task)
        return None

    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
        collection = await self.get_collection()
        if not ObjectId.is_valid(task_id):
            return None

        update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_task_by_id(task_id)

        result = await collection.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_data}
        )
        
        if result.modified_count == 1:
            return await self.get_task_by_id(task_id)
        return None

    async def delete_task(self, task_id: str) -> bool:
        collection = await self.get_collection()
        if not ObjectId.is_valid(task_id):
            return False

        result = await collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count == 1

task_crud = TaskCRUD()