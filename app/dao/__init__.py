# Pacote responsável pelas classes DAO (Data Access Object),
# que fazem a comunicação entre os models e o banco de dados.

from app.dao.usuario_dao import UsuarioDAO
from app.dao.produto_dao import ProdutoDAO
from app.dao.carrinho_dao import CarrinhoDAO
from app.dao.pedido_dao import PedidoDAO

__all__ = [
    "UsuarioDAO",
    "ProdutoDAO",
    "CarrinhoDAO",
    "PedidoDAO",
]
