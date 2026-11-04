from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base declarativa ÚNICA do projeto.

    Equivalente ao seu DbContext no EF: TODOS os modelos (Usuario, Medico,
    Farmaceutico, Paciente, Prescricao, Protocolo, Frasco, OperacaoFracionamento)
    devem herdar desta mesma classe.

    Antes, o projeto tinha 3 classes "Base(DeclarativeBase)" diferentes
    (uma em polymorphic.py, uma em prescricao.py, uma em operacaofracionamento.py).
    Cada uma delas gera seu próprio metadata/registry internamente - é como se
    fossem 3 DbContexts diferentes que não se enxergam. Isso quebra os
    relationship() entre classes que "pertencem" a Bases diferentes.
    """
    pass