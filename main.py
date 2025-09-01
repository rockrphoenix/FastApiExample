from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from models import TaskCreate, TaskUpdate, TaskResponse
from crud import task_crud
from database import connect_to_mongo, close_mongo_connection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="To-Do List API",
    description="Una API REST para gestión de tareas usando FastAPI y MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación...")
    try:
        await connect_to_mongo()
        logger.info("Conexión a MongoDB establecida exitosamente")
    except Exception as e:
        logger.error(f"Error al conectar con MongoDB: {str(e)}", exc_info=True)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Cerrando aplicación...")
    await close_mongo_connection()
    logger.info("Conexión a MongoDB cerrada")

@app.get("/", summary="Página de bienvenida")
async def root():
    return {"message": "Bienvenido a la API de gestión de tareas"}

@app.get("/tasks", response_model=List[TaskResponse], summary="Obtener todas las tareas")
async def get_all_tasks():
    logger.info("Obteniendo todas las tareas")
    try:
        tasks = await task_crud.get_all_tasks()
        logger.info(f"Se obtuvieron {len(tasks)} tareas")
        return tasks
    except Exception as e:
        logger.error(f"Error al obtener las tareas: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las tareas: {str(e)}"
        )

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Crear una nueva tarea")
async def create_task(task: TaskCreate):
    logger.info(f"Creando nueva tarea: {task.title}")
    try:
        new_task = await task_crud.create_task(task)
        logger.info(f"Tarea creada exitosamente con ID: {new_task.id}")
        return new_task
    except Exception as e:
        logger.error(f"Error al crear la tarea: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la tarea: {str(e)}"
        )

@app.get("/tasks/{task_id}", response_model=TaskResponse, summary="Obtener una tarea por ID")
async def get_task(task_id: str):
    logger.info(f"Obteniendo tarea con ID: {task_id}")
    try:
        task = await task_crud.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Tarea con ID {task_id} no encontrada")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        logger.info(f"Tarea obtenida: {task.title}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener la tarea: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la tarea: {str(e)}"
        )

@app.put("/tasks/{task_id}", response_model=TaskResponse, summary="Actualizar una tarea")
async def update_task(task_id: str, task_update: TaskUpdate):
    logger.info(f"Actualizando tarea con ID: {task_id}")
    try:
        updated_task = await task_crud.update_task(task_id, task_update)
        if not updated_task:
            logger.warning(f"Tarea con ID {task_id} no encontrada para actualizar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        logger.info(f"Tarea actualizada exitosamente: {updated_task.title}")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar la tarea: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la tarea: {str(e)}"
        )

@app.delete("/tasks/{task_id}", summary="Eliminar una tarea")
async def delete_task(task_id: str):
    logger.info(f"Eliminando tarea con ID: {task_id}")
    try:
        deleted = await task_crud.delete_task(task_id)
        if not deleted:
            logger.warning(f"Tarea con ID {task_id} no encontrada para eliminar")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        logger.info(f"Tarea con ID {task_id} eliminada exitosamente")
        return {"message": f"Tarea con ID {task_id} eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar la tarea: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la tarea: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)