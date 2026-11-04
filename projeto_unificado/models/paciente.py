from typing import List
from decimal import Decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.base import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    peso: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    prescricoes: Mapped[List["Prescricao"]] = relationship(back_populates="paciente")