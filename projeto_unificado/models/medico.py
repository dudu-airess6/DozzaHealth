from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.usuario import Usuario


class Medico(Usuario):
    """
    Subclasse TPH de Usuario.
    Como não declara __tablename__, o SQLAlchemy adiciona as colunas
    abaixo (crm, especialidade) na MESMA tabela "usuarios" (herança
    de tabela única) - equivalente ao .HasValue<Medico>("Medico") do EF.
    """
    __mapper_args__ = {
        "polymorphic_identity": "Medico",
    }

    # nullable=True porque, na mesma tabela, farmacêuticos não têm CRM
    crm: Mapped[str] = mapped_column(String(20), nullable=True)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relacionamento One-to-Many (o back_populates="medico" precisa
    # existir do outro lado, em Prescricao - ver próximo passo do plano)
    prescricoes: Mapped[List["Prescricao"]] = relationship(back_populates="medico")

    def prescrever(self):
        # Lógica de prescrição
        pass