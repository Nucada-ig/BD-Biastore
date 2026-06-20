from app.database import db


class Usuario(db.Model):
    """
    Representa o cliente que compra na plataforma.
    Pode também ser vendedor, indicado pelo campo `is_vendedor`.
    """
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255), nullable=True)

    # Indica se este usuário também atua como vendedor
    is_vendedor = db.Column(db.Boolean, default=False, nullable=False)

    # Relação 1:1 -> cada usuário possui um único carrinho
    carrinho = db.relationship(
        "Carrinho",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um usuário pode ter vários pedidos
    pedidos = db.relationship(
        "Pedido",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um usuário (quando vendedor) pode ter vários produtos cadastrados
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
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "endereco": self.endereco,
            "is_vendedor": self.is_vendedor,
        }

    def __repr__(self):
        return f"<Usuario {self.id} - {self.nome}>"
