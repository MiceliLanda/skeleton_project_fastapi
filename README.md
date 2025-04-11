# Guía de Uso del Proyecto

## VirtualEnv
### Creación del entorno virtual (Windows/Linux (usa "python3" si es necesario))
```bash
python -m venv <nombre_env>
```

### Activar entorno virtual
# Windows
```bash
.\<nombre_env>\Scripts\activate
```

# Linux/MacOS
```bash
source <nombre_env>/bin/activate
```

# Desactivar (cualquier SO)
```bash
deactivate
```

### Instalación de dependencias
- **Dependencias**: Asegúrate de tener todas las dependencias necesarias instaladas antes de correr el proyecto. Puedes hacerlo ejecutando:
```bash
pip install -r requirements.txt`
```

## Variables de Entorno
Asegúrate de tener el archivo `.env` configurado correctamente con las siguientes variables:

- **SECRET_KEY**=<tu_clave_secreta_cifrado_jwt>
- **ALGORITHM**=<algoritmo_de_encriptación>
- **ACCESS_TOKEN_EXPIRE_MINUTES**=<tiempo_de_expiración>

Configuración de conexión a gestor de base de datos
- **DB_HOST**=<ip_configuracion_db>
- **DB_PORT**=<puerto_conexión_db>
- **DB_USER**=<usuario_db>
- **DB_PASSWORD**=<contraseña_db>
- **DB_NAME**=<nombre_db>

Usuario que se crea por defecto como administrador
- **ADMIN_USERNAME**=<nombre_usuario>
- **ADMIN_EMAIL**=<correo_electrónico>
- **ADMIN_PASSWORD**=<contraseña_default>

### Inicializar Configuración de alembic
Para inicializar la configuración de Alembic ejecuta (fuera de la carpeta /src)
```bash
alembic init alembic
```

- Agrega estas lineas de código para que detecte nuestro archivo de configuración de alembic en el archivo "alembic/env.py"

```Python
import os
import sys
from logging.config import fileConfig
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
fileConfig(os.path.join(BASE_DIR, 'alembic.ini'))
```

### Configurar url de la base de datos en el archivo "alembic/env.py"
- **Importante:** No olvides importar `load_dotenv`
```Python
from dotenv import load_dotenv
load_dotenv()
```
- Debe estar al inicio del archivo, antes de usar `os.getenv()`.
-  **Configuración:** Debajo de la variable config agregar esta linea de código para vincular la configuración de la url de la db: 
```Python
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

config = context.config
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
```

### Agregar SQLModel para que alembic reconozca nuestros modelos
Se agrega esta linea para importar:
```Python
from sqlmodel import SQLModel
```

### Agregar nuestros modelos
Se agrega esta linea para importar los modelos precargados en el proyecto: 
```Python
from src.models import User,UserCredentials,UserPermissions,Permissions
```
- **Importante:** Cada que se cree un nuevo modelo agregar a las importaciones

### Cambiar objetivo de SQLModel
Se agrega esta linea para que alembic reconozca los modelos de las tablas, debajo de las configuraciones:
```Python
target_metadata = SQLModel.metadata
```

### Generar Archivo de Revisión de Tablas Antes de la Migración
Para generar un archivo de migración que refleje los cambios en las tablas antes de migrar, ejecuta:
```bash
alembic revision --autogenerate -m "mensaje de la migración"
```
Este archivo de migración se ubicará en la carpeta `alembic/versions/`.
Ahí podrás corroborar que tus tablas estén correctamente construidas antes de la migración.

### Correr la Migración
Para aplicar las migraciones, ejecuta el siguiente comando:
```bash
alembic upgrade head
```

## Comandos de FastAPI
### Correr el Proyecto
Para ejecutar el proyecto, usa el siguiente comando:
```bash
fastapi dev src/main.py
```

## Notas
- La base de datos se maneja a través de Alembic y SQLAlchemy. Asegúrate de crear la base de datos antes de migrar ya que Alembic no la crea automáticamente.

- El proyecto cuenta con archivo de configuración de Docker para la creación de imagen del mismo.

- Para la creación del usuario admin se tiene un observer el cual se ejecuta de manera automática al iniciar la app, si esto no sucede puedes ejecutar la creación mediante CLI de la siguiente manera.
```bash
python .\src\cli.py create-admin-cli
```
