from datetime import datetime
from app.database import db


class Pedido(db.Model):
    """
    Representa uma compra finalizada pelo usuário.
    Relação N:1 com Usuario e N:N com Produto (via ItemPedido).
    """
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default="processando")
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

    # FK -> usuário que realizou o pedido
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    # Relação N:1 -> vários pedidos pertencem a um único usuário
    usuario = db.relationship("Usuario", back_populates="pedidos")

    # Relação 1:N -> pedido possui vários itens (cada item referencia um produto)
    itens = db.relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data.isoformat() if self.data else None,
            "status": self.status,
            "valor_total": self.valor_total,
            "usuario_id": self.usuario_id,
            "itens": [item.to_dict() for item in self.itens],
        }

    def __repr__(self):
        return f"<Pedido {self.id} - usuario {self.usuario_id} - status {self.status}>"


class ItemPedido(db.Model):
    """
    Tabela associativa entre Pedido e Produto.
    Guarda também a quantidade e o preço unitário no momento da compra,
    preservando o histórico mesmo que o preço do produto mude depois.
    """
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens_pedido")

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
        }

    def __repr__(self):
        return f"<ItemPedido pedido={self.pedido_id} produto={self.produto_id} qtd={self.quantidade}>"
