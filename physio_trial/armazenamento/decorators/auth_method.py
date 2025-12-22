from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from armazenamento.context.app_context import require_logged_user

P = ParamSpec("P")
R = TypeVar("R")

def auth_method(method: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator para métodos de serviço.

    Impede execução se não houver usuário logado
    (baseado em contextvars).
    """
    @wraps(method)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        require_logged_user()
        return method(*args, **kwargs)

    return wrapper
