from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy import Engine, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import SQLAlchemyError

from armazenamento.dal.data_access_layer import DataAccessLayer, ResultType

class SqliteAccessLayer(DataAccessLayer):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def call_function(self, functional_context: str, **kwargs: Any) -> ResultType:

        try:
            with self._engine.connect() as conn:
                result = conn.execute(text(functional_context), kwargs)

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
            raise RuntimeError(f"Database error executing query {functional_context}: {sae}") from sae
        except Exception as e:
            raise RuntimeError(f"Unexpected error executing query {functional_context}: {e}") from e

    def call_procedure(self, procedural_context: str, **kwargs: Any) -> Dict[str, Any]:

        try:
            with self._engine.begin() as conn:
                result = conn.execute(text(procedural_context), kwargs)

                row: Optional[RowMapping] = result.mappings().first() if result.returns_rows else None
                if row is not None:
                    if len(row.keys()) == 1:
                        only_val = next(iter(row.values()))
                        if isinstance(only_val, dict):
                            return only_val
                    return dict(row)

                return {}
        except SQLAlchemyError as sae:
            raise RuntimeError(f"Database error executing DML statement {procedural_context}: {sae}") from sae
        except Exception as e:
            raise RuntimeError(f"Unexpected error executing DML statement {procedural_context}: {e}") from e
