from datetime import datetime
from app.database import db


# Valores possíveis para status_pedido, conforme a CHECK constraint do banco.
# O carrinho de compras é representado como um Pedido com status PROCESSANDO,
# que ainda não foi finalizado - ver app/dao/pedido_dao.py.
STATUS_PROCESSANDO = "PROCESSANDO"
STATUS_PAGO = "PAGO"
STATUS_ENVIADO = "ENVIADO"
STATUS_ENTREGUE = "ENTREGUE"
STATUS_CANCELADO = "CANCELADO"


class Pedido(db.Model):
    """
    Representa um pedido do usuário.

    Importante: como o banco relacional não possui uma tabela própria de
    carrinho, o "carrinho de compras" é modelado como um Pedido com
    status PROCESSANDO. Quando o usuário finaliza a compra, o status é
    avançado para PAGO (e depois ENVIADO/ENTREGUE conforme o fluxo).
    Cada usuário deve ter no máximo um pedido em PROCESSANDO por vez,
    que funciona como o "carrinho atual" dele.
    """
    __tablename__ = "pedido"

    pedido_id = db.Column(db.Integer, primary_key=True)
    status_pedido = db.Column(db.String(50), nullable=False, default=STATUS_PROCESSANDO)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    # FK -> usuário que fez o pedido
    cpf = db.Column(db.String(11), db.ForeignKey("usuario.cpf"), nullable=True)

    # Relação N:1 -> vários pedidos pertencem a um único usuário
    usuario = db.relationship("Usuario", back_populates="pedidos")

    # Relação 1:N -> pedido possui vários itens (cada item referencia um produto)
    itens = db.relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

    # Relação 1:1 -> pedido pode ter um registro de pagamento
    pagamento = db.relationship(
        "Pagamento",
        back_populates="pedido",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Relação 1:1 -> pedido pode ter um registro de envio
    envio = db.relationship(
        "Envio",
        back_populates="pedido",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "pedido_id": self.pedido_id,
            "status_pedido": self.status_pedido,
            "data_pedido": self.data_pedido.isoformat() if self.data_pedido else None,
            "total": float(self.total) if self.total is not None else None,
            "cpf": self.cpf,
            "itens": [item.to_dict() for item in self.itens],
        }

    def __repr__(self):
        return f"<Pedido {self.pedido_id} - cpf {self.cpf} - status {self.status_pedido}>"


class ItemPedido(db.Model):
    """
    Item de um pedido (linha de produto dentro do pedido).
    Chave primária composta (produto_id, pedido_id), conforme o banco.
    """
    __tablename__ = "item_pedido"

    produto_id = db.Column(db.Integer, db.ForeignKey("produto.produto_id"), primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.pedido_id"), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_historico = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens_pedido")

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "pedido_id": self.pedido_id,
            "quantidade": self.quantidade,
            "preco_historico": float(self.preco_historico) if self.preco_historico is not None else None,
        }

    def __repr__(self):
        return f"<ItemPedido pedido={self.pedido_id} produto={self.produto_id} qtd={self.quantidade}>"
