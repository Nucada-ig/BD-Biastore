from flask import Blueprint, render_template, request, session
from app.auth_utils import login_obrigatorio
from app.dao import ProdutoDAO

# Blueprint de produto: pesquisa no catalogo e visualizacao de um produto especifico
produto = Blueprint("produto", __name__, url_prefix="/produto")


@produto.route("/pesquisa")
@login_obrigatorio
def pesquisa():
    """
    Busca no catalogo geral os produtos de acordo com a busca do usuario.
    Permite filtro futuro (preco, categoria, etc.) via querystring.
    """
    termo = request.args.get("q", "")
    produtos = ProdutoDAO.buscar_por_nome(termo) if termo else ProdutoDAO.listar_todos()
    return render_template("produto/pesquisa.html", produtos=produtos, termo=termo)


@produto.route("/<int:produto_id>")
@login_obrigatorio
def ver_produto(produto_id):
    """
    Abre a pagina de informacoes do produto: preco, imagem, descricao etc.
    Se o usuario logado for o vendedor dono do produto, exibe tambem as
    opcoes de editar/excluir.
    """
    item = ProdutoDAO.buscar_por_id(produto_id)
    if item is None:
        return render_template("produto/produto.html", produto=None), 404

    eh_vendedor_dono = (
        session.get("is_vendedor")
        and item.vendedor_id == session.get("usuario_id")
    )

    return render_template(
        "produto/produto.html",
        produto=item,
        eh_vendedor_dono=eh_vendedor_dono,
    )
