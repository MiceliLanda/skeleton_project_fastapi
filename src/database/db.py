from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "zdes7iinyy")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "rent_away_app")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Conexión
engine = create_engine(str(DATABASE_URL), echo=True)

# Función para obtener sesión
def get_db():
    with Session(engine) as session:
        yield session

# # Crear las tablas en la base de datos
# def init_db():
#     SQLModel.metadata.create_all(engine)
