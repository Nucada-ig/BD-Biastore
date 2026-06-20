from app.database import db


class Produto(db.Model):
    """
    Representa o produto cadastrado por um vendedor (Usuario com is_vendedor=True).
    """
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(255), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    # FK -> vendedor (Usuario) responsável pelo produto
    vendedor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    # Relação N:1 -> várias produtos pertencem a um único vendedor
    vendedor = db.relationship("Usuario", back_populates="produtos")

    # Relação N:N -> produto pode estar em vários carrinhos (via ItemCarrinho)
    itens_carrinho = db.relationship(
        "ItemCarrinho",
        back_populates="produto",
        cascade="all, delete-orphan"
    )

    # Relação N:N -> produto pode estar em vários pedidos (via ItemPedido)
    itens_pedido = db.relationship(
        "ItemPedido",
        back_populates="produto",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "imagem": self.imagem,
            "preco": self.preco,
            "descricao": self.descricao,
            "vendedor_id": self.vendedor_id,
        }

    def __repr__(self):
        return f"<Produto {self.id} - {self.nome}>"
