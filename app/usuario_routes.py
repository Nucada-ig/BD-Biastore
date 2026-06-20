from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth_utils import login_obrigatorio
from app.dao import UsuarioDAO, ProdutoDAO, PedidoDAO

# Blueprint da area do usuario comum: home, perfil e pedidos
usuario = Blueprint("usuario", __name__, url_prefix="/usuario")


@usuario.route("/home")
@login_obrigatorio
def home():
    """
    Home page do usuario: abre com recomendacoes de produtos personalizados.
    Por enquanto exibe o catalogo geral como recomendacao (ajustar quando
    houver logica de personalizacao).
    """
    produtos = ProdutoDAO.listar_todos()
    return render_template("usuario/home.html", produtos=produtos)


@usuario.route("/perfil", methods=["GET", "POST"])
@login_obrigatorio
def perfil():
    """
    Exibe e permite editar as informacoes basicas do usuario logado.
    """
    usuario_logado = UsuarioDAO.buscar_por_id(session["usuario_id"])

    if request.method == "POST":
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        UsuarioDAO.atualizar(usuario_logado.id, nome=nome, endereco=endereco)
        return redirect(url_for("usuario.perfil"))

    return render_template("usuario/perfil.html", usuario=usuario_logado)


@usuario.route("/pedidos")
@login_obrigatorio
def pedidos():
    """
    Exibe os pedidos do usuario logado, com status (entregue, a caminho, etc.).
    Rota de nivel 3, acessada a partir do perfil.
    """
    lista_pedidos = PedidoDAO.listar_por_usuario(session["usuario_id"])
    return render_template("usuario/pedidos.html", pedidos=lista_pedidos)
