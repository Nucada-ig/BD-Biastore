from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.auth_utils import usuario_obrigatorio
from app.dao import UsuarioDAO, ProdutoDAO, PedidoDAO, EnderecoDAO
from app.graph import categorias_preferidas

usuario = Blueprint("usuario", __name__, url_prefix="/usuario")


@usuario.route("/home")
@usuario_obrigatorio
def home():
    cpf = session["usuario_cpf"]
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = 8

    try:
        tops = categorias_preferidas(cpf, limite=3)
    except Exception:
        tops = []

    produtos_destaque = ProdutoDAO.listar_por_categoria(tops[0], limite=10) if tops else []
    produtos_mix = ProdutoDAO.listar_mix_categorias(tops, limite_por_categoria=5) if tops else []
    produtos_descoberta = ProdutoDAO.listar_mix_aleatorio(n_categorias=3, limite_por_categoria=5) if not tops else []
    produtos, total = ProdutoDAO.listar_paginado(pagina, por_pagina)
    total_paginas = max(1, -(-total // por_pagina))  # ceil division

    return render_template(
        "usuario/home.html",
        produtos=produtos,
        produtos_destaque=produtos_destaque,
        produtos_mix=produtos_mix,
        produtos_descoberta=produtos_descoberta,
        categoria_destaque=tops[0] if tops else None,
        pagina=pagina,
        total_paginas=total_paginas,
    )


@usuario.route("/perfil", methods=["GET", "POST"])
@usuario_obrigatorio
def perfil():
    usuario_logado = UsuarioDAO.buscar_por_cpf(session["usuario_cpf"])
    aba = request.args.get("aba", "perfil")

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "editar_perfil":
            email = request.form.get("email", "").strip()
            senha_atual = request.form.get("senha_atual", "")
            nova_senha = request.form.get("nova_senha", "")

            if email and email != usuario_logado.email:
                existente = UsuarioDAO.buscar_por_email(email)
                if existente and existente.cpf != usuario_logado.cpf:
                    flash("Este e-mail já está em uso.", "erro")
                    return redirect(url_for("usuario.perfil", aba="perfil"))
                UsuarioDAO.atualizar(usuario_logado.cpf, email=email)

            if nova_senha:
                if senha_atual != usuario_logado.senha:
                    flash("Senha atual incorreta.", "erro")
                    return redirect(url_for("usuario.perfil", aba="perfil"))
                UsuarioDAO.atualizar(usuario_logado.cpf, senha=nova_senha)

            flash("Dados atualizados com sucesso.", "sucesso")
            return redirect(url_for("usuario.perfil", aba="perfil"))

        if acao == "adicionar_endereco":
            cep = request.form.get("cep", "").replace("-", "").strip()
            numero = request.form.get("numero", "").strip()
            complemento = request.form.get("complemento", "").strip()
            bairro = request.form.get("bairro", "").strip()
            cidade = request.form.get("cidade", "").strip()
            estado = request.form.get("estado", "").strip()

            if not (cep and numero and bairro and cidade and estado):
                flash("Preencha todos os campos obrigatórios do endereço.", "erro")
                return redirect(url_for("usuario.perfil", aba="enderecos"))

            EnderecoDAO.criar(
                cpf=usuario_logado.cpf,
                cep=cep,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
            )
            flash("Endereço adicionado.", "sucesso")
            return redirect(url_for("usuario.perfil", aba="enderecos"))

    pedidos = PedidoDAO.listar_por_usuario(session["usuario_cpf"])
    enderecos = EnderecoDAO.listar_por_usuario(session["usuario_cpf"])

    return render_template(
        "usuario/perfil.html",
        usuario=usuario_logado,
        pedidos=pedidos,
        enderecos=enderecos,
        aba=aba,
    )


@usuario.route("/perfil/endereco/<int:endereco_id>/remover", methods=["POST"])
@usuario_obrigatorio
def remover_endereco(endereco_id):
    removido = EnderecoDAO.remover(endereco_id, session["usuario_cpf"])
    if not removido:
        flash("Endereço não encontrado.", "erro")
    else:
        flash("Endereço removido.", "sucesso")
    return redirect(url_for("usuario.perfil", aba="enderecos"))


# Mantida por compatibilidade com links existentes — redireciona para a aba
@usuario.route("/pedidos")
@usuario_obrigatorio
def pedidos():
    return redirect(url_for("usuario.perfil", aba="pedidos"))
