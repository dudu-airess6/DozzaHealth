from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from data.context import SessionLocal
from search.auth import criar_token_jwt
from .schemas import CadastroRequest, CadastroResponse, LoginRequest, LoginResponse
from .auth_service import cadastrar_usuario_db, autenticar_usuario_db

router = APIRouter(prefix="/auth", tags=["Autenticação & Usuários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cadastro", response_model=CadastroResponse, status_code=status.HTTP_201_CREATED)
def cadastro(dados: CadastroRequest, db: Session = Depends(get_db)):
    user_id = cadastrar_usuario_db(dados, db)
    return CadastroResponse(
        mensagem="Usuário cadastrado com sucesso.",
        usuario_id=user_id
    )

@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario_db(dados, db)
    user_id = getattr(usuario, "id", None) or getattr(usuario, "id_usuario", None)
    tipo_usr = getattr(usuario, "tipo_usuario", None) or "Farmaceutico"
    
    token_payload = {
        "sub": str(user_id),
        "nome": getattr(usuario, "nome", "Usuario"),
        "tipo_usuario": tipo_usr,
        "crf": getattr(usuario, "crf", None)
    }
    
    jwt_token = criar_token_jwt(token_payload)

    return LoginResponse(
        mensagem="Login realizado com sucesso.",
        usuario_id=user_id,
        nome=getattr(usuario, "nome", "Usuario"),
        tipo_usuario=tipo_usr,
        access_token=jwt_token,
        token_type="bearer"
    )