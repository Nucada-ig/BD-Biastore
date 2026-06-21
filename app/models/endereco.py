from app.database import db


class Endereco(db.Model):
    """
    Endereço cadastrado por um usuário (cliente). Um usuário pode ter
    vários endereços; cada Envio referencia um deles como endereço
    de entrega.
    """
    __tablename__ = "enderecos"

    endereco_id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey("usuario.cpf"), nullable=False)
    cep = db.Column(db.String(8), db.ForeignKey("codigo_postal.cep"), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100), nullable=True)

    usuario = db.relationship("Usuario", back_populates="enderecos")
    codigo_postal = db.relationship("CodigoPostal")
    envios = db.relationship("Envio", back_populates="endereco")

    def to_dict(self):
        return {
            "endereco_id": self.endereco_id,
            "cpf": self.cpf,
            "cep": self.cep,
            "numero": self.numero,
            "complemento": self.complemento,
        }

    def __repr__(self):
        return f"<Endereco {self.endereco_id} - cpf {self.cpf}>"


class EnderecoVendedor(db.Model):
    """
    Endereço cadastrado por um vendedor. Um vendedor pode ter vários
    endereços (ex: múltiplas unidades/centros de distribuição).
    """
    __tablename__ = "endereco_vendedor"

    endereco_id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey("vendedor.vendedor_id"), nullable=False)
    cep = db.Column(db.String(8), db.ForeignKey("codigo_postal.cep"), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100), nullable=True)

    vendedor = db.relationship("Vendedor", back_populates="enderecos")
    codigo_postal = db.relationship("CodigoPostal")

    def to_dict(self):
        return {
            "endereco_id": self.endereco_id,
            "vendedor_id": self.vendedor_id,
            "cep": self.cep,
            "numero": self.numero,
            "complemento": self.complemento,
        }

    def __repr__(self):
        return f"<EnderecoVendedor {self.endereco_id} - vendedor {self.vendedor_id}>"
