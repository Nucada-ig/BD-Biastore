import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.dao import UsuarioDAO, VendedorDAO

_RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_SENHA_MIN = 6


def _validar_cadastro(form):
    """
    Valida os campos do formulário de cadastro.
    Retorna um dict {campo: mensagem} com os erros encontrados.
    """
    erros = {}
    is_vendedor = bool(form.get("is_vendedor"))

    nome = (form.get("nome") or "").strip()
    if not nome:
        erros["nome"] = "Informe um nome."

    email = (form.get("email") or "").strip()
    if not email:
        erros["email"] = "Informe um e-mail."
    elif not _RE_EMAIL.match(email):
        erros["email"] = "E-mail em formato inválido."

    senha = form.get("senha") or ""
    confirmar = form.get("confirmar_senha") or ""
    if not senha:
        erros["senha"] = "Informe uma senha."
    elif len(senha) < _SENHA_MIN:
        erros["senha"] = f"A senha deve ter pelo menos {_SENHA_MIN} caracteres."
    elif senha != confirmar:
        erros["confirmar_senha"] = "As senhas não conferem."

    if is_vendedor:
        cnpj = re.sub(r"\D", "", form.get("cnpj") or "")
        if len(cnpj) != 14:
            erros["cnpj"] = "CNPJ deve ter 14 dígitos numéricos."
    else:
        cpf = re.sub(r"\D", "", form.get("cpf") or "")
        if len(cpf) != 11:
            erros["cpf"] = "CPF deve ter 11 dígitos numéricos."

    return erros

# Blueprint de autenticação: login e cadastro de usuario/vendedor
auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Tela de login do usuario/vendedor.

    Como Usuario e Vendedor sao tabelas totalmente separadas no banco
    (sem nenhuma ligacao entre elas), o login tenta primeiro encontrar
    o e-mail em Usuario; se nao encontrar, tenta em Vendedor.
    """
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = UsuarioDAO.buscar_por_email(email)
        if usuario is not None and usuario.senha == senha:
            session["tipo_sessao"] = "usuario"
            session["usuario_cpf"] = usuario.cpf
            return redirect(url_for("usuario.home"))

        vendedor = VendedorDAO.buscar_por_email(email)
        if vendedor is not None and vendedor.senha == senha:
            session["tipo_sessao"] = "vendedor"
            session["vendedor_id"] = vendedor.vendedor_id
            return redirect(url_for("vendedor.home"))

        return render_template("auth/login.html", erro="E-mail ou senha invalidos.")

    return render_template("auth/login.html")


@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """
    Tela de cadastro de um novo usuario ou vendedor.

    O checkbox "is_vendedor" decide qual tabela recebe o cadastro:
    Usuario (precisa de CPF) ou Vendedor (precisa de CNPJ).
    """
    if request.method == "POST":
        erros = _validar_cadastro(request.form)

        is_vendedor = bool(request.form.get("is_vendedor"))
        email = (request.form.get("email") or "").strip()
        nome = (request.form.get("nome") or "").strip()
        senha = request.form.get("senha") or ""

        # Verificar duplicidade de e-mail só se o formato já passou
        if "email" not in erros:
            if is_vendedor and VendedorDAO.buscar_por_email(email) is not None:
                erros["email"] = "Este e-mail já está cadastrado."
            elif not is_vendedor and UsuarioDAO.buscar_por_email(email) is not None:
                erros["email"] = "Este e-mail já está cadastrado."

        if erros:
            return render_template("auth/cadastro.html", erros=erros, form=request.form)

        if is_vendedor:
            cnpj = re.sub(r"\D", "", request.form.get("cnpj") or "")
            vendedor = VendedorDAO.criar(
                nome_vendedor=nome,
                cnpj_vendedor=cnpj,
                email=email,
                senha=senha,
            )
            session["tipo_sessao"] = "vendedor"
            session["vendedor_id"] = vendedor.vendedor_id
            return redirect(url_for("vendedor.home"))

        cpf = re.sub(r"\D", "", request.form.get("cpf") or "")
        usuario = UsuarioDAO.criar(
            cpf=cpf,
            nome=nome,
            email=email,
            senha=senha,
        )
        session["tipo_sessao"] = "usuario"
        session["usuario_cpf"] = usuario.cpf
        return redirect(url_for("usuario.home"))

    return render_template("auth/cadastro.html", erros={}, form={})


@auth.route("/logout")
def logout():
    """Encerra a sessao do usuario/vendedor logado."""
    session.clear()
    return redirect(url_for("auth.login"))
