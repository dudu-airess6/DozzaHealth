from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "sua_chave_secreta_super_segura_dozza_health"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

def criar_token_jwt(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um token JWT assinado com tempo de expiração."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def obter_usuario_logado(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Extrai e valida o token JWT enviado no cabeçalho Authorization."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido."
        )

def verificar_acesso_farmaceutico(usuario: dict = Depends(obter_usuario_logado)) -> dict:
    """Garante que apenas usuários do tipo 'Farmaceutico' acessem o recurso."""
    tipo_usuario = usuario.get("tipo_usuario")
    
    if tipo_usuario != "Farmaceutico":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas farmacêuticos credenciados podem realizar buscas."
        )
    return usuario