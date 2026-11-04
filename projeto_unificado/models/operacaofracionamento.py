from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.base import Base


class OperacaoFracionamento(Base):
    __tablename__ = "operacoes_fracionamento"

    id: Mapped[int] = mapped_column(primary_key=True)

    prescricao_id: Mapped[int] = mapped_column(ForeignKey("prescricoes.id"), nullable=False)
    prescricao: Mapped["Prescricao"] = relationship()

    # CORRIGIDO: a tabela "farmaceuticos" nunca existiu (bug original).
    # Como Farmaceutico é TPH, a FK correta aponta para "usuarios.id"
    farmaceutico_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    farmaceutico: Mapped["Farmaceutico"] = relationship(back_populates="operacoes_aprovadas")

    frasco_original_id: Mapped[int] = mapped_column(ForeignKey("frascos.id"), nullable=False)
    frasco_original: Mapped["Frasco"] = relationship()

    volume_extraido: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    data_hora_inicio: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)

    data_hora_fim: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(String(50), nullable=False)

    relatorio_detalhes: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    id_interno_mes: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)