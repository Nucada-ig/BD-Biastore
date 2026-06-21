from app.database import db
from app.models import Pedido, ItemPedido, Produto, Pagamento
from app.models.pedido import STATUS_PROCESSANDO, STATUS_PAGO
from app.models.pagamento import STATUS_APROVADO


class PedidoDAO:
    """
    Encapsula as operações de banco de dados relacionadas a Pedido e
    ItemPedido.

    Importante: como o banco relacional não possui uma tabela própria
    de carrinho, o "carrinho de compras" é representado aqui como um
    Pedido com status_pedido = PROCESSANDO. As funções
    buscar_ou_criar_carrinho / adicionar_item / remover_item /
    calcular_total operam sobre esse pedido em aberto. Quando o usuário
    finaliza a compra, finalizar_pedido() avança o status para PAGO.

    Cada usuário deve ter no máximo 1 pedido em PROCESSANDO por vez.
    """

    # ----------------------------------------------------------------
    # Consultas gerais de pedido
    # ----------------------------------------------------------------

    @staticmethod
    def buscar_por_id(pedido_id):
        """Retorna um pedido pelo id, ou None se não existir."""
        return db.session.get(Pedido, pedido_id)

    @staticmethod
    def listar_por_usuario(cpf):
        """
        Retorna os pedidos finalizados de um usuário (ou seja, todo
        pedido que NÃO está mais em PROCESSANDO), do mais recente
        para o mais antigo. Usado na tela de "Meus pedidos".
        """
        return (
            db.session.query(Pedido)
            .filter(Pedido.cpf == cpf, Pedido.status_pedido != STATUS_PROCESSANDO)
            .order_by(Pedido.data_pedido.desc())
            .all()
        )

    @staticmethod
    def atualizar_status(pedido_id, status):
        """Atualiza o status do pedido (ex: PAGO, ENVIADO, ENTREGUE)."""
        pedido = PedidoDAO.buscar_por_id(pedido_id)
        if pedido is None:
            return None
        pedido.status_pedido = status
        db.session.commit()
        return pedido

    # ----------------------------------------------------------------
    # "Carrinho" = Pedido com status PROCESSANDO
    # ----------------------------------------------------------------

    @staticmethod
    def buscar_carrinho(cpf):
        """
        Retorna o pedido em PROCESSANDO do usuário (o "carrinho atual"),
        ou None se ele não tiver nenhum carrinho em aberto.
        """
        return (
            db.session.query(Pedido)
            .filter_by(cpf=cpf, status_pedido=STATUS_PROCESSANDO)
            .first()
        )

    @staticmethod
    def buscar_ou_criar_carrinho(cpf):
        """
        Retorna o carrinho (pedido PROCESSANDO) do usuário; cria um
        novo, vazio, se ele ainda não tiver nenhum em aberto.
        """
        carrinho = PedidoDAO.buscar_carrinho(cpf)
        if carrinho is None:
            carrinho = Pedido(cpf=cpf, status_pedido=STATUS_PROCESSANDO, total=0)
            db.session.add(carrinho)
            db.session.commit()
        return carrinho

    @staticmethod
    def adicionar_item(pedido_id, produto_id, quantidade=1):
        """
        Adiciona um produto ao carrinho (pedido em PROCESSANDO). Se o
        produto já estiver no carrinho, soma a quantidade ao item
        existente. Também atualiza o campo `total` do pedido.
        """
        item = db.session.get(ItemPedido, (produto_id, pedido_id))
        produto = db.session.get(Produto, produto_id)
        if produto is None:
            return None

        if item:
            item.quantidade += quantidade
        else:
            item = ItemPedido(
                pedido_id=pedido_id,
                produto_id=produto_id,
                quantidade=quantidade,
                preco_historico=produto.preco_unitario,
            )
            db.session.add(item)

        db.session.flush()
        PedidoDAO._recalcular_total(pedido_id)
        db.session.commit()
        return item

    @staticmethod
    def atualizar_quantidade(pedido_id, produto_id, quantidade):
        """Atualiza a quantidade de um item específico do carrinho."""
        item = db.session.get(ItemPedido, (produto_id, pedido_id))
        if item is None:
            return None
        item.quantidade = quantidade
        db.session.flush()
        PedidoDAO._recalcular_total(pedido_id)
        db.session.commit()
        return item

    @staticmethod
    def remover_item(pedido_id, produto_id):
        """Remove um item do carrinho. Retorna True se removeu, False se não encontrou."""
        item = db.session.get(ItemPedido, (produto_id, pedido_id))
        if item is None:
            return False
        db.session.delete(item)
        db.session.flush()
        PedidoDAO._recalcular_total(pedido_id)
        db.session.commit()
        return True

    @staticmethod
    def calcular_total(pedido_id):
        """Calcula o valor total dos itens presentes no carrinho/pedido."""
        pedido = db.session.get(Pedido, pedido_id)
        if pedido is None:
            return 0
        return sum(item.quantidade * item.preco_historico for item in pedido.itens)

    @staticmethod
    def _recalcular_total(pedido_id):
        """Recalcula e grava o campo `total` do pedido, a partir dos itens atuais."""
        pedido = db.session.get(Pedido, pedido_id)
        if pedido is not None:
            pedido.total = PedidoDAO.calcular_total(pedido_id)

    # ----------------------------------------------------------------
    # Finalização da compra
    # ----------------------------------------------------------------

    @staticmethod
    def finalizar_pedido(pedido_id, metodo_pagamento):
        """
        Finaliza a compra: avança o status do pedido de PROCESSANDO
        para PAGO, e registra o pagamento (forma escolhida + status
        de aprovação). A partir daqui, o pedido deixa de ser o
        "carrinho atual" do usuário (um novo carrinho será criado na
        próxima vez que ele adicionar um item).

        Args:
            pedido_id: id do pedido a finalizar.
            metodo_pagamento: um dos valores aceitos pela constraint do
                banco (ver app.models.pagamento): CARTAO_CREDITO,
                BOLETO, PIX ou TRANSFERENCIA.

        Retorna o pedido atualizado, ou None se ele não existir ou
        não tiver itens.
        """
        pedido = db.session.get(Pedido, pedido_id)
        if pedido is None or not pedido.itens:
            return None

        PedidoDAO._recalcular_total(pedido_id)
        pedido.status_pedido = STATUS_PAGO

        pagamento = db.session.get(Pagamento, pedido_id)
        if pagamento is None:
            pagamento = Pagamento(
                pedido_id=pedido_id,
                metodo_pagamento=metodo_pagamento,
                status_pagamento=STATUS_APROVADO,
            )
            db.session.add(pagamento)
        else:
            pagamento.metodo_pagamento = metodo_pagamento
            pagamento.status_pagamento = STATUS_APROVADO

        db.session.commit()
        return pedido