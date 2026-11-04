from pydantic import BaseModel
from typing import List, Any, Optional

class MedicamentoSchema(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    forma: Optional[str] = None
    concentracao: Optional[str] = None

class RespostaBuscaSchema(BaseModel):
    total_encontrados: int
    pagina: int
    limite: int
    resultados: List[Any]