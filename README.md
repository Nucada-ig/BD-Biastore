# BIA-Store

Aplicação web de e-commerce desenvolvida em **Flask**, como projeto acadêmico. Permite que usuários comprem produtos e que vendedores cadastrem e gerenciem seus próprios produtos.

## Tecnologias

- **Python 3 + Flask** — framework web
- **Flask-SQLAlchemy** — ORM para acesso ao banco de dados
- **PostgreSQL** (Google Cloud SQL) — banco de dados em produção
- **SQLite** — fallback automático para desenvolvimento local

## Estrutura do projeto

```
ecommerce/
├── mainflask.py              # ponto de entrada da aplicação
├── seed.py                   # popula o banco com dados de teste
├── requirements.txt
└── app/
    ├── __init__.py            # application factory (create_app)
    ├── routes.py              # registro central dos blueprints
    ├── auth_routes.py         # rotas de login e cadastro
    ├── auth_utils.py          # decorators de controle de acesso
    ├── usuario_routes.py      # rotas do usuário: home, perfil, pedidos
    ├── produto_routes.py      # rotas de produto: pesquisa e visualização
    ├── carrinho_routes.py     # rotas de carrinho e finalização da compra
    ├── vendedor_routes.py     # rotas do vendedor: home, cadastro/edição de produtos
    ├── dao/                   # acesso ao banco de dados (Data Access Object)
    ├── database/              # configuração da conexão (SQLAlchemy)
    ├── models/                # classes de modelo (Usuario, Produto, Carrinho, Pedido)
    └── view/
        ├── templates/         # HTMLs, organizados por área
        └── static/            # CSS e JS
```

## Como rodar localmente

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone <url-do-repositorio>
   cd ecommerce
   ```

2. (Opcional, recomendado) crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Popule o banco com dados de teste (cria automaticamente as tabelas em SQLite):
   ```bash
   python seed.py
   ```

5. Inicie a aplicação:
   ```bash
   python mainflask.py
   ```

6. Acesse em [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Contas de teste

Criadas automaticamente pelo `seed.py`:

| Perfil    | E-mail               | Senha    |
|-----------|-----------------------|----------|
| Cliente   | cliente@teste.com     | 123456   |
| Vendedor  | loja@biastore.com     | 123456   |

> Senhas armazenadas em texto puro propositalmente nesta etapa do projeto (foco em fluxo/funcionalidades). Hash de senha e validação de campos serão implementados em uma etapa posterior.

## Banco de dados (Google Cloud SQL)

Por padrão, sem nenhuma variável de ambiente configurada, a aplicação usa um arquivo SQLite local (`app/database/ecommerce.db`) — ideal para desenvolvimento.

Para conectar a uma instância PostgreSQL no Google Cloud SQL, defina as variáveis de ambiente:

```bash
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_NAME=nome_do_banco
DB_HOST=127.0.0.1          # ou o IP da instância
DB_PORT=5432
# alternativamente, em ambientes Cloud Run/App Engine:
INSTANCE_CONNECTION_NAME=projeto:regiao:instancia
```

A lógica de montagem da URI de conexão está em `app/database/__init__.py`.
 
