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

    # Configurações gerais da aplicação
    app.config["SECRET_KEY"] = "troque-essa-chave-em-producao"

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

    # OBS: não usamos db.create_all() aqui, pois as tabelas já são
    # criadas/gerenciadas diretamente no Cloud SQL (via SQL Studio /
    # migrations). Em ambiente local com SQLite, rode manualmente
    # `flask shell` -> `db.create_all()` se precisar criar as tabelas.

    return app
