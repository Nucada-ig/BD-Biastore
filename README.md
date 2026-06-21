# BIA-Store

Aplicação web de e-commerce desenvolvida em **Flask** como projeto acadêmico. Permite que clientes naveguem, adicionem ao carrinho e finalizem compras, enquanto vendedores cadastram e gerenciam seus próprios produtos.

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3 + Flask |
| ORM | Flask-SQLAlchemy |
| Banco relacional | PostgreSQL (Google Cloud SQL) em produção · SQLite como fallback local |
| Banco de grafos | Neo4j AuraDB — histórico de compras e recomendações |
| Frontend | Jinja2 · CSS próprio (sem framework) · JS vanilla |

## Funcionalidades

**Clientes**
- Cadastro e login
- Vitrine com paginação e dois carrosséis de recomendação personalizados (baseados no histórico de compras no grafo)
- Pesquisa de produtos com filtro por categoria
- Página de detalhe do produto com adição ao carrinho via AJAX (sem recarregar a página)
- Checkout com seleção de endereço de entrega e forma de pagamento
- Histórico de pedidos e gerenciamento de perfil (e-mail, senha, endereços)

**Vendedores**
- Painel próprio para cadastrar, editar e excluir produtos
- Acesso restrito ao estoque e produtos da própria loja

**Recomendações (Neo4j)**
- Ao finalizar uma compra, a relação `(Usuario)-[:usuacomprou]->(Categoria)` é registrada no grafo
- A home exibe dois carrosséis: o primeiro com produtos da categoria mais comprada, o segundo com um mix das três principais

## Estrutura do projeto

```
BD-Biastore/
├── mainflask.py              # ponto de entrada da aplicação
├── seed.py                   # popula o banco com dados e histórico de teste
├── requirements.txt
└── app/
    ├── __init__.py           # application factory (create_app)
    ├── auth_utils.py         # decorators de controle de acesso
    ├── routes/               # blueprints organizados por área
    │   ├── __init__.py       # registro central dos blueprints
    │   ├── auth.py           # login e cadastro
    │   ├── usuario.py        # home, perfil, pedidos, endereços
    │   ├── produto.py        # pesquisa e visualização de produto
    │   ├── carrinho.py       # carrinho e finalização de compra
    │   └── vendedor.py       # painel do vendedor
    ├── graph/                # integração Neo4j
    │   ├── connection.py     # driver singleton (leitura lazy do .env)
    │   └── pedidos.py        # registrar_compra · categorias_preferidas
    ├── dao/                  # Data Access Objects
    ├── database/             # configuração de conexão (SQLAlchemy)
    ├── models/               # modelos ORM
    └── view/
        ├── templates/        # HTMLs organizados por área
        └── static/           # CSS e assets
```

## Como rodar localmente

### 1. Clone e entre na pasta

```bash
git clone <url-do-repositorio>
cd BD-Biastore
```

### 2. Ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto. Sem ele a aplicação usa SQLite e desativa as recomendações.

```env
# Banco relacional (PostgreSQL)
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=biastore

# Banco de grafos (Neo4j AuraDB)
NEO4J_URI=neo4j+ssc://xxxxxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=senha
```

> Se as variáveis de banco relacional não estiverem definidas, a aplicação usa SQLite automaticamente.  
> Se as variáveis do Neo4j não estiverem definidas, os carrosséis de recomendação são omitidos silenciosamente.

### 5. Popule o banco

```bash
python seed.py
```

Cria vendedores, produtos, clientes e histórico de compras de teste.

### 6. Inicie a aplicação

```bash
python mainflask.py
```

Acesse em [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Contas de teste

Criadas automaticamente pelo `seed.py`. Na tela de login há um dropdown **"Selecionar conta"** que preenche as credenciais automaticamente.

### Clientes

| Nome | E-mail | Senha |
|------|--------|-------|
| Cliente Teste | cliente@teste.com | 123456 |
| Ana Lima | ana.lima@teste.com | 123456 |
| Bruno Souza | bruno.souza@teste.com | 123456 |
| Carla Mendes | carla.mendes@teste.com | 123456 |
| Diego Oliveira | diego.oliveira@teste.com | 123456 |
| Fernanda Costa | fernanda.costa@teste.com | 123456 |

Os clientes com nomes reais já possuem histórico de compras em categorias distintas, o que ativa os carrosséis de recomendação na home.

### Vendedores

| Loja | E-mail | Senha | Categoria principal |
|------|--------|-------|---------------------|
| TechStore | loja@techstore.com | 123456 | Eletrônicos |
| Mundo Kids | loja@mundokids.com | 123456 | Brinquedos |
| BitShop | loja@bitshop.com | 123456 | Informática e Acessórios |
| Ativa Esportes | loja@ativaesportes.com | 123456 | Esporte e Lazer |
| Natura Beleza | loja@naturabeleza.com | 123456 | Beleza e Saúde |
