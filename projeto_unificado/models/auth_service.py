import traceback
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.usuario import Usuario
from models.farmaceutico import Farmaceutico
from models.medico import Medico
from .schemas import CadastroRequest, LoginRequest

def cadastrar_usuario_db(dados: CadastroRequest, db: Session) -> int:
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
        if not dados.crf:
            raise HTTPException(status_code=400, detail="O CRF é obrigatório para farmacêuticos.")
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

    return getattr(novo_usuario, "id", None) or getattr(novo_usuario, "id_usuario", None)


def autenticar_usuario_db(dados: LoginRequest, db: Session):
    try:
        usuario = db.query(Usuario).filter(Usuario.login == dados.usuario).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")

        senha_no_banco = getattr(usuario, "senha_hash", None) or getattr(usuario, "senha", None)
        if senha_no_banco != dados.senha:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")

        return usuario
    except HTTPException as he:
        raise he
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")