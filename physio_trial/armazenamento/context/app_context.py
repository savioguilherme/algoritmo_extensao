from contextvars import ContextVar

from sqlalchemy import text
from sqlalchemy.engine import Connection

# SET_AUDIT_USER_SQL = text("SET LOCAL app.user_id = :uid")
SET_AUDIT_USER_SQL = text("SET LOCAL app.user_id = 1")

current_user_id: ContextVar[int | None] = ContextVar("current_user_id", default=None)

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

    # conn.execute(SET_AUDIT_USER_SQL, {"uid": user_id})
    conn.execute(SET_AUDIT_USER_SQL)
