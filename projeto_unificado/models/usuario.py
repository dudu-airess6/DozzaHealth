from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data.base import Base


class Usuario(Base):
    """
    Classe base da hierarquia TPH (Table Per Hierarchy).
    Equivalente ao .HasDiscriminator<string>("TipoUsuario") do EF.

    Todas as subclasses (Medico, Farmaceutico) ficam armazenadas nesta
    mesma tabela "usuarios", diferenciadas pela coluna tipo_usuario.
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(100))

    login: Mapped[str] = mapped_column(String(50), unique=True)

    senha_hash: Mapped[str] = mapped_column(String(255))

    # Coluna discriminadora (equivalente ao .HasValue<T>("...") do EF)
    tipo_usuario: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": "tipo_usuario",
        "polymorphic_identity": "usuario",
    }

    def login_sistema(self) -> None:
        # Lógica de login
        pass

    def logout_sistema(self) -> None:
        # Lógica de logout
        pass