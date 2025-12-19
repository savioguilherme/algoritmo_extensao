from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from sqlalchemy import Engine

class DataAccessLayer(ABC):
    """
    Base para camadas de acesso a dados (ex.: PostgreAccessLayer ou SQLiteAccessLayer).

    Convenção:
      - call_function: executa uma function e retorna um dict (ou mapeamento) com o resultado.
      - call_procedure: executa uma procedure e retorna um dict com OUT params.
    """
    def __init__(self, engine: Engine):
        self._engine = engine

    @abstractmethod
    def call_function(self, function_name: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Executa uma FUNCTION no banco.

        Args:
            function_name: nome da function (ex.: 'fn_meu_metodo').
            **kwargs: argumentos nomeados esperados pela function.

        Returns:
            dict com o resultado retornado pela function.
        """
        raise NotImplementedError

    @abstractmethod
    def call_procedure(self, procedure_name: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Executa uma PROCEDURE no banco.

        Args:
            procedure_name: nome da procedure (ex.: 'pr_meu_metodo').
            **kwargs: argumentos nomeados esperados pela procedure.

        Returns:
            dict com os OUT params retornados pela procedure.
        """
        raise NotImplementedError
