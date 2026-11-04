from typing import List, Optional
from models.farmaceutico import OperacaoFracionamento
from models.frasco import Frasco
from sqlalchemy import String, ForeignKey, create_engine # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session # pyright: ignore[reportMissingImports]

class Base(DeclarativeBase):
    pass
 
# ==========================================
# HERANÇA TPH (Table Per Hierarchy)
# ==========================================
class Usuario(Base):
    __tablename__ = "usuarios" # Todas as subclasses ficarão nesta tabela

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    # ... outros campos (login, senha_hash) omitidos para brevidade ...

    # O equivalente ao .HasDiscriminator<string>("TipoUsuario")
    tipo_usuario: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": "tipo_usuario",
        "polymorphic_identity": "usuario" # Valor padrão se não for instanciado como Medico ou Farmaceutico
    }

class Medico(Usuario):
    # O equivalente ao .HasValue<Medico>("Medico")
    __mapper_args__ = {
        "polymorphic_identity": "Medico"
    }

    # Relacionamento One-to-Many
    prescricoes: Mapped[List["Prescricao"]] = relationship(back_populates="medico")

class Farmaceutico(Usuario):
    # O equivalente ao .HasValue<Farmaceutico>("Farmaceutico")
    __mapper_args__ = {
        "polymorphic_identity": "Farmaceutico"
    }

    # Relacionamentos One-to-Many
    protocolos_gerenciados: Mapped[List["Protocolo"]] = relationship(back_populates="farmaceutico")
    operacoes_aprovadas: Mapped[List["OperacaoFracionamento"]] = relationship(back_populates="farmaceutico")

# ==========================================
# CONFIGURAÇÃO DE DELETE BEHAVIOR (RESTRICT / SET NULL)
# ==========================================
class Prescricao(Base):
    __tablename__ = "prescricoes"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # DeleteBehavior.Restrict -> ondelete="RESTRICT"
    # Como Medico é TPH, a ForeignKey aponta para a tabela base "usuarios.id"
    medico_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    medico: Mapped["Medico"] = relationship(back_populates="prescricoes")
    
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT"))
    
    # ... resto da classe ...

class Protocolo(Base):
    __tablename__ = "protocolos"
    id: Mapped[int] = mapped_column(primary_key=True)

    # DeleteBehavior.SetNull -> ondelete="SET NULL" + nullable=True
    farmaceutico_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    farmaceutico: Mapped[Optional["Farmaceutico"]] = relationship(back_populates="protocolos_gerenciados")

    frascos: Mapped[List["Frasco"]] = relationship(back_populates="protocolo")
    # ... resto da classe ...