# armazenamento/db.py
import os
from typing import Optional
from sqlalchemy import create_engine

from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer
from armazenamento.dal.data_access_layer import DataAccessLayer

def get_db_accessor(env: str, stack: Optional[str]) -> DataAccessLayer:
    db_url = os.getenv(env, "")

    engine = create_engine(
        db_url,
        pool_pre_ping=True, # evita conexões quebradas
        future=True
    )

    match stack:
        case "postgresql":
            return PostgreAccessLayer(engine)
        case _:
            return DataAccessLayer(engine)  # ou lançar erro
