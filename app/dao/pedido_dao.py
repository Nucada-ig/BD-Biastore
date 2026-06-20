from app.database import db
from app.models import Pedido, ItemPedido, Carrinho


class PedidoDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Pedido e ItemPedido.
    """

    @staticmethod
    def buscar_por_id(pedido_id):
        """Retorna um pedido pelo id, ou None se não existir."""
        return db.session.get(Pedido, pedido_id)

    @staticmethod
    def listar_por_usuario(usuario_id):
        """Retorna todos os pedidos de um usuário (usado na tela de Pedido/perfil)."""
        return (
            db.session.query(Pedido)
            .filter_by(usuario_id=usuario_id)
            .order_by(Pedido.data.desc())
            .all()
        )

    @staticmethod
    def criar_a_partir_do_carrinho(carrinho_id, usuario_id):
        """
        Cria um novo Pedido a partir dos itens de um Carrinho (rota de Finalização).
        Copia cada item do carrinho para o pedido, guardando o preço unitário
        no momento da compra, e em seguida esvazia o carrinho.
        """
        carrinho = db.session.get(Carrinho, carrinho_id)
        if carrinho is None or not carrinho.itens:
            return None

        valor_total = sum(item.quantidade * item.produto.preco for item in carrinho.itens)

        pedido = Pedido(
            usuario_id=usuario_id,
            valor_total=valor_total,
            status="processando",
        )
        db.session.add(pedido)
        db.session.flush()  # garante que pedido.id já está disponível

        for item in carrinho.itens:
            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco,
            )
            db.session.add(item_pedido)

        # Esvazia o carrinho, já que os itens foram transformados em pedido
        for item in list(carrinho.itens):
            db.session.delete(item)

        db.session.commit()
        return pedido

    @staticmethod
    def atualizar_status(pedido_id, status):
        """Atualiza o status do pedido (ex: 'processando', 'a caminho', 'entregue')."""
        pedido = PedidoDAO.buscar_por_id(pedido_id)
        if pedido is None:
            return None
        pedido.status = status
        db.session.commit()
        return pedido
