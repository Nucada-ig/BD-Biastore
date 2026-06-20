from app.database import db


class Carrinho(db.Model):
    """
    Representa o carrinho de compras de um usuário.
    Relação 1:1 com Usuario e N:N com Produto (via ItemCarrinho).
    """
    __tablename__ = "carrinho"

    id = db.Column(db.Integer, primary_key=True)

    # FK -> usuário dono do carrinho
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True)

    # Relação 1:1 -> carrinho pertence a um único usuário
    usuario = db.relationship("Usuario", back_populates="carrinho")

    # Relação 1:N -> carrinho possui vários itens (cada item referencia um produto)
    itens = db.relationship(
        "ItemCarrinho",
        back_populates="carrinho",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "itens": [item.to_dict() for item in self.itens],
        }

    def __repr__(self):
        return f"<Carrinho {self.id} - usuario {self.usuario_id}>"


class ItemCarrinho(db.Model):
    """
    Tabela associativa entre Carrinho e Produto.
    Permite que um produto apareça em vários carrinhos e um carrinho
    tenha vários produtos, guardando também a quantidade.
    """
    __tablename__ = "item_carrinho"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    carrinho_id = db.Column(db.Integer, db.ForeignKey("carrinho.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)

    carrinho = db.relationship("Carrinho", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens_carrinho")

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
        }

    def __repr__(self):
        return f"<ItemCarrinho carrinho={self.carrinho_id} produto={self.produto_id} qtd={self.quantidade}>"
