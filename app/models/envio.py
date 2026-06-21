from app.database import db


class Envio(db.Model):
    """
    Dados de envio/entrega de um pedido. Relação 1:1 com Pedido
    (pedido_id é ao mesmo tempo PK e FK).

    O endereço de entrega referencia um endereço já cadastrado do
    usuário (tabela Endereco), em vez de armazenar o endereço como
    texto livre.
    """
    __tablename__ = "envio"

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.pedido_id"), primary_key=True)
    status_envio = db.Column(db.String(50), nullable=False)
    transportadora = db.Column(db.String(100), nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=False)
    codigo_rastreamento = db.Column(db.String(100), nullable=False)

    # FK -> endereço de entrega (já cadastrado pelo usuário)
    endereco_id = db.Column(db.Integer, db.ForeignKey("enderecos.endereco_id"), nullable=False)

    pedido = db.relationship("Pedido", back_populates="envio")
    endereco = db.relationship("Endereco", back_populates="envios")

    def to_dict(self):
        return {
            "pedido_id": self.pedido_id,
            "status_envio": self.status_envio,
            "transportadora": self.transportadora,
            "data_entrega": self.data_entrega.isoformat() if self.data_entrega else None,
            "codigo_rastreamento": self.codigo_rastreamento,
            "endereco_id": self.endereco_id,
        }

    def __repr__(self):
        return f"<Envio pedido={self.pedido_id} status={self.status_envio}>"
