from flask import Blueprint, redirect, url_for

# Blueprint raiz, usado apenas para o redirecionamento inicial ("/")
routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    """Redireciona a raiz da aplicacao para a tela de login."""
    return redirect(url_for("auth.login"))


def register_blueprints(app):
    """
    Registra todos os blueprints de rotas da aplicacao.
    Cada area (auth, usuario, produto, carrinho, vendedor) fica em seu
    proprio arquivo dentro da pasta app/, conforme a estrutura definida.
    """
    from app.auth_routes import auth
    from app.usuario_routes import usuario
    from app.produto_routes import produto
    from app.carrinho_routes import carrinho
    from app.vendedor_routes import vendedor

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(usuario)
    app.register_blueprint(produto)
    app.register_blueprint(carrinho)
    app.register_blueprint(vendedor)
