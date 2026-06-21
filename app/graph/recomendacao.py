"""
Consultas de recomendação baseadas no grafo de compras (dataset Olist).

Caminho percorrido no grafo (direções confirmadas via inspeção real do
banco - atenção que "contém itens" e "info itens" apontam na direção
CONTRÁRIA à leitura intuitiva do nome):

    (customer) -[:comprou]-> (order) <-[:`contém itens`]- (order_item)
               <-[:`info itens`]- (product)

Onde:
    - customer.customer_id        identifica o cliente
    - order.order_id               identifica o pedido
    - order_item.order_item_id     identifica a linha do item dentro do pedido
                                     (uma linha por produto na order)
    - product.product_category_name  é a categoria do produto

Os relacionamentos não possuem propriedades próprias; toda a contagem é
feita a partir dos nós percorridos no caminho.
"""

from app.graph.connection import get_driver


def categoria_preferida_do_cliente(customer_id: str) -> str | None:
    """
    Retorna a categoria de produto mais comprada por um cliente,
    com base no histórico de compras registrado no grafo.

    Usada para alimentar a recomendação de produtos na home page:
    a ideia é sugerir produtos da categoria que o cliente mais compra.

    Args:
        customer_id: valor de customer_id do nó olist_customers_dataset.csv

    Returns:
        O nome da categoria mais comprada (str), ou None se o cliente
        não existir no grafo ou não tiver nenhuma compra registrada.
        Em caso de empate entre categorias, retorna uma delas (a ordem
        de desempate não é garantida).
    """
    query = """
    MATCH (c:`olist_customers_dataset.csv` {customer_id: $customer_id})
          -[:comprou]->(o:`olist_orders_dataset.csv`)
          <-[:`contém itens`]-(oi:`olist_order_items_dataset`)
          <-[:`info itens`]-(p:`olist_products_dataset.csv`)
    RETURN p.product_category_name AS categoria, count(oi) AS total_itens
    ORDER BY total_itens DESC
    LIMIT 1
    """

    driver = get_driver()
    with driver.session() as session:
        resultado = session.run(query, customer_id=customer_id)
        registro = resultado.single()
        return registro["categoria"] if registro else None
