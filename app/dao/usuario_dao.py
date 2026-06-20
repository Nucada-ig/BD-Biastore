from app.database import db
from app.models import Usuario


class UsuarioDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Usuario.
    """

    @staticmethod
    def criar(nome, email, senha, endereco=None, is_vendedor=False):
        """Cria e persiste um novo usuário."""
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            endereco=endereco,
            is_vendedor=is_vendedor,
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def buscar_por_id(usuario_id):
        """Retorna um usuário pelo id, ou None se não existir."""
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def buscar_por_email(email):
        """Retorna um usuário pelo email (usado no login), ou None se não existir."""
        return db.session.query(Usuario).filter_by(email=email).first()

    @staticmethod
    def listar_todos():
        """Retorna todos os usuários cadastrados."""
        return db.session.query(Usuario).all()

    @staticmethod
    def listar_vendedores():
        """Retorna apenas os usuários que são vendedores."""
        return db.session.query(Usuario).filter_by(is_vendedor=True).all()

    @staticmethod
    def atualizar(usuario_id, **dados):
        """
        Atualiza os campos informados em **dados para o usuário indicado.
        Exemplo: UsuarioDAO.atualizar(1, nome="Novo Nome", endereco="Rua X")
        """
        usuario = UsuarioDAO.buscar_por_id(usuario_id)
        if usuario is None:
            return None
        for campo, valor in dados.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        db.session.commit()
        return usuario

    @staticmethod
    def deletar(usuario_id):
        """Remove um usuário pelo id. Retorna True se removeu, False se não encontrou."""
        usuario = UsuarioDAO.buscar_por_id(usuario_id)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True
