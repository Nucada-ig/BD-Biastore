from app.database import db
from app.models.endereco import Endereco
from app.models.codigo_postal import CodigoPostal


class EnderecoDAO:

    @staticmethod
    def listar_por_usuario(cpf):
        return (
            db.session.query(Endereco)
            .filter_by(cpf=cpf)
            .all()
        )

    @staticmethod
    def buscar(endereco_id):
        return db.session.get(Endereco, endereco_id)

    @staticmethod
    def criar(cpf, cep, numero, complemento, bairro, cidade, estado):
        # garante que o CEP existe na tabela de apoio
        codigo_postal = db.session.get(CodigoPostal, cep)
        if codigo_postal is None:
            codigo_postal = CodigoPostal(
                cep=cep, bairro=bairro, cidade=cidade, estado=estado
            )
            db.session.add(codigo_postal)

        endereco = Endereco(
            cpf=cpf,
            cep=cep,
            numero=numero,
            complemento=complemento or None,
        )
        db.session.add(endereco)
        db.session.commit()
        return endereco

    @staticmethod
    def remover(endereco_id, cpf):
        """Remove o endereço somente se pertencer ao cpf informado."""
        endereco = db.session.get(Endereco, endereco_id)
        if endereco is None or endereco.cpf != cpf:
            return False
        db.session.delete(endereco)
        db.session.commit()
        return True
