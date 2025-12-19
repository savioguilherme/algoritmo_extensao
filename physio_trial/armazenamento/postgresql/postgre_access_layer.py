from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Engine, text
from sqlalchemy.engine import RowMapping

from armazenamento.dal.data_access_layer import DataAccessLayer

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

ResultType = Union[Dict[str, Any], List[Dict[str, Any]]]

class PostgreAccessLayer(DataAccessLayer):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def call_function(self, function_name: str, **kwargs: Any) -> ResultType:
        fn = _validate_identifier(function_name)

        placeholders = ", ".join(f":{k}" for k in kwargs)
        sql = text(f"SELECT * FROM {fn}({placeholders})")

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

    def call_procedure(self, procedure_name: str, **kwargs: Any) -> Dict[str, Any]:
        pr = _validate_identifier(procedure_name)

        placeholders = ", ".join(f":{k}" for k in kwargs.keys())
        sql = text(f"CALL {pr}({placeholders})")

        # CALL pode retornar 1 linha com OUT params (quando a procedure tem OUT params).
        with self._engine.begin() as conn:
            result = conn.execute(sql, kwargs)

            row: Optional[RowMapping] = result.mappings().first() if result.returns_rows else None
            if row is not None:
                if len(row.keys()) == 1:
                    only_val = next(iter(row.values()))
                    if isinstance(only_val, dict):
                        return only_val
                return dict(row)

            return {}
