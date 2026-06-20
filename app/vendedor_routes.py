from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from app.auth_utils import vendedor_obrigatorio
from app.dao import ProdutoDAO

# Blueprint da area do vendedor: home, cadastro/edicao/exclusao de produtos
vendedor = Blueprint("vendedor", __name__, url_prefix="/vendedor")


@vendedor.route("/home")
@vendedor_obrigatorio
def home():
    """
    Home page do vendedor: visualizacao dos produtos cadastrados,
    com caminho para cadastro/edicao de produtos.
    """
    produtos = ProdutoDAO.listar_por_vendedor(session["usuario_id"])
    return render_template("vendedor/home.html", produtos=produtos)


@vendedor.route("/produto/cadastro", methods=["GET", "POST"])
@vendedor_obrigatorio
def cadastrar_produto():
    """
    Pagina para o cadastro de novos produtos: nome, imagem, preco, descricao.
    """
    if request.method == "POST":
        ProdutoDAO.criar(
            nome=request.form.get("nome"),
            preco=float(request.form.get("preco")),
            vendedor_id=session["usuario_id"],
            imagem=request.form.get("imagem"),
            descricao=request.form.get("descricao"),
        )
        return redirect(url_for("vendedor.home"))

    return render_template("vendedor/cadastro_produto.html", produto=None)


def _garantir_produto_do_vendedor(produto_id):
    """
    Busca o produto e garante que ele pertence ao vendedor logado.
    Retorna o produto, ou interrompe a requisicao com 404 caso contrario.
    """
    item = ProdutoDAO.buscar_por_id(produto_id)
    if item is None or item.vendedor_id != session["usuario_id"]:
        abort(404)
    return item


@vendedor.route("/produto/<int:produto_id>/editar", methods=["GET", "POST"])
@vendedor_obrigatorio
def editar_produto(produto_id):
    """
    Permite alterar um produto ja cadastrado pelo vendedor logado.
    """
    item = _garantir_produto_do_vendedor(produto_id)

    if request.method == "POST":
        ProdutoDAO.atualizar(
            produto_id,
            nome=request.form.get("nome"),
            preco=float(request.form.get("preco")),
            imagem=request.form.get("imagem"),
            descricao=request.form.get("descricao"),
        )
        return redirect(url_for("produto.ver_produto", produto_id=produto_id))

    return render_template("vendedor/cadastro_produto.html", produto=item)


@vendedor.route("/produto/<int:produto_id>/deletar", methods=["POST"])
@vendedor_obrigatorio
def deletar_produto(produto_id):
    """
    Remove (retira) um produto cadastrado pelo vendedor logado.
    """
    _garantir_produto_do_vendedor(produto_id)
    ProdutoDAO.deletar(produto_id)
    return redirect(url_for("vendedor.home"))
