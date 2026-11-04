from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.usuario import Usuario


class Farmaceutico(Usuario):
    """
    Subclasse TPH de Usuario.
    Assim como Medico, adiciona a coluna abaixo (crf) na mesma
    tabela "usuarios" - equivalente ao .HasValue<Farmaceutico>("Farmaceutico") do EF.
    """
    __mapper_args__ = {
        "polymorphic_identity": "Farmaceutico",
    }

    # nullable=True porque, na mesma tabela, médicos não têm CRF
    crf: Mapped[str] = mapped_column(String(20), nullable=True)

    # Relacionamentos One-to-Many (os back_populates precisam existir
    # do outro lado, em Protocolo e OperacaoFracionamento - próximo passo)
    protocolos_gerenciados: Mapped[List["Protocolo"]] = relationship(back_populates="farmaceutico")
    operacoes_aprovadas: Mapped[List["OperacaoFracionamento"]] = relationship(back_populates="farmaceutico")

    def selecionar_protocolo(self):
        # Lógica para selecionar protocolo
        pass

    def iniciar_fracionamento(self):
        # Lógica para iniciar fracionamento
        pass