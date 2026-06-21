import os
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

# Instância única do SQLAlchemy, usada por todos os models da aplicação.
db = SQLAlchemy()


def build_database_uri():
    """
    Monta a URI de conexão do banco de dados.

    - Em produção, aponta para o PostgreSQL no Google Cloud SQL.
    - Localmente, se as variáveis de ambiente do Cloud SQL não estiverem
      definidas, cai para um arquivo SQLite (apenas para desenvolvimento).

    Variáveis de ambiente esperadas (Cloud SQL):
        DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
        INSTANCE_CONNECTION_NAME (quando usado o Cloud SQL Auth Proxy / socket unix)
    """
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
    db_host = os.environ.get("DB_HOST", "127.0.0.1")
    db_port = os.environ.get("DB_PORT", "5432")

    # Conexão via Cloud SQL Auth Proxy / socket unix (usado no Cloud Run/App Engine)
    if db_user and db_password and db_name and instance_connection_name:
        return (
            f"postgresql+psycopg2://{db_user}:{quote_plus(db_password)}@/"
            f"{db_name}?host=/cloudsql/{instance_connection_name}"
        )

    # Conexão via host/porta (ex: Cloud SQL Auth Proxy local, ou IP direto)
    if db_user and db_password and db_name:
        return f"postgresql+psycopg2://{db_user}:{quote_plus(db_password)}@{db_host}:{db_port}/{db_name}"

    # Fallback local para desenvolvimento sem Cloud SQL configurado
    sqlite_path = os.path.join(os.path.dirname(__file__), "ecommerce.db")
    return f"sqlite:///{sqlite_path}"
