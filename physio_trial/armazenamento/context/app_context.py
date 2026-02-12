from contextvars import ContextVar

from sqlalchemy import text
from sqlalchemy.engine import Connection

from datetime import time

current_user_id: ContextVar[int | None] = ContextVar("current_user_id", default=None)
current_user_type: ContextVar[int | None] = ContextVar("current_user_type", default=None)
current_user_types_list: ContextVar[list[int] | None] = ContextVar("current_user_types_list", default=None)
current_session_codes_list: ContextVar[list[str] | None] = ContextVar("current_session_codes_list", default=None)
current_datetimes: ContextVar[list[time] | None] = ContextVar("current_datetimes", default=None)

def require_logged_user() -> int:
    """
    Retorna o ID do usuário logado ou levanta exceção.
    """
    uid = current_user_id.get()

    if uid is None or uid <= 0:
        raise PermissionError("Usuário não autenticado.")

    return uid

def set_audited_user_id(conn: Connection) -> None:
    """
    Define o ID do usuário auditável na conexão do banco de dados.

    Args:
        conn: Conexão do banco de dados.
    """
    user_id = require_logged_user()

    conn.execute(text(f"SET LOCAL app.user_id = {user_id}"))
