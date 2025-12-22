from __future__ import annotations

import re
from typing import Any, Dict, Optional

from sqlalchemy import Engine, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import SQLAlchemyError

from armazenamento.dal.data_access_layer import DataAccessLayer, ResultType
from armazenamento.context.app_context import set_audited_user_id

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")

def _validate_identifier(name: str) -> str:
    """
    Permite nomes do tipo:
      - fn_minhas_coisas
      - public.fn_minhas_coisas
      - schema_x.proc_y

    Evita SQL injection via nome de function/procedure.
    """
    if not _IDENTIFIER_RE.match(name):
        raise ValueError(f"Invalid SQL identifier: {name!r}")
    return name

class PostgreAccessLayer(DataAccessLayer):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def call_function(self, functional_context: str, **kwargs: Any) -> ResultType:
        fn = _validate_identifier(functional_context)

        placeholders = ", ".join(f":{k}" for k in kwargs)
        sql = text(f"SELECT * FROM {fn}({placeholders})")

        try:
            with self._engine.connect() as conn:
                result = conn.execute(sql, kwargs)

                rows = result.mappings().all()

                # 1) Nenhuma linha retornada
                if not rows:
                    return {}

                # 2) Uma única linha
                if len(rows) == 1:
                    row = rows[0]

                    # Caso especial: única coluna
                    if len(row) == 1:
                        only_val = next(iter(row.values()))
                        if isinstance(only_val, dict):
                            return only_val

                    return dict(row)

                # 3) Várias linhas (RETURNS TABLE / SETOF)
                return [dict(r) for r in rows]
        except SQLAlchemyError as sae:
            raise RuntimeError(f"Database error executing function {fn}: {sae}") from sae
        except Exception as e:
            raise RuntimeError(f"Unexpected error executing function {fn}: {e}") from e

    def call_procedure(self, procedural_context: str, **kwargs: Any) -> Dict[str, Any]:
        pr = _validate_identifier(procedural_context)

        placeholders = ", ".join(f":{k}" for k in kwargs.keys())
        sql = text(f"CALL {pr}({placeholders})")

        # CALL pode retornar 1 linha com OUT params (quando a procedure tem OUT params).
        try:
            with self._engine.begin() as conn:
                set_audited_user_id(conn)
                result = conn.execute(sql, kwargs)

                row: Optional[RowMapping] = result.mappings().first() if result.returns_rows else None
                if row is not None:
                    if len(row.keys()) == 1:
                        only_val = next(iter(row.values()))
                        if isinstance(only_val, dict):
                            return only_val
                    return dict(row)

                return {}
        except SQLAlchemyError as sae:
            raise RuntimeError(f"Database error executing procedure {pr}: {sae}") from sae
        except Exception as e:
            raise RuntimeError(f"Unexpected error executing procedure {pr}: {e}") from e
