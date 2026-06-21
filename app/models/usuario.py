from app.database import db


class Usuario(db.Model):
    """
    Representa o cliente que compra na plataforma.

    A chave primária é o CPF (conforme o banco relacional já existente),
    e não um id autoincrement - 'id' existe na tabela apenas como coluna
    auxiliar com restrição UNIQUE, herdada do schema original.

    Vendedores são uma entidade totalmente separada (ver Vendedor),
    sem nenhuma ligação direta com Usuario no banco.
    """
    __tablename__ = "usuario"

    cpf = db.Column(db.String(11), primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    # Relação 1:N -> um usuário pode ter vários telefones
    telefones = db.relationship(
        "TelefoneCliente",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um usuário pode ter vários endereços cadastrados
    enderecos = db.relationship(
        "Endereco",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    # Relação 1:N -> um usuário pode ter vários pedidos (inclui o
    # "carrinho atual", que é um Pedido com status PROCESSANDO)
    pedidos = db.relationship(
        "Pedido",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """
        Converte o objeto em dict, útil para respostas JSON ou templates.
        Não inclui a senha por padrão.
        """
        return {
            "cpf": self.cpf,
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
        }

    def __repr__(self):
        return f"<Usuario {self.cpf} - {self.nome}>"
