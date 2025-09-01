# FastAPI Todo API

Una API REST moderna para gestión de tareas construida con FastAPI y MongoDB.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido
- **MongoDB**: Base de datos NoSQL con Motor (driver asíncrono)
- **Pydantic v2**: Validación de datos y serialización
- **CORS**: Configurado para aplicaciones React
- **Logging**: Sistema completo de logs para debugging
- **Documentación automática**: Swagger UI incluido

## 📋 Requisitos

- Python 3.11+
- MongoDB 4.4+
- pip

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd FastApiExample
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install fastapi uvicorn motor pymongo
```

4. **Configurar MongoDB:**
```bash
# Con Docker
docker run -d -p 27017:27017 mongo

# O instalar MongoDB localmente
```

5. **Variables de entorno (opcional):**
```bash
export MONGODB_URL="mongodb://localhost:27017"
```

## 🚀 Uso

### Ejecutar la API

```bash
python main.py
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Página de bienvenida |
| `GET` | `/tasks` | Obtener todas las tareas |
| `POST` | `/tasks` | Crear una nueva tarea |
| `GET` | `/tasks/{task_id}` | Obtener tarea por ID |
| `PUT` | `/tasks/{task_id}` | Actualizar una tarea |
| `DELETE` | `/tasks/{task_id}` | Eliminar una tarea |

### Ejemplos con cURL

**Crear una tarea:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudiar FastAPI",
    "description": "Aprender endpoints y MongoDB"
  }'
```

**Obtener todas las tareas:**
```bash
curl -X GET "http://localhost:8000/tasks"
```

**Marcar tarea como completada:**
```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 📁 Estructura del proyecto

```
FastApiExample/
├── main.py              # Aplicación FastAPI principal
├── models.py            # Modelos Pydantic
├── database.py          # Configuración MongoDB
├── crud.py              # Operaciones CRUD
├── migrate_data.py      # Script de migración
├── requirements.txt     # Dependencias (opcional)
├── README.md           # Este archivo
└── .gitignore          # Archivos ignorados por Git
```

## 🗄️ Esquema de datos

### TaskCreate
```json
{
  "title": "string (requerido)",
  "description": "string (opcional)"
}
```

### TaskResponse
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "creation_date": "datetime"
}
```

## 🔧 Configuración para React

La API está configurada con CORS para funcionar con aplicaciones React en:
- `http://localhost:3000`
- `http://localhost:3001`

### Ejemplo de consumo en React:

```javascript
// Crear tarea
const createTask = async (title, description) => {
  const response = await fetch('http://localhost:8000/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description })
  });
  return response.json();
};

// Obtener tareas
const getTasks = async () => {
  const response = await fetch('http://localhost:8000/tasks');
  return response.json();
};
```

## 🐛 Debugging

La API incluye logging detallado. Los logs aparecen en la consola mostrando:
- Inicio/cierre de aplicación
- Conexiones a MongoDB
- Requests HTTP con detalles
- Errores completos con stack trace

## 🚀 Despliegue

Para producción, considera:
- Usar variables de entorno para configuración
- Configurar HTTPS
- Usar un servidor WSGI como Gunicorn
- Configurar un proxy reverso (Nginx)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ✨ Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [MongoDB](https://www.mongodb.com/) - Base de datos
- [Motor](https://motor.readthedocs.io/) - Driver asíncrono para MongoDB
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI