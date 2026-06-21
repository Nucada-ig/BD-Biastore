# Pacote responsável pelas classes de modelo (entidades) da aplicação.
#
# Estrutura adaptada para refletir o banco relacional real (PostgreSQL
# no Google Cloud SQL). Diferenças importantes em relação à versão
# anterior (SQLite local):
#   - Usuario usa CPF como chave primária (não um id autoincrement)
#   - Vendedor é uma entidade própria, sem ligação direta com Usuario
#   - Não existe tabela de Carrinho: o carrinho de compras é
#     representado como um Pedido com status_pedido = PROCESSANDO

from app.models.usuario import Usuario
from app.models.vendedor import Vendedor
from app.models.produto import Produto
from app.models.pedido import Pedido, ItemPedido
from app.models.pagamento import Pagamento
from app.models.envio import Envio
from app.models.endereco import Endereco, EnderecoVendedor
from app.models.telefone import TelefoneCliente, TelefoneVendedor
from app.models.codigo_postal import CodigoPostal

__all__ = [
    "Usuario",
    "Vendedor",
    "Produto",
    "Pedido",
    "ItemPedido",
    "Pagamento",
    "Envio",
    "Endereco",
    "EnderecoVendedor",
    "TelefoneCliente",
    "TelefoneVendedor",
    "CodigoPostal",
]
