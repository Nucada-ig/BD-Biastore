from app.database import db


class Vendedor(db.Model):
    """
    Representa o vendedor que cadastra e vende produtos na plataforma.

    É uma entidade totalmente separada de Usuario no banco relacional
    (sem CPF, sem FK em comum) - faz login com email/senha próprios.
    """
    __tablename__ = "vendedor"

    vendedor_id = db.Column(db.Integer, primary_key=True)
    nome_vendedor = db.Column(db.String(100), nullable=False)
    cnpj_vendedor = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)

    # Relação 1:N -> um vendedor pode ter vários telefones
    telefones = db.relationship(
        "TelefoneVendedor",
        back_populates="vendedor",
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um vendedor pode ter vários endereços cadastrados
    enderecos = db.relationship(
        "EnderecoVendedor",
        back_populates="vendedor",
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um vendedor pode ter vários produtos cadastrados
    produtos = db.relationship(
        "Produto",
        back_populates="vendedor",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """
        Converte o objeto em dict, útil para respostas JSON ou templates.
        Não inclui a senha por padrão.
        """
        return {
            "vendedor_id": self.vendedor_id,
            "nome_vendedor": self.nome_vendedor,
            "cnpj_vendedor": self.cnpj_vendedor,
            "email": self.email,
        }

    def __repr__(self):
        return f"<Vendedor {self.vendedor_id} - {self.nome_vendedor}>"
