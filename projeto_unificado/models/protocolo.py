from typing import List, Optional
from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.base import Base


class Protocolo(Base):
    __tablename__ = "protocolos"

    id: Mapped[int] = mapped_column(primary_key=True)

    medicamento: Mapped[str] = mapped_column(String(150), nullable=False)

    composicao: Mapped[str] = mapped_column(String(500), nullable=False)

    area_secao_transversal: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    quantidade_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    viscosidade: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    # Sem [Required] no C# original -> pode ser nulo
    tipo_valvula: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    taxa_gotejamento_padrao: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    # int? no C# -> Optional aqui. FK aponta para "usuarios.id" pois
    # Farmaceutico é TPH (fica na mesma tabela que Usuario/Medico)
    farmaceutico_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    farmaceutico: Mapped[Optional["Farmaceutico"]] = relationship(
        back_populates="protocolos_gerenciados"
    )

    frascos: Mapped[List["Frasco"]] = relationship(back_populates="protocolo")