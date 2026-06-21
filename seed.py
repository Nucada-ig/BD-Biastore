"""
Script de seed: popula o banco de dados com dados de teste.

Como usar:
    python seed.py

Categorias (alinhadas ao dataset Olist no Neo4j):
    eletronicos, brinquedos, informatica_acessorios,
    esporte_lazer, beleza_saude
"""

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.database import db
from app.dao import UsuarioDAO, VendedorDAO, ProdutoDAO, PedidoDAO


VENDEDORES_TESTE = [

    # ── TechStore · eletronicos ───────────────────────────────────────
    {
        "nome_vendedor": "TechStore",
        "cnpj_vendedor": "66777888000136",
        "email": "loja@techstore.com",
        "senha": "123456",
        "produtos": [
            {
                "nome_produto": "Smartphone 128 GB",
                "categoria": "eletronicos",
                "preco_unitario": 1299.90,
                "estoque": 25,
                "imagem": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
                "descricao": "Smartphone com tela AMOLED de 6,5'', processador octa-core e câmera tripla de 64 MP. Bateria de 5000 mAh com carregamento rápido 33W.",
                "material": "Vidro temperado + alumínio",
                "peso": "195g",
                "dimensoes": "163 × 75 × 8,5 mm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 7 dias para defeito de fábrica. Produto deve estar na embalagem original.",
            },
            {
                "nome_produto": "Fone Bluetooth Over-Ear",
                "categoria": "eletronicos",
                "preco_unitario": 249.90,
                "estoque": 40,
                "imagem": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
                "descricao": "Fone de ouvido over-ear com cancelamento ativo de ruído, autonomia de 30h e dobramento compacto. Conexão Bluetooth 5.3.",
                "material": "Plástico ABS + couro sintético",
                "peso": "280g",
                "dimensoes": "Headband ajustável — tamanho único",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias sem sinais de uso.",
            },
            {
                "nome_produto": "Smartwatch Fitness",
                "categoria": "eletronicos",
                "preco_unitario": 399.90,
                "estoque": 30,
                "imagem": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
                "descricao": "Smartwatch com monitor cardíaco, SpO2, GPS integrado e resistência à água IP68. Tela AMOLED 1,4'' sempre ativa.",
                "material": "Caixa: alumínio · Pulseira: silicone",
                "peso": "38g (sem pulseira)",
                "dimensoes": "44 × 38 × 10,7 mm",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
            {
                "nome_produto": "Câmera de Segurança Wi-Fi",
                "categoria": "eletronicos",
                "preco_unitario": 179.90,
                "estoque": 50,
                "imagem": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600",
                "descricao": "Câmera IP Full HD 1080p com visão noturna infravermelha, detecção de movimento e armazenamento em nuvem ou cartão SD.",
                "material": "Carcaça: policarbonato ABS",
                "peso": "180g",
                "dimensoes": "8,5 × 8,5 × 12 cm",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 7 dias para defeito de fábrica.",
            },
            {
                "nome_produto": "Caixa de Som Portátil 20W",
                "categoria": "eletronicos",
                "preco_unitario": 189.90,
                "estoque": 45,
                "imagem": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600",
                "descricao": "Caixa de som Bluetooth 5.0 com 20W RMS, resistência à água IPX7 e bateria de 12h. Graves potentes com tecnologia Bass Boost.",
                "material": "Plástico ABS + malha de tecido",
                "peso": "580g",
                "dimensoes": "20 × 8 × 8 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias sem sinais de uso.",
            },
        ],
    },

    # ── Mundo Kids · brinquedos ───────────────────────────────────────
    {
        "nome_vendedor": "Mundo Kids",
        "cnpj_vendedor": "77888999000127",
        "email": "loja@mundokids.com",
        "senha": "123456",
        "produtos": [
            {
                "nome_produto": "Kit de Blocos de Montar 500 peças",
                "categoria": "brinquedos",
                "preco_unitario": 149.90,
                "estoque": 35,
                "imagem": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=600",
                "descricao": "Kit de blocos coloridos compatíveis com as principais marcas do mercado. Estimula a criatividade e o raciocínio espacial. Indicado para +6 anos.",
                "material": "ABS não tóxico",
                "peso": "720g",
                "dimensoes": "Caixa: 38 × 28 × 8 cm · 500 peças",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
            {
                "nome_produto": "Boneca Articulada 30 cm",
                "categoria": "brinquedos",
                "preco_unitario": 79.90,
                "estoque": 50,
                "imagem": "https://images.unsplash.com/photo-1563396983906-b3795482a59a?w=600",
                "descricao": "Boneca com 11 pontos de articulação, cabelo penteável e acessórios inclusos. Indicada para crianças a partir de 3 anos.",
                "material": "Vinil atóxico",
                "peso": "310g",
                "dimensoes": "30 cm de altura",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias com produto sem uso.",
            },
            {
                "nome_produto": "Carrinho de Controle Remoto",
                "categoria": "brinquedos",
                "preco_unitario": 119.90,
                "estoque": 25,
                "imagem": "https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=600",
                "descricao": "Carrinho RC com tração 4×4, velocidade de até 25 km/h e autonomia de 30 min. Frequência 2,4 GHz sem interferência. Indicado para +8 anos.",
                "material": "ABS resistente a impacto",
                "peso": "850g",
                "dimensoes": "35 × 20 × 14 cm",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
            {
                "nome_produto": "Jogo de Tabuleiro Estratégia",
                "categoria": "brinquedos",
                "preco_unitario": 89.90,
                "estoque": 40,
                "imagem": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=600",
                "descricao": "Jogo de tabuleiro para 2 a 4 jogadores com cartas de missão e peças colecionáveis. Partidas de 45–90 min. Indicado para +10 anos.",
                "material": "Papelão rígido + plástico ABS",
                "peso": "1,1 kg",
                "dimensoes": "Caixa: 30 × 30 × 8 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias com caixa lacrada.",
            },
            {
                "nome_produto": "Pelúcia Urso 45 cm",
                "categoria": "brinquedos",
                "preco_unitario": 59.90,
                "estoque": 60,
                "imagem": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600",
                "descricao": "Pelúcia de urso macio e hipoalergênico com enchimento de fibra siliconada. Lavável em máquina. Indicado para todas as idades.",
                "material": "Pelúcia de poliéster · Enchimento: fibra siliconada",
                "peso": "400g",
                "dimensoes": "45 cm de altura sentado",
                "prazo_entrega": 4,
                "politica_troca": "Trocas em até 30 dias sem sinais de uso.",
            },
        ],
    },

    # ── BitShop · informatica_acessorios ──────────────────────────────
    {
        "nome_vendedor": "BitShop",
        "cnpj_vendedor": "88999000000118",
        "email": "loja@bitshop.com",
        "senha": "123456",
        "produtos": [
            {
                "nome_produto": "Teclado Mecânico TKL",
                "categoria": "informatica_acessorios",
                "preco_unitario": 299.90,
                "estoque": 20,
                "imagem": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600",
                "descricao": "Teclado mecânico tenkeyless (87 teclas) com switches lineares, retroiluminação RGB por tecla e cabo USB-C destacável.",
                "material": "Carcaça: alumínio escovado · Switches: mecânicos lineares",
                "peso": "780g",
                "dimensoes": "36 × 13 × 3,5 cm",
                "prazo_entrega": 7,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
            {
                "nome_produto": "Mouse Gamer 12000 DPI",
                "categoria": "informatica_acessorios",
                "preco_unitario": 159.90,
                "estoque": 35,
                "imagem": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600",
                "descricao": "Mouse gamer com sensor óptico de 12000 DPI ajustável, 7 botões programáveis e RGB. Cabo trançado de 1,8 m.",
                "material": "ABS texturizado + borracha lateral",
                "peso": "95g",
                "dimensoes": "12,5 × 6,5 × 4 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias sem sinais de uso.",
            },
            {
                "nome_produto": "Webcam Full HD 1080p",
                "categoria": "informatica_acessorios",
                "preco_unitario": 189.90,
                "estoque": 30,
                "imagem": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=600",
                "descricao": "Webcam com resolução Full HD 1080p a 30 fps, microfone embutido com cancelamento de ruído e correção automática de luz.",
                "material": "Plástico ABS + vidro óptico",
                "peso": "160g",
                "dimensoes": "8,5 × 6 × 5 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias com produto lacrado.",
            },
            {
                "nome_produto": "HD Externo Portátil 1 TB",
                "categoria": "informatica_acessorios",
                "preco_unitario": 279.90,
                "estoque": 22,
                "imagem": "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=600",
                "descricao": "HD externo de 1 TB com USB 3.0, velocidade de leitura de até 130 MB/s e carcaça anti-impacto. Compatível com PC, Mac e console.",
                "material": "Policarbonato com revestimento emborrachado",
                "peso": "148g",
                "dimensoes": "11 × 7,5 × 1,5 cm",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 7 dias para defeito. Dados não recuperados após retorno.",
            },
            {
                "nome_produto": "Hub USB-C 7 em 1",
                "categoria": "informatica_acessorios",
                "preco_unitario": 129.90,
                "estoque": 40,
                "imagem": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=600",
                "descricao": "Hub USB-C com HDMI 4K, 3× USB-A 3.0, leitor de cartão SD/microSD e Power Delivery de 100W. Compatível com MacBook e notebooks USB-C.",
                "material": "Liga de alumínio",
                "peso": "98g",
                "dimensoes": "11 × 3,5 × 1,2 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
        ],
    },

    # ── Ativa Esportes · esporte_lazer ───────────────────────────────
    {
        "nome_vendedor": "Ativa Esportes",
        "cnpj_vendedor": "44555666000154",
        "email": "loja@ativaesportes.com",
        "senha": "123456",
        "produtos": [
            {
                "nome_produto": "Raquete de Beach Tennis",
                "categoria": "esporte_lazer",
                "preco_unitario": 189.90,
                "estoque": 20,
                "imagem": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=600",
                "descricao": "Raquete de beach tennis em fibra de carbono com núcleo EVA. Controle e potência para jogadores intermediários.",
                "material": "Face: fibra de carbono · Núcleo: EVA",
                "peso": "340g",
                "dimensoes": "Comprimento: 57 cm · Largura: 29 cm",
                "prazo_entrega": 7,
                "politica_troca": "Trocas em até 30 dias sem sinais de uso em quadra.",
            },
            {
                "nome_produto": "Bola de Futebol Campo",
                "categoria": "esporte_lazer",
                "preco_unitario": 79.90,
                "estoque": 60,
                "imagem": "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=600",
                "descricao": "Bola de futebol campo costurada à mão com câmara de butil de alta retenção de ar. Tamanho oficial 5.",
                "material": "Couro sintético PU · Câmara: butil",
                "peso": "430g",
                "dimensoes": "Circunferência: 68–70 cm (tamanho 5)",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias sem uso em campo.",
            },
            {
                "nome_produto": "Luva de Boxe 14 oz",
                "categoria": "esporte_lazer",
                "preco_unitario": 149.90,
                "estoque": 30,
                "imagem": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=600",
                "descricao": "Luva de boxe em couro sintético com espuma de alto impacto e fecho em velcro. Ideal para treino e sparring.",
                "material": "Couro sintético · Espuma: PU alta densidade",
                "peso": "400g (par 14 oz)",
                "dimensoes": "Tamanho: 14 oz (universal adulto)",
                "prazo_entrega": 6,
                "politica_troca": "Trocas em até 30 dias sem marcas de uso intenso.",
            },
            {
                "nome_produto": "Colchonete Yoga 6 mm",
                "categoria": "esporte_lazer",
                "preco_unitario": 69.90,
                "estoque": 45,
                "imagem": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600",
                "descricao": "Colchonete de yoga com superfície antiderrapante em ambos os lados e alça para transporte. Espessura de 6 mm.",
                "material": "TPE livre de PVC",
                "peso": "950g",
                "dimensoes": "183 × 61 × 0,6 cm",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias sem uso.",
            },
            {
                "nome_produto": "Garrafa Térmica Esportiva 750 ml",
                "categoria": "esporte_lazer",
                "preco_unitario": 59.90,
                "estoque": 70,
                "imagem": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600",
                "descricao": "Garrafa térmica de aço inox com dupla parede a vácuo. Mantém bebidas frias por 24h ou quentes por 12h.",
                "material": "Aço inox 18/8 · Tampa: polipropileno",
                "peso": "300g (vazia)",
                "dimensoes": "Capacidade: 750 ml · Altura: 26 cm",
                "prazo_entrega": 4,
                "politica_troca": "Trocas em até 30 dias com embalagem original.",
            },
        ],
    },

    # ── Natura Beleza · beleza_saude ─────────────────────────────────
    {
        "nome_vendedor": "Natura Beleza",
        "cnpj_vendedor": "55666777000145",
        "email": "loja@naturabeleza.com",
        "senha": "123456",
        "produtos": [
            {
                "nome_produto": "Kit Skincare Hidratante",
                "categoria": "beleza_saude",
                "preco_unitario": 119.90,
                "estoque": 30,
                "imagem": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600",
                "descricao": "Kit com sérum hidratante, tônico facial e hidratante diurno. Rotina completa para pele normal a seca.",
                "material": "Ácido hialurônico, niacinamida, vitamina E",
                "peso": "380g (kit completo)",
                "dimensoes": "3 frascos: 30 ml, 100 ml, 50 ml",
                "prazo_entrega": 5,
                "politica_troca": "Trocas em até 30 dias com produto lacrado.",
            },
            {
                "nome_produto": "Protetor Solar FPS 60",
                "categoria": "beleza_saude",
                "preco_unitario": 49.90,
                "estoque": 80,
                "imagem": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=600",
                "descricao": "Protetor solar facial com FPS 60 e proteção UVA/UVB. Textura fluida de absorção rápida, sem deixar resíduo branco.",
                "material": "Filtros químicos e físicos, extrato de aloe vera",
                "peso": "120g",
                "dimensoes": "Bisnaga 120 ml",
                "prazo_entrega": 4,
                "politica_troca": "Trocas em até 30 dias com produto lacrado.",
            },
            {
                "nome_produto": "Shampoo Nutritivo Argan",
                "categoria": "beleza_saude",
                "preco_unitario": 39.90,
                "estoque": 60,
                "imagem": "https://images.unsplash.com/photo-1585751119414-ef2636f8aede?w=600",
                "descricao": "Shampoo com óleo de argan marroquino para cabelos secos e danificados. Restaura brilho e maciez desde a primeira lavagem.",
                "material": "Óleo de argan, queratina hidrolisada",
                "peso": "350g",
                "dimensoes": "Frasco 300 ml",
                "prazo_entrega": 4,
                "politica_troca": "Trocas em até 30 dias com produto lacrado.",
            },
            {
                "nome_produto": "Perfume Floral Feminino 75 ml",
                "categoria": "beleza_saude",
                "preco_unitario": 159.90,
                "estoque": 20,
                "imagem": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=600",
                "descricao": "Eau de Parfum com notas de peônia, rosa e almíscar branco. Fragrância sofisticada com duração de até 8h.",
                "material": "Álcool, água destilada, composição aromática",
                "peso": "180g (com caixa)",
                "dimensoes": "Frasco 75 ml",
                "prazo_entrega": 6,
                "politica_troca": "Trocas somente com frasco lacrado.",
            },
            {
                "nome_produto": "Creme Hidratante Corporal 400 ml",
                "categoria": "beleza_saude",
                "preco_unitario": 34.90,
                "estoque": 90,
                "imagem": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600",
                "descricao": "Hidratante corporal com manteiga de karité e vitamina E. Absorção rápida, pele macia por até 48h.",
                "material": "Manteiga de karité, vitamina E, pantenol",
                "peso": "430g",
                "dimensoes": "Pote 400 ml",
                "prazo_entrega": 4,
                "politica_troca": "Trocas em até 30 dias com produto lacrado.",
            },
        ],
    },
]


def seed():
    app = create_app()

    with app.app_context():
        if db.engine.dialect.name != "postgresql":
            db.create_all()

        for dados_vendedor in VENDEDORES_TESTE:
            vendedor = VendedorDAO.buscar_por_email(dados_vendedor["email"])
            if vendedor is None:
                vendedor = VendedorDAO.criar(
                    nome_vendedor=dados_vendedor["nome_vendedor"],
                    cnpj_vendedor=dados_vendedor["cnpj_vendedor"],
                    email=dados_vendedor["email"],
                    senha=dados_vendedor["senha"],
                )
                print(f"Vendedor criado: {vendedor.nome_vendedor} ({vendedor.email})")
            else:
                print(f"Vendedor já existia: {vendedor.nome_vendedor} ({vendedor.email})")

            produtos_existentes = {
                p.nome_produto: p
                for p in ProdutoDAO.listar_por_vendedor(vendedor.vendedor_id)
            }
            criados = 0
            for dados_produto in dados_vendedor["produtos"]:
                if dados_produto["nome_produto"] in produtos_existentes:
                    produto_existente = produtos_existentes[dados_produto["nome_produto"]]
                    ProdutoDAO.atualizar(
                        produto_existente.produto_id,
                        imagem=dados_produto.get("imagem"),
                        descricao=dados_produto.get("descricao"),
                        material=dados_produto.get("material"),
                        peso=dados_produto.get("peso"),
                        dimensoes=dados_produto.get("dimensoes"),
                        prazo_entrega=dados_produto.get("prazo_entrega"),
                        politica_troca=dados_produto.get("politica_troca"),
                    )
                    continue
                ProdutoDAO.criar(
                    nome_produto=dados_produto["nome_produto"],
                    categoria=dados_produto["categoria"],
                    preco_unitario=dados_produto["preco_unitario"],
                    vendedor_id=vendedor.vendedor_id,
                    estoque=dados_produto["estoque"],
                    imagem=dados_produto.get("imagem"),
                    descricao=dados_produto.get("descricao"),
                    material=dados_produto.get("material"),
                    peso=dados_produto.get("peso"),
                    dimensoes=dados_produto.get("dimensoes"),
                    prazo_entrega=dados_produto.get("prazo_entrega"),
                    politica_troca=dados_produto.get("politica_troca"),
                )
                criados += 1

            total = len(ProdutoDAO.listar_por_vendedor(vendedor.vendedor_id))
            print(f"  Produtos novos: {criados} | Total da loja: {total}")

        # Cada cliente tem 3 compras em 3 categorias diferentes
        clientes_teste = [
            {
                "cpf": "12345678900", "nome": "Cliente Teste",
                "email": "cliente@teste.com", "compras": [],
            },
            {
                "cpf": "11111111101", "nome": "Ana Lima",
                "email": "ana.lima@teste.com",
                "compras": ["eletronicos", "brinquedos", "esporte_lazer"],
            },
            {
                "cpf": "22222222202", "nome": "Bruno Souza",
                "email": "bruno.souza@teste.com",
                "compras": ["informatica_acessorios", "beleza_saude", "eletronicos"],
            },
            {
                "cpf": "33333333303", "nome": "Carla Mendes",
                "email": "carla.mendes@teste.com",
                "compras": ["brinquedos", "esporte_lazer", "beleza_saude"],
            },
            {
                "cpf": "44444444404", "nome": "Diego Oliveira",
                "email": "diego.oliveira@teste.com",
                "compras": ["esporte_lazer", "eletronicos", "informatica_acessorios"],
            },
            {
                "cpf": "55555555505", "nome": "Fernanda Costa",
                "email": "fernanda.costa@teste.com",
                "compras": ["beleza_saude", "brinquedos", "informatica_acessorios"],
            },
        ]

        try:
            from app.graph.pedidos import registrar_compra as _registrar_grafo
        except Exception:
            _registrar_grafo = None

        print()
        for dados_cliente in clientes_teste:
            cliente = UsuarioDAO.buscar_por_email(dados_cliente["email"])
            if cliente is None:
                cliente = UsuarioDAO.criar(
                    cpf=dados_cliente["cpf"],
                    nome=dados_cliente["nome"],
                    email=dados_cliente["email"],
                    senha="123456",
                )
                print(f"Cliente criado: {cliente.nome} ({cliente.email})")
            else:
                print(f"Cliente já existia: {cliente.nome} ({cliente.email})")

            if not dados_cliente["compras"]:
                continue

            pedidos_existentes = PedidoDAO.listar_por_usuario(cliente.cpf)
            if pedidos_existentes:
                print(f"  Pedidos já existem, pulando criação.")
                continue

            for categoria in dados_cliente["compras"]:
                produtos_cat = ProdutoDAO.listar_por_categoria(categoria, limite=1)
                if not produtos_cat:
                    print(f"  [aviso] Nenhum produto em '{categoria}', pulando.")
                    continue
                produto = produtos_cat[0]
                carrinho = PedidoDAO.buscar_ou_criar_carrinho(cliente.cpf)
                PedidoDAO.adicionar_item(carrinho.pedido_id, produto.produto_id, 1)
                pedido = PedidoDAO.finalizar_pedido(carrinho.pedido_id, "PIX")
                if pedido and _registrar_grafo:
                    try:
                        _registrar_grafo(cliente.cpf, pedido.itens)
                    except Exception as e:
                        print(f"  [grafo] {e}")
                print(f"  Pedido criado: {produto.nome_produto} ({categoria})")

        print("\nSeed concluído. Senha padrão para todos: 123456")
        print("\nClientes:")
        for c in clientes_teste:
            print(f"  - {c['nome']}: {c['email']}")
        print("\nVendedores:")
        for v in VENDEDORES_TESTE:
            print(f"  - {v['nome_vendedor']}: {v['email']}")


if __name__ == "__main__":
    seed()
