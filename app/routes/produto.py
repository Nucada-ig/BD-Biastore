from flask import Blueprint, render_template, request, session
from app.auth_utils import login_obrigatorio
from app.dao import ProdutoDAO

# Blueprint de produto: pesquisa no catalogo e visualizacao de um produto especifico
produto = Blueprint("produto", __name__, url_prefix="/produto")


@produto.route("/pesquisa")
@login_obrigatorio
def pesquisa():
    """
    Busca no catálogo com filtros opcionais de texto e categoria via querystring:
        ?q=termo        filtra por nome
        ?categoria=X    filtra por categoria
    Os dois filtros são cumulativos.
    """
    termo = request.args.get("q", "")
    categoria_ativa = request.args.get("categoria", "")

    produtos = ProdutoDAO.buscar_por_nome(termo) if termo else ProdutoDAO.listar_todos()

    if categoria_ativa:
        produtos = [p for p in produtos if p.categoria == categoria_ativa]

    categorias = ProdutoDAO.listar_categorias()

    return render_template(
        "produto/pesquisa.html",
        produtos=produtos,
        termo=termo,
        categoria_ativa=categoria_ativa,
        categorias=categorias,
    )


@produto.route("/<int:produto_id>")
@login_obrigatorio
def ver_produto(produto_id):
    """
    Abre a pagina de informacoes do produto: preco, categoria, estoque etc.
    Se o usuario logado for o vendedor dono do produto, exibe tambem as
    opcoes de editar/excluir.
    """
    item = ProdutoDAO.buscar_por_id(produto_id)
    if item is None:
        return render_template("produto/produto.html", produto=None), 404

    eh_vendedor_dono = (
        session.get("tipo_sessao") == "vendedor"
        and item.vendedor_id == session.get("vendedor_id")
    )

    return render_template(
        "produto/produto.html",
        produto=item,
        eh_vendedor_dono=eh_vendedor_dono,
    )
