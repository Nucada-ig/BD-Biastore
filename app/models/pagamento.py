from app.database import db


# Valores possíveis, conforme as CHECK constraints do banco.
METODO_CARTAO_CREDITO = "CARTAO_CREDITO"
METODO_BOLETO = "BOLETO"
METODO_PIX = "PIX"
METODO_TRANSFERENCIA = "TRANSFERENCIA"

STATUS_PENDENTE = "PENDENTE"
STATUS_APROVADO = "APROVADO"
STATUS_RECUSADO = "RECUSADO"
STATUS_ESTORNADO = "ESTORNADO"


class Pagamento(db.Model):
    """
    Dados de pagamento de um pedido. Relação 1:1 com Pedido
    (pedido_id é ao mesmo tempo PK e FK).
    """
    __tablename__ = "pagamento"

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.pedido_id"), primary_key=True)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    status_pagamento = db.Column(db.String(50), nullable=False, default=STATUS_PENDENTE)

    pedido = db.relationship("Pedido", back_populates="pagamento")

    def to_dict(self):
        return {
            "pedido_id": self.pedido_id,
            "metodo_pagamento": self.metodo_pagamento,
            "status_pagamento": self.status_pagamento,
        }

    def __repr__(self):
        return f"<Pagamento pedido={self.pedido_id} status={self.status_pagamento}>"
