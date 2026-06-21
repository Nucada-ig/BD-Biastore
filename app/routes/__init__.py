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
    """
    from app.routes.auth import auth
    from app.routes.usuario import usuario
    from app.routes.produto import produto
    from app.routes.carrinho import carrinho
    from app.routes.vendedor import vendedor

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(usuario)
    app.register_blueprint(produto)
    app.register_blueprint(carrinho)
    app.register_blueprint(vendedor)
