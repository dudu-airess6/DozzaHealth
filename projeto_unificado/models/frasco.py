from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.base import Base


class Frasco(Base):
    __tablename__ = "frascos"

    id: Mapped[int] = mapped_column(primary_key=True)

    # nullable=False já garante no banco que o campo é obrigatório
    # (equivalente ao [Required] / ao "if volume_atual is None: raise" que
    # existia no __init__ da versão em classe pura)
    volume_atual: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    status: Mapped[str] = mapped_column(String(50), nullable=False)

    data_validade: Mapped[datetime] = mapped_column(nullable=False)

    localizacao_estoque: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    protocolo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("protocolos.id"), nullable=True
    )
    protocolo: Mapped[Optional["Protocolo"]] = relationship(back_populates="frascos")

    def get_quantidade_restante(self) -> Decimal:
        return self.volume_atual