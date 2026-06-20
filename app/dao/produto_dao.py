from app.database import db
from app.models import Produto


class ProdutoDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Produto.
    """

    @staticmethod
    def criar(nome, preco, vendedor_id, imagem=None, descricao=None):
        """Cria e persiste um novo produto."""
        produto = Produto(
            nome=nome,
            preco=preco,
            vendedor_id=vendedor_id,
            imagem=imagem,
            descricao=descricao,
        )
        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def buscar_por_id(produto_id):
        """Retorna um produto pelo id, ou None se não existir."""
        return db.session.get(Produto, produto_id)

    @staticmethod
    def listar_todos():
        """Retorna todos os produtos cadastrados (usado no catálogo geral)."""
        return db.session.query(Produto).all()

    @staticmethod
    def listar_por_vendedor(vendedor_id):
        """Retorna os produtos cadastrados por um vendedor específico."""
        return db.session.query(Produto).filter_by(vendedor_id=vendedor_id).all()

    @staticmethod
    def buscar_por_nome(termo):
        """
        Busca produtos cujo nome contenha o termo informado (case-insensitive).
        Usado na rota de pesquisa/catálogo.
        """
        return (
            db.session.query(Produto)
            .filter(Produto.nome.ilike(f"%{termo}%"))
            .all()
        )

    @staticmethod
    def atualizar(produto_id, **dados):
        """
        Atualiza os campos informados em **dados para o produto indicado.
        Exemplo: ProdutoDAO.atualizar(1, preco=59.9, descricao="Nova descricao")
        """
        produto = ProdutoDAO.buscar_por_id(produto_id)
        if produto is None:
            return None
        for campo, valor in dados.items():
            if hasattr(produto, campo):
                setattr(produto, campo, valor)
        db.session.commit()
        return produto

    @staticmethod
    def deletar(produto_id):
        """Remove um produto pelo id. Retorna True se removeu, False se não encontrou."""
        produto = ProdutoDAO.buscar_por_id(produto_id)
        if produto is None:
            return False
        db.session.delete(produto)
        db.session.commit()
        return True
