from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.auth_utils import usuario_obrigatorio
from app.dao import PedidoDAO, EnderecoDAO
from app.graph import registrar_compra

# Blueprint de carrinho: contem os produtos do usuario e leva para a finalizacao.
# O "carrinho" e representado, no banco, como um Pedido com status PROCESSANDO.
carrinho = Blueprint("carrinho", __name__, url_prefix="/carrinho")


@carrinho.route("/")
@usuario_obrigatorio
def ver_carrinho():
    """
    Exibe os produtos que o usuario colocou no carrinho e o valor total.
    """
    cpf = session["usuario_cpf"]
    carrinho_usuario = PedidoDAO.buscar_ou_criar_carrinho(cpf)
    total = PedidoDAO.calcular_total(carrinho_usuario.pedido_id)
    enderecos = EnderecoDAO.listar_por_usuario(cpf)
    return render_template(
        "carrinho/carrinho.html",
        itens=carrinho_usuario.itens,
        total=total,
        enderecos=enderecos,
    )


@carrinho.route("/adicionar/<int:produto_id>", methods=["POST"])
@usuario_obrigatorio
def adicionar(produto_id):
    """
    Adiciona um produto ao carrinho do usuario logado.
    Requisições AJAX (X-Requested-With: XMLHttpRequest) recebem JSON;
    requisições normais redirecionam para o carrinho.
    """
    from flask import jsonify
    quantidade = int(request.form.get("quantidade", 1))
    carrinho_usuario = PedidoDAO.buscar_ou_criar_carrinho(session["usuario_cpf"])
    PedidoDAO.adicionar_item(carrinho_usuario.pedido_id, produto_id, quantidade)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(ok=True)
    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho.route("/remover/<int:produto_id>", methods=["POST"])
@usuario_obrigatorio
def remover(produto_id):
    """
    Remove um item especifico do carrinho do usuario logado, identificado
    pelo produto_id (a chave do item no pedido e composta por
    produto_id + pedido_id).
    """
    carrinho_usuario = PedidoDAO.buscar_ou_criar_carrinho(session["usuario_cpf"])
    PedidoDAO.remover_item(carrinho_usuario.pedido_id, produto_id)
    return redirect(url_for("carrinho.ver_carrinho"))


@carrinho.route("/finalizar", methods=["POST"])
@usuario_obrigatorio
def finalizar():
    """
    Rota responsavel pelo pagamento e finalizacao geral da compra.
    Avanca o pedido (que ate aqui era o "carrinho", em PROCESSANDO)
    para o status PAGO, e registra a forma de pagamento escolhida.
    """
    cpf = session["usuario_cpf"]
    metodo_pagamento = request.form.get("metodo_pagamento")
    endereco_id = request.form.get("endereco_id", type=int)

    if not endereco_id:
        flash("Selecione um endereço de entrega.", "erro")
        return redirect(url_for("carrinho.ver_carrinho"))

    endereco = EnderecoDAO.buscar(endereco_id)
    if endereco is None or endereco.cpf != cpf:
        flash("Endereço inválido.", "erro")
        return redirect(url_for("carrinho.ver_carrinho"))

    carrinho_usuario = PedidoDAO.buscar_ou_criar_carrinho(cpf)
    pedido = PedidoDAO.finalizar_pedido(carrinho_usuario.pedido_id, metodo_pagamento)

    if pedido is None:
        return redirect(url_for("carrinho.ver_carrinho"))

    try:
        registrar_compra(cpf, pedido.itens)
    except Exception as e:
        import traceback
        print("[GRAFO] Erro ao registrar compra:", traceback.format_exc())

    return render_template("carrinho/finalizacao.html", pedido=pedido, endereco=endereco)