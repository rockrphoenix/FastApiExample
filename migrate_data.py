#!/usr/bin/env python3
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def migrate_tasks():
    """Migrar tareas existentes agregando campos faltantes"""
    client = AsyncIOMotorClient(
        os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
    )
    
    db = client.todo_app
    collection = db.tasks
    
    print("Iniciando migración de tareas...")
    
    # Buscar tareas sin completed o creation_date
    tasks_to_update = await collection.find({
        "$or": [
            {"completed": {"$exists": False}},
            {"creation_date": {"$exists": False}}
        ]
    }).to_list(None)
    
    if not tasks_to_update:
        print("No hay tareas que migrar.")
        return
    
    print(f"Encontradas {len(tasks_to_update)} tareas para migrar")
    
    # Actualizar cada tarea
    for task in tasks_to_update:
        update_fields = {}
        
        if "completed" not in task:
            update_fields["completed"] = False
            
        if "creation_date" not in task:
            update_fields["creation_date"] = datetime.now()
        
        if update_fields:
            await collection.update_one(
                {"_id": task["_id"]},
                {"$set": update_fields}
            )
            print(f"Actualizada tarea {task['_id']}: {task.get('title', 'Sin título')}")
    
    print("Migración completada exitosamente!")
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_tasks())