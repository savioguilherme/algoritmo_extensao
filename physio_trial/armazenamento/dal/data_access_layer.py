from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from sqlalchemy import Engine

ResultType = Union[Dict[str, Any], List[Dict[str, Any]]]

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
    def call_function(self, functional_context: str, **kwargs: Any) -> ResultType:
        """
        Executa uma FUNCTION no banco ou algum script de consulta (query).

        Args:
            functional_context: nome da function ou script sql funcional de query
                (ex.: 'fn_meu_metodo' ou 'SELECT * FROM paciente').
            **kwargs: argumentos nomeados esperados pela function.

        Returns:
            dict com o resultado retornado pela function ou query.
        """
        raise NotImplementedError

    @abstractmethod
    def call_procedure(self, procedural_context: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Executa uma PROCEDURE no banco ou algum script envolvendo operações DML.

        Args:
            procedural_context: nome da procedure ou sql script de DML
                (ex.: 'pr_meu_metodo' ou 'INSERT INTO ...').
            **kwargs: argumentos nomeados esperados pela procedure.

        Returns:
            dict com os OUT params retornados pela procedure ou statement.
        """
        raise NotImplementedError
