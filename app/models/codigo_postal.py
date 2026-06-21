from app.database import db


class CodigoPostal(db.Model):
    """
    Tabela de apoio com dados de CEP (bairro, cidade, estado),
    compartilhada entre endereços de usuário e de vendedor.
    """
    __tablename__ = "codigo_postal"

    cep = db.Column(db.String(8), primary_key=True)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)

    def to_dict(self):
        return {
            "cep": self.cep,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
        }

    def __repr__(self):
        return f"<CodigoPostal {self.cep} - {self.cidade}/{self.estado}>"
