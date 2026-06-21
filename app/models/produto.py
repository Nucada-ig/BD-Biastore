from app.database import db


class Produto(db.Model):
    """
    Representa o produto cadastrado por um Vendedor.
    """
    __tablename__ = "produto"

    produto_id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    imagem = db.Column(db.String(500), nullable=True)

    descricao = db.Column(db.Text, nullable=True)
    material = db.Column(db.String(200), nullable=True)
    peso = db.Column(db.String(50), nullable=True)
    dimensoes = db.Column(db.String(100), nullable=True)
    prazo_entrega = db.Column(db.Integer, nullable=True)
    politica_troca = db.Column(db.Text, nullable=True)

    # FK -> vendedor responsável pelo produto
    vendedor_id = db.Column(db.Integer, db.ForeignKey("vendedor.vendedor_id"), nullable=True)

    # Relação N:1 -> vários produtos pertencem a um único vendedor
    vendedor = db.relationship("Vendedor", back_populates="produtos")

    # Relação 1:N -> produto pode estar em vários itens de pedido
    itens_pedido = db.relationship(
        "ItemPedido",
        back_populates="produto",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "nome_produto": self.nome_produto,
            "categoria": self.categoria,
            "preco_unitario": float(self.preco_unitario) if self.preco_unitario is not None else None,
            "estoque": self.estoque,
            "imagem": self.imagem,
            "vendedor_id": self.vendedor_id,
            "descricao": self.descricao,
            "material": self.material,
            "peso": self.peso,
            "dimensoes": self.dimensoes,
            "prazo_entrega": self.prazo_entrega,
            "politica_troca": self.politica_troca,
        }

    def __repr__(self):
        return f"<Produto {self.produto_id} - {self.nome_produto}>"