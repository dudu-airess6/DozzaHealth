from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.base import Base


class Prescricao(Base):
    __tablename__ = "prescricoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    dosagem: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("pacientes.id", ondelete="RESTRICT"), nullable=False
    )
    # back_populates precisa existir do lado de Paciente também
    # (Paciente ainda está como Pydantic - ver observação abaixo)
    paciente: Mapped["Paciente"] = relationship(back_populates="prescricoes")

    # CORRIGIDO: como Medico é TPH (fica na tabela "usuarios", não "medicos"),
    # a FK precisa apontar para "usuarios.id"
    medico_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False
    )
    medico: Mapped["Medico"] = relationship(back_populates="prescricoes")

    medicamento_nome: Mapped[str] = mapped_column(String(150), nullable=False)

    data_prescricao: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="Pendente", nullable=False)