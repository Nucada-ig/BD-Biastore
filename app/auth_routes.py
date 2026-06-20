from flask import Blueprint, render_template, request, redirect, url_for, session
from app.dao import UsuarioDAO

# Blueprint de autenticação: login e cadastro de usuario/vendedor
auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Tela de login do usuario/vendedor.
    Apos login, redireciona para a home page correta (usuario ou vendedor).
    """
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = UsuarioDAO.buscar_por_email(email)

        if usuario is None or usuario.senha != senha:
            return render_template("auth/login.html", erro="E-mail ou senha invalidos.")

        # Guarda os dados essenciais do usuario logado na sessao
        session["usuario_id"] = usuario.id
        session["is_vendedor"] = usuario.is_vendedor

        if usuario.is_vendedor:
            return redirect(url_for("vendedor.home"))
        return redirect(url_for("usuario.home"))

    return render_template("auth/login.html")


@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """
    Tela de cadastro de um novo usuario/vendedor.
    """
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        is_vendedor = bool(request.form.get("is_vendedor"))

        if UsuarioDAO.buscar_por_email(email) is not None:
            return render_template("auth/cadastro.html", erro="E-mail ja cadastrado.")

        usuario = UsuarioDAO.criar(
            nome=nome,
            email=email,
            senha=senha,
            is_vendedor=is_vendedor,
        )

        session["usuario_id"] = usuario.id
        session["is_vendedor"] = usuario.is_vendedor

        if usuario.is_vendedor:
            return redirect(url_for("vendedor.home"))
        return redirect(url_for("usuario.home"))

    return render_template("auth/cadastro.html")


@auth.route("/logout")
def logout():
    """Encerra a sessao do usuario logado."""
    session.clear()
    return redirect(url_for("auth.login"))
