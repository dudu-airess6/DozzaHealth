from typing import Optional
import traceback
import importlib
import pkgutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # IMPORTADO
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn

from data.base import Base
from data.context import SessionLocal, engine
import models

# Importa automaticamente todos os arquivos da pasta 'models' para resolver mappers
for _, module_name, _ in pkgutil.iter_modules(models.__path__):
    if module_name != "main":
        importlib.import_module(f"models.{module_name}")

from models.usuario import Usuario
from models.farmaceutico import Farmaceutico
from models.medico import Medico

Base.metadata.create_all(bind=engine)

# Gerenciador do ciclo de vida da aplicação (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        test_user = db.query(Usuario).filter(Usuario.login == "testuser").first()
        if not test_user:
            novo_teste = Farmaceutico(
                nome="Usuario Teste",
                login="testuser",
                senha_hash="secretpassword",
                crf="12345"
            )
            db.add(novo_teste)
            db.commit()
            print(">>> [SUCESSO] Usuario 'testuser' pronto para testes do k6!")
        else:
            print(">>> [SUCESSO] Usuario 'testuser' já existe e está pronto!")
    except Exception as e:
        print(f">>> [ERRO NO STARTUP]: {e}")
        db.rollback()
    finally:
        db.close()
    yield

app = FastAPI(title="DozzaHealth API", lifespan=lifespan)

# CONFIGURAÇÃO DE CORS (LIBERA O FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SCHEMAS
class LoginRequest(BaseModel):
    usuario: str
    senha: str

class LoginResponse(BaseModel):
    mensagem: str
    usuario_id: int
    nome: str
    tipo_usuario: str

class CadastroRequest(BaseModel):
    nome: str
    login: str
    senha: str
    tipo_usuario: str
    crm: Optional[str] = None
    especialidade: Optional[str] = None
    crf: Optional[str] = None

class CadastroResponse(BaseModel):
    mensagem: str
    usuario_id: int

# ROTAS
@app.post("/api/login", response_model=LoginResponse, name="Login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.login == dados.usuario).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")

        senha_no_banco = getattr(usuario, "senha_hash", None) or getattr(usuario, "senha", None)
        if senha_no_banco != dados.senha:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")

        user_id = getattr(usuario, "id", None) or getattr(usuario, "id_usuario", None)

        return LoginResponse(
            mensagem="Login realizado com sucesso.",
            usuario_id=user_id,
            nome=getattr(usuario, "nome", "Usuario"),
            tipo_usuario=getattr(usuario, "tipo_usuario", None) or "Farmaceutico",
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        print("\n" + "="*50)
        print("TRACEBACK DO ERRO NO LOGIN:")
        traceback.print_exc()
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/api/cadastro", response_model=CadastroResponse, status_code=201, name="CadastrarUsuario")
def cadastro(dados: CadastroRequest, db: Session = Depends(get_db)):
    login_existente = db.query(Usuario).filter(Usuario.login == dados.login).first()
    if login_existente is not None:
        raise HTTPException(status_code=400, detail="Este login já está em uso.")

    if dados.tipo_usuario == "Medico":
        novo_usuario = Medico(
            nome=dados.nome,
            login=dados.login,
            senha_hash=dados.senha,
            crm=dados.crm,
            especialidade=dados.especialidade,
        )
    elif dados.tipo_usuario == "Farmaceutico":
        novo_usuario = Farmaceutico(
            nome=dados.nome,
            login=dados.login,
            senha_hash=dados.senha,
            crf=dados.crf,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="tipo_usuario deve ser 'Medico' ou 'Farmaceutico'.",
        )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return CadastroResponse(
        mensagem="Usuário cadastrado com sucesso.",
        usuario_id=getattr(novo_usuario, "id", None) or getattr(novo_usuario, "id_usuario", None),
    )

if __name__ == "__main__":
    uvicorn.run("models.main:app", host="127.0.0.1", port=8000, reload=True)