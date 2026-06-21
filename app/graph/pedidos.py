"""
Operações de escrita no grafo disparadas pelo fluxo de pedidos.

Estrutura criada:
    (Usuario {cpf})-[:usuacomprou {quantidade}]->(Categoria {nome})

Usa MERGE em nós e relacionamento para que compras repetidas na mesma
categoria acumulem quantidade, sem duplicar nós nem arestas.
"""

from app.graph.connection import get_driver


def registrar_compra(cpf: str, itens) -> None:
    """
    Registra no grafo as categorias compradas pelo usuário ao finalizar
    um pedido. Cada item do pedido gera (ou atualiza) a relação COMPROU
    entre o nó Usuario e o nó Categoria correspondente.

    Args:
        cpf:   CPF do usuário que finalizou o pedido.
        itens: lista de ItemPedido com .produto.categoria e .quantidade.
    """
    driver = get_driver()
    with driver.session() as neo4j_session:
        for item in itens:
            neo4j_session.execute_write(
                _merge_comprou,
                cpf,
                item.produto.categoria,
                item.quantidade,
            )


def _merge_comprou(tx, cpf: str, categoria: str, quantidade: int) -> None:
    tx.run(
        """
        MERGE (u:Usuario {cpf: $cpf})
        MERGE (c:Categoria {nome: $categoria})
        MERGE (u)-[r:usuacomprou]->(c)
        ON CREATE SET r.quantidade = $quantidade
        ON MATCH  SET r.quantidade = r.quantidade + $quantidade
        """,
        cpf=cpf,
        categoria=categoria,
        quantidade=quantidade,
    )


def categorias_preferidas(cpf: str, limite: int = 2) -> list[str]:
    """
    Retorna as categorias que o usuário mais comprou, ordenadas por
    quantidade total de itens adquiridos naquela categoria.

    Args:
        cpf:    CPF do usuário.
        limite: quantas categorias retornar (padrão: 2).

    Returns:
        Lista de nomes de categoria, do mais comprado ao menos comprado.
        Retorna lista vazia se o usuário não tiver histórico no grafo.
    """
    query = """
    MATCH (u:Usuario {cpf: $cpf})-[r:usuacomprou]->(c:Categoria)
    RETURN c.nome AS categoria, r.quantidade AS quantidade
    ORDER BY r.quantidade DESC
    LIMIT $limite
    """
    driver = get_driver()
    with driver.session() as neo4j_session:
        resultado = neo4j_session.run(query, cpf=cpf, limite=limite)
        return [registro["categoria"] for registro in resultado]
