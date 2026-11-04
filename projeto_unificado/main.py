from contextlib import asynccontextmanager
import importlib
import pkgutil

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Banco de dados
from data.context import Base, SessionLocal, engine

# Importa automaticamente todos os modelos do SQLAlchemy
import models

for _, module_name, _ in pkgutil.iter_modules(models.__path__):
    if module_name != "main":
        importlib.import_module(f"models.{module_name}")

from models.farmaceutico import Farmaceutico
from models.usuario import Usuario

# Rotas do CoppeliaSim
from routers import objetos, simulacao

# Rotas do DozzaHealth
from models.router import router as auth_cadastro_router  # Rotas de Login, Cadastros e Fracionamento
from search.router import router as busca_router        # Rota de Busca de Medicamentos
from search.services import busca_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Cria as tabelas no SQLite se não existirem
    Base.metadata.create_all(bind=engine)

    # 2. Carrega a base de dados de medicamentos em memória
    if hasattr(busca_service, "carregar_dados"):
        busca_service.carregar_dados()

    # 3. Garante o usuário semente 'testuser' para testes
    db = SessionLocal()
    try:
        test_user = (
            db.query(Usuario).filter(Usuario.login == "testuser").first()
        )
        if not test_user:
            novo_teste = Farmaceutico(
                nome="Usuario Teste",
                login="testuser",
                senha_hash="secretpassword",
                crf="12345",
            )
            db.add(novo_teste)
            db.commit()
            print(">>> [SUCESSO] Usuario 'testuser' pronto para uso!")
        else:
            print(">>> [SUCESSO] Usuario 'testuser' já existe!")
    except Exception as e:
        print(f">>> [ERRO NO STARTUP]: {e}")
        db.rollback()
    finally:
        db.close()

    yield


app = FastAPI(
    title="Plataforma Unificada - DozzaHealth & CoppeliaSim",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração de CORS para liberar o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Endpoints do DozzaHealth
app.include_router(busca_router)
app.include_router(auth_cadastro_router)  # <-- Removido o prefix="/auth" duplicado

# 2. Endpoints do CoppeliaSim
app.include_router(
    simulacao.router, prefix="/api/simulacao", tags=["Coppelia - Simulação"]
)
app.include_router(
    objetos.router, prefix="/api/objetos", tags=["Coppelia - Objetos e Robô"]
)

# 3. Servir os arquivos estáticos do Frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)