from flask import Flask
from app.database import db, build_database_uri


def create_app():
    """
    Application Factory: cria e configura a instância do Flask.
    """
    app = Flask(
        __name__,
        template_folder="view/templates",
        static_folder="view/static"
    )


    # Chave secreta para assinar cookies de sessão
    import os
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao")

    # Configuração do banco de dados:
    # usa Postgres/Cloud SQL se as variáveis de ambiente estiverem definidas,
    # caso contrário cai para SQLite local (apenas para desenvolvimento).
    app.config["SQLALCHEMY_DATABASE_URI"] = build_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa o SQLAlchemy com a aplicação
    db.init_app(app)

    # Importa os models para que o SQLAlchemy os reconheça
    from app import models  # noqa: F401

    # Registra todas as rotas da aplicação (cada area em seu proprio arquivo)
    from app.routes import register_blueprints
    register_blueprints(app)

   

    return app
