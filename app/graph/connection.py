"""
Conexão com o banco de dados em grafos (Neo4j AuraDB).

Mantido isolado do app/database/ (que cuida do banco relacional), já que
são tecnologias e finalidades diferentes: o relacional guarda os dados
"vivos" da aplicação (usuários, produtos, pedidos), enquanto o grafo é
usado apenas para consultas de recomendação.
"""

import os
from neo4j import GraphDatabase


# OBS sobre o protocolo: usamos neo4j+ssc:// (TLS sem verificação estrita
# de certificado) por padrão, em vez de neo4j+s://, porque em alguns
# ambientes Windows o Python não usa corretamente o store de certificados
# raiz do sistema, causando falha de roteamento mesmo com credenciais e
# rede corretas. Se o ambiente de quem for rodar não tiver esse problema,
# a variável NEO4J_URI pode ser definida com neo4j+s:// sem alterar o código.


_driver = None


def get_driver():
    """
    Retorna uma instância única (singleton) do driver do Neo4j,
    criando-a na primeira chamada e reaproveitando nas próximas.
    As variáveis são lidas do ambiente na primeira chamada para que
    a aplicação não quebre na inicialização caso o .env esteja incompleto.
    """
    global _driver
    if _driver is None:
        uri = os.environ.get("NEO4J_URI")
        user = os.environ.get("NEO4J_USER")
        password = os.environ.get("NEO4J_PASSWORD")
        if not all([uri, user, password]):
            raise EnvironmentError(
                "Variáveis NEO4J_URI, NEO4J_USER e NEO4J_PASSWORD não encontradas. "
                "Configure o arquivo .env."
            )
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver


def fechar_driver():
    """
    Encerra a conexão com o Neo4j. Útil para chamar no encerramento da
    aplicação (ex: teardown do Flask), evitando conexões penduradas.
    """
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
