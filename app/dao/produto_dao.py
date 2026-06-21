from app.database import db
from app.models import Produto


class ProdutoDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Produto.
    """

    @staticmethod
    def criar(nome_produto, categoria, preco_unitario, vendedor_id, estoque=0, imagem=None,
              descricao=None, material=None, peso=None, dimensoes=None,
              prazo_entrega=None, politica_troca=None):
        """Cria e persiste um novo produto."""
        produto = Produto(
            nome_produto=nome_produto,
            categoria=categoria,
            preco_unitario=preco_unitario,
            vendedor_id=vendedor_id,
            estoque=estoque,
            imagem=imagem,
            descricao=descricao,
            material=material,
            peso=peso,
            dimensoes=dimensoes,
            prazo_entrega=prazo_entrega,
            politica_troca=politica_troca,
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
    def listar_paginado(pagina: int = 1, por_pagina: int = 8):
        """Retorna uma página de produtos e o total de registros."""
        q = db.session.query(Produto)
        total = q.count()
        produtos = q.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return produtos, total

    @staticmethod
    def listar_por_vendedor(vendedor_id):
        """Retorna os produtos cadastrados por um vendedor específico."""
        return db.session.query(Produto).filter_by(vendedor_id=vendedor_id).all()

    @staticmethod
    def listar_por_categoria(categoria, limite=None):
        """Retorna os produtos de uma categoria específica."""
        q = db.session.query(Produto).filter_by(categoria=categoria)
        if limite:
            q = q.limit(limite)
        return q.all()

    @staticmethod
    def listar_mix_categorias(categorias: list, limite_por_categoria: int = 5) -> list:
        """
        Retorna produtos de várias categorias embaralhados.
        Busca até `limite_por_categoria` itens de cada categoria em ordem
        aleatória e depois mistura tudo antes de retornar.
        """
        if not categorias:
            return []
        import random
        from sqlalchemy import func
        resultado = []
        for cat in categorias:
            produtos = (
                db.session.query(Produto)
                .filter_by(categoria=cat)
                .order_by(func.random())
                .limit(limite_por_categoria)
                .all()
            )
            resultado.extend(produtos)
        random.shuffle(resultado)
        return resultado

    @staticmethod
    def buscar_por_nome(termo):
        """
        Busca produtos cujo nome contenha o termo informado (case-insensitive).
        Usado na rota de pesquisa/catálogo.
        """
        return (
            db.session.query(Produto)
            .filter(Produto.nome_produto.ilike(f"%{termo}%"))
            .all()
        )

    @staticmethod
    def listar_categorias() -> list:
        """Retorna as categorias distintas que têm ao menos um produto, ordenadas."""
        rows = (
            db.session.query(Produto.categoria)
            .distinct()
            .order_by(Produto.categoria)
            .all()
        )
        return [r[0] for r in rows]

    @staticmethod
    def atualizar(produto_id, **dados):
        """
        Atualiza os campos informados em **dados para o produto indicado.
        Exemplo: ProdutoDAO.atualizar(1, preco_unitario=59.9, estoque=10)
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