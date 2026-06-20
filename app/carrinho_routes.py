from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth_utils import login_obrigatorio
from app.dao import CarrinhoDAO, PedidoDAO

# Blueprint de carrinho: contem os produtos do usuario e leva para a finalizacao
carrinho = Blueprint("carrinho", __name__, url_prefix="/carrinho")


@carrinho.route("/")
@login_obrigatorio
def ver_carrinho():
    """
    Exibe os produtos que o usuario colocou no carrinho e o valor total.
    """
    carrinho_usuario = CarrinhoDAO.buscar_ou_criar(session["usuario_id"])
    total = CarrinhoDAO.calcular_total(carrinho_usuario.id)
    return render_template(
        "carrinho/carrinho.html",
        itens=carrinho_usuario.itens,
        total=total,
    )


@carrinho.route("/adicionar/<int:produto_id>", methods=["POST"])
@login_obrigatorio
def adicionar(produto_id):
    """
    Adiciona um produto ao carrinho do usuario logado.
    """
    quantidade = int(request.form.get("quantidade", 1))
    carrinho_usuario = CarrinhoDAO.buscar_ou_criar(session["usuario_id"])
    CarrinhoDAO.adicionar_item(carrinho_usuario.id, produto_id, quantidade)
    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho.route("/remover/<int:item_id>", methods=["POST"])
@login_obrigatorio
def remover(item_id):
    """
    Remove um item especifico do carrinho.
    """
    CarrinhoDAO.remover_item(item_id)
    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho.route("/finalizar", methods=["GET", "POST"])
@login_obrigatorio
def finalizar():
    """
    Rota responsavel pelo pagamento e finalizacao geral da compra.
    Transforma os itens do carrinho em um Pedido e esvazia o carrinho.
    """
    carrinho_usuario = CarrinhoDAO.buscar_ou_criar(session["usuario_id"])
    pedido = PedidoDAO.criar_a_partir_do_carrinho(carrinho_usuario.id, session["usuario_id"])

    if pedido is None:
        return redirect(url_for("carrinho.ver_carrinho"))

    return render_template("carrinho/finalizacao.html", pedido=pedido)
