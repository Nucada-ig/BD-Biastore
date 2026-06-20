from app.database import db
from app.models import Carrinho, ItemCarrinho


class CarrinhoDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Carrinho e ItemCarrinho.
    """

    @staticmethod
    def criar_para_usuario(usuario_id):
        """Cria um carrinho vazio para o usuário informado."""
        carrinho = Carrinho(usuario_id=usuario_id)
        db.session.add(carrinho)
        db.session.commit()
        return carrinho

    @staticmethod
    def buscar_por_usuario(usuario_id):
        """Retorna o carrinho do usuário, ou None se não existir."""
        return db.session.query(Carrinho).filter_by(usuario_id=usuario_id).first()

    @staticmethod
    def buscar_ou_criar(usuario_id):
        """Retorna o carrinho do usuário; cria um novo se ainda não existir."""
        carrinho = CarrinhoDAO.buscar_por_usuario(usuario_id)
        if carrinho is None:
            carrinho = CarrinhoDAO.criar_para_usuario(usuario_id)
        return carrinho

    @staticmethod
    def adicionar_item(carrinho_id, produto_id, quantidade=1):
        """
        Adiciona um produto ao carrinho. Se o produto já estiver no carrinho,
        apenas soma a quantidade ao item existente.
        """
        item = (
            db.session.query(ItemCarrinho)
            .filter_by(carrinho_id=carrinho_id, produto_id=produto_id)
            .first()
        )
        if item:
            item.quantidade += quantidade
        else:
            item = ItemCarrinho(
                carrinho_id=carrinho_id,
                produto_id=produto_id,
                quantidade=quantidade,
            )
            db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def atualizar_quantidade(item_id, quantidade):
        """Atualiza a quantidade de um item específico do carrinho."""
        item = db.session.get(ItemCarrinho, item_id)
        if item is None:
            return None
        item.quantidade = quantidade
        db.session.commit()
        return item

    @staticmethod
    def remover_item(item_id):
        """Remove um item do carrinho. Retorna True se removeu, False se não encontrou."""
        item = db.session.get(ItemCarrinho, item_id)
        if item is None:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    @staticmethod
    def limpar_carrinho(carrinho_id):
        """Remove todos os itens de um carrinho (usado após a finalização da compra)."""
        db.session.query(ItemCarrinho).filter_by(carrinho_id=carrinho_id).delete()
        db.session.commit()

    @staticmethod
    def calcular_total(carrinho_id):
        """Calcula o valor total dos itens presentes no carrinho."""
        carrinho = db.session.get(Carrinho, carrinho_id)
        if carrinho is None:
            return 0.0
        total = sum(item.quantidade * item.produto.preco for item in carrinho.itens)
        return total
