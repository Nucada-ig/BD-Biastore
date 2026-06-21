from sqlalchemy import text
from app.database import db
from app.models import Usuario


class UsuarioDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Usuario.
    A chave de identificação principal é o CPF.
    """

    @staticmethod
    def _proximo_id():
        """
        Gera o próximo valor para a coluna `id` (UNIQUE, mas não PK).

        No PostgreSQL usa a sequence usuario_id_seq diretamente.
        No SQLite (desenvolvimento local) usa MAX(id)+1 como fallback,
        já que SQLite não suporta sequences.
        """
        if db.engine.dialect.name == "postgresql":
            return db.session.execute(
                text("SELECT nextval('usuario_id_seq')")
            ).scalar()
        maior_id = db.session.query(db.func.max(Usuario.id)).scalar()
        return (maior_id or 0) + 1

    @staticmethod
    def criar(cpf, nome, email, senha):
        """Cria e persiste um novo usuário."""
        usuario = Usuario(
            cpf=cpf,
            id=UsuarioDAO._proximo_id(),
            nome=nome,
            email=email,
            senha=senha,
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def buscar_por_cpf(cpf):
        """Retorna um usuário pelo CPF, ou None se não existir."""
        return db.session.get(Usuario, cpf)

    @staticmethod
    def buscar_por_email(email):
        """Retorna um usuário pelo email (usado no login), ou None se não existir."""
        return db.session.query(Usuario).filter_by(email=email).first()

    @staticmethod
    def listar_todos():
        """Retorna todos os usuários cadastrados."""
        return db.session.query(Usuario).all()

    @staticmethod
    def atualizar(cpf, **dados):
        """
        Atualiza os campos informados em **dados para o usuário indicado.
        Exemplo: UsuarioDAO.atualizar('12345678900', nome="Novo Nome")
        """
        usuario = UsuarioDAO.buscar_por_cpf(cpf)
        if usuario is None:
            return None
        for campo, valor in dados.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        db.session.commit()
        return usuario

    @staticmethod
    def deletar(cpf):
        """Remove um usuário pelo CPF. Retorna True se removeu, False se não encontrou."""
        usuario = UsuarioDAO.buscar_por_cpf(cpf)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True
