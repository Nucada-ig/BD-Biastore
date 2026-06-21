from app.database import db


class TelefoneCliente(db.Model):
    """
    Telefone de um usuário (cliente). Um usuário pode ter vários
    telefones; a chave primária é composta (cpf, telefone).
    """
    __tablename__ = "telefone_cliente"

    cpf = db.Column(db.String(11), db.ForeignKey("usuario.cpf"), primary_key=True)
    telefone = db.Column(db.String(20), primary_key=True)

    usuario = db.relationship("Usuario", back_populates="telefones")

    def to_dict(self):
        return {"cpf": self.cpf, "telefone": self.telefone}

    def __repr__(self):
        return f"<TelefoneCliente cpf={self.cpf} telefone={self.telefone}>"


class TelefoneVendedor(db.Model):
    """
    Telefone de um vendedor. Um vendedor pode ter vários telefones;
    a chave primária é composta (vendedor_id, telefone).
    """
    __tablename__ = "telefone_vendedor"

    vendedor_id = db.Column(db.Integer, db.ForeignKey("vendedor.vendedor_id"), primary_key=True)
    telefone = db.Column(db.String(20), primary_key=True)

    vendedor = db.relationship("Vendedor", back_populates="telefones")

    def to_dict(self):
        return {"vendedor_id": self.vendedor_id, "telefone": self.telefone}

    def __repr__(self):
        return f"<TelefoneVendedor vendedor_id={self.vendedor_id} telefone={self.telefone}>"
