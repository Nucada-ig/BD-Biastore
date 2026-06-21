from functools import wraps
from flask import session, redirect, url_for


def login_obrigatorio(view_func):
    """
    Garante que haja uma sessao ativa (usuario OU vendedor) antes de
    acessar a rota. Caso contrario, redireciona para o login.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "tipo_sessao" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapper


def usuario_obrigatorio(view_func):
    """
    Garante que a sessao ativa seja especificamente de um usuario
    (cliente). Caso contrario, redireciona para a home do vendedor
    (se for o caso) ou para o login.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "tipo_sessao" not in session:
            return redirect(url_for("auth.login"))
        if session.get("tipo_sessao") != "usuario":
            return redirect(url_for("vendedor.home"))
        return view_func(*args, **kwargs)
    return wrapper


def vendedor_obrigatorio(view_func):
    """
    Garante que a sessao ativa seja especificamente de um vendedor.
    Caso contrario, redireciona para a home do usuario comum (se for
    o caso) ou para o login.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "tipo_sessao" not in session:
            return redirect(url_for("auth.login"))
        if session.get("tipo_sessao") != "vendedor":
            return redirect(url_for("usuario.home"))
        return view_func(*args, **kwargs)
    return wrapper
