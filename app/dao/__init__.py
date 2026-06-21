# Pacote responsável pelas classes DAO (Data Access Object),
# que fazem a comunicação entre os models e o banco de dados.

from app.dao.usuario_dao import UsuarioDAO
from app.dao.vendedor_dao import VendedorDAO
from app.dao.produto_dao import ProdutoDAO
from app.dao.pedido_dao import PedidoDAO
from app.dao.endereco_dao import EnderecoDAO

__all__ = [
    "UsuarioDAO",
    "VendedorDAO",
    "ProdutoDAO",
    "PedidoDAO",
    "EnderecoDAO",
]
