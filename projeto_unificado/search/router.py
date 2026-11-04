from fastapi import APIRouter, Depends, Query
from typing import Optional
from search.auth import verificar_acesso_farmaceutico
from .services import busca_service
from .schemas import RespostaBuscaSchema

router = APIRouter(prefix="/api/v1", tags=["Busca de Prescrições"])

@router.get(
    "/buscar", 
    response_model=RespostaBuscaSchema,
    summary="Busca de medicamentos líquidos (Acesso exclusivo para Farmacêuticos)"
)
def buscar_medicamentos(
    q: Optional[str] = Query(None, description="Termo de busca"),
    forma: Optional[str] = Query(None, description="Filtro por forma farmacêutica"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    usuario_logado: dict = Depends(verificar_acesso_farmaceutico)
):
    return busca_service.buscar(q=q, forma=forma, page=page, limit=limit)