from functools import wraps
from flask import session, redirect, url_for


def login_obrigatorio(view_func):
    """
    Garante que o usuario esteja logado (sessao com usuario_id) antes
    de acessar a rota. Caso contrario, redireciona para o login.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapper


def vendedor_obrigatorio(view_func):
    """
    Garante que o usuario logado seja um vendedor antes de acessar a rota.
    Caso contrario, redireciona para a home do usuario comum.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        if not session.get("is_vendedor"):
            return redirect(url_for("usuario.home"))
        return view_func(*args, **kwargs)
    return wrapper
