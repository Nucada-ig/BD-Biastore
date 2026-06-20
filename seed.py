"""
Script de seed: popula o banco de dados com dados de teste para que a
aplicacao tenha conteudo navegavel (vendedores, um cliente e produtos).

Como usar:
    python seed.py

Pode ser executado quantas vezes quiser: ele verifica se os dados de
teste já existem antes de inserir, evitando duplicar registros.
"""

from app import create_app
from app.database import db
from app.dao import UsuarioDAO, ProdutoDAO


PRODUTOS_TESTE = [
    {
        "nome": "Camiseta Essencial Algodão",
        "preco": 59.90,
        "descricao": "Camiseta básica de algodão pima, corte reto, ideal para o dia a dia.",
        "imagem": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600",
    },
    {
        "nome": "Calça Jeans Reta",
        "preco": 159.90,
        "descricao": "Calça jeans de corte reto, lavagem média, tecido resistente.",
        "imagem": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600",
    },
    {
        "nome": "Tênis Casual Branco",
        "preco": 229.90,
        "descricao": "Tênis casual unissex, solado em EVA leve, combina com qualquer look.",
        "imagem": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
    },
    {
        "nome": "Jaqueta Jeans",
        "preco": 189.90,
        "descricao": "Jaqueta jeans clássica, forro leve, ótima para dias mais frios.",
        "imagem": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600",
    },
    {
        "nome": "Boné Aba Curva",
        "preco": 49.90,
        "descricao": "Boné em sarja, aba curva, ajuste traseiro com fivela.",
        "imagem": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600",
    },
    {
        "nome": "Mochila Urbana Impermeável",
        "preco": 139.90,
        "descricao": "Mochila com compartimento para notebook e tecido impermeável.",
        "imagem": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
    },
]


def seed():
    app = create_app()

    with app.app_context():
        # Cria as tabelas se ainda não existirem (uso local/dev com SQLite).
        # No Cloud SQL, as tabelas já são gerenciadas separadamente.
        db.create_all()

        # ----- Vendedor de teste -----
        vendedor = UsuarioDAO.buscar_por_email("loja@biastore.com")
        if vendedor is None:
            vendedor = UsuarioDAO.criar(
                nome="BIA-Store",
                email="loja@biastore.com",
                senha="123456",
                is_vendedor=True,
            )
            print(f"Vendedor criado: {vendedor.nome} ({vendedor.email})")
        else:
            print(f"Vendedor já existia: {vendedor.nome} ({vendedor.email})")

        # ----- Cliente de teste -----
        cliente = UsuarioDAO.buscar_por_email("cliente@teste.com")
        if cliente is None:
            cliente = UsuarioDAO.criar(
                nome="Cliente Teste",
                email="cliente@teste.com",
                senha="123456",
                endereco="Rua das Flores, 123 - Centro",
            )
            print(f"Cliente criado: {cliente.nome} ({cliente.email})")
        else:
            print(f"Cliente já existia: {cliente.nome} ({cliente.email})")

        # ----- Produtos de teste, vinculados ao vendedor -----
        produtos_existentes = {p.nome for p in ProdutoDAO.listar_por_vendedor(vendedor.id)}
        criados = 0
        for dados in PRODUTOS_TESTE:
            if dados["nome"] in produtos_existentes:
                continue
            ProdutoDAO.criar(
                nome=dados["nome"],
                preco=dados["preco"],
                vendedor_id=vendedor.id,
                imagem=dados["imagem"],
                descricao=dados["descricao"],
            )
            criados += 1

        print(f"Produtos novos criados: {criados}")
        print(f"Total de produtos do vendedor: {len(ProdutoDAO.listar_por_vendedor(vendedor.id))}")
        print("\nSeed concluído.")
        print("Login do vendedor -> email: loja@biastore.com | senha: 123456")
        print("Login do cliente  -> email: cliente@teste.com | senha: 123456")


if __name__ == "__main__":
    seed()
