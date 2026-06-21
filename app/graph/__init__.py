# Pacote responsável pelo acesso ao banco de dados em grafos (Neo4j).
# Mantido separado da pasta `dao/`, que fala apenas com o banco relacional.

from app.graph.recomendacao import categoria_preferida_do_cliente
from app.graph.pedidos import registrar_compra, categorias_preferidas

__all__ = [
    "categoria_preferida_do_cliente",
    "registrar_compra",
    "categorias_preferidas",
]
