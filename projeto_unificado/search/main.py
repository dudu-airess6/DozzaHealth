from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Banco de dados e Modelos
from data.context import Base, SessionLocal, engine
import models
from models import Farmaceutico, Usuario

# Rotas do CoppeliaSim
from routers import objetos, simulacao

# Serviços e Rotas do DozzaHealth (pasta search)
from search.auth import router as auth_router
from search.router import router as busca_router
from search.services import busca_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Cria as tabelas do banco SQLite
    Base.metadata.create_all(bind=engine)

    # 2. Carrega a base de dados em memória
    if hasattr(busca_service, "carregar_dados"):
        busca_service.carregar_dados()

    # 3. Garante o usuário semente para testes
    db = SessionLocal()
    try:
        test_user = db.query(Usuario).filter(Usuario.login == "testuser").first()
        if not test_user:
            novo_teste = Farmaceutico(
                nome="Usuario Teste",
                login="testuser",
                senha_hash="secretpassword",
                crf="12345",
            )
            db.add(novo_teste)
            db.commit()
            print(">>> [SUCESSO] Usuario 'testuser' criado!")
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Integrar endpoints do DozzaHealth
app.include_router(busca_router, prefix="/api/v1", tags=["Medicamentos"])
app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])

# Integrar endpoints do CoppeliaSim
app.include_router(
    simulacao.router, prefix="/api/simulacao", tags=["Coppelia - Simulação"]
)
app.include_router(
    objetos.router, prefix="/api/objetos", tags=["Coppelia - Objetos e Robô"]
)

# Servir a aplicação Frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)