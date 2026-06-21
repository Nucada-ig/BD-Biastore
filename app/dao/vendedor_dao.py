from app.database import db
from app.models import Vendedor


class VendedorDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Vendedor.
    """

    @staticmethod
    def criar(nome_vendedor, cnpj_vendedor, email, senha):
        """Cria e persiste um novo vendedor."""
        vendedor = Vendedor(
            nome_vendedor=nome_vendedor,
            cnpj_vendedor=cnpj_vendedor,
            email=email,
            senha=senha,
        )
        db.session.add(vendedor)
        db.session.commit()
        return vendedor

    @staticmethod
    def buscar_por_id(vendedor_id):
        """Retorna um vendedor pelo id, ou None se não existir."""
        return db.session.get(Vendedor, vendedor_id)

    @staticmethod
    def buscar_por_email(email):
        """Retorna um vendedor pelo email (usado no login), ou None se não existir."""
        return db.session.query(Vendedor).filter_by(email=email).first()

    @staticmethod
    def listar_todos():
        """Retorna todos os vendedores cadastrados."""
        return db.session.query(Vendedor).all()

    @staticmethod
    def atualizar(vendedor_id, **dados):
        """
        Atualiza os campos informados em **dados para o vendedor indicado.
        """
        vendedor = VendedorDAO.buscar_por_id(vendedor_id)
        if vendedor is None:
            return None
        for campo, valor in dados.items():
            if hasattr(vendedor, campo):
                setattr(vendedor, campo, valor)
        db.session.commit()
        return vendedor

    @staticmethod
    def deletar(vendedor_id):
        """Remove um vendedor pelo id. Retorna True se removeu, False se não encontrou."""
        vendedor = VendedorDAO.buscar_por_id(vendedor_id)
        if vendedor is None:
            return False
        db.session.delete(vendedor)
        db.session.commit()
        return True
