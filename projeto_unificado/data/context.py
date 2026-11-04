from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from data.base import Base

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Desativa o log SQL para não sobrecarregar o terminal no teste de carga
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Tempo limite para aguardar liberamento do banco sem travar com erro 500
    }
)

# Ativa o modo WAL no SQLite para permitir leituras/escritas concorrentes
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_banco():
    Base.metadata.create_all(bind=engine)