from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    usuario: str
    senha: str

class LoginResponse(BaseModel):
    mensagem: str
    usuario_id: int
    nome: str
    tipo_usuario: str
    access_token: Optional[str] = None
    token_type: str = "bearer"

class CadastroRequest(BaseModel):
    nome: str
    login: str
    senha: str
    tipo_usuario: str  # "Farmaceutico" ou "Medico"
    crm: Optional[str] = None
    especialidade: Optional[str] = None
    crf: Optional[str] = None

class CadastroResponse(BaseModel):
    mensagem: str
    usuario_id: int