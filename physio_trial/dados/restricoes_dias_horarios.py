from __future__ import annotations

from datetime import datetime, time
from typing import List, Set

class RestricoesDiasHorarios:
    """
    Classe que armazena as restrições e disponibilidades
    semanais (por dia da semana e horário).
    """

    def __init__(self) -> None:
        # Índice 0 = segunda, ..., 6 = domingo
        self.disponibilidade_semanal: List[Set[time]] = [set() for _ in range(7)]
        self.restricoes: Set[datetime] = set()

    def adicionar_disponibilidade(self, dia_semana: int, horario: time) -> None:
        self.disponibilidade_semanal[dia_semana % 7].add(horario)

    def remover_disponibilidade(self, dia_semana: int, horario: time) -> None:
        self.disponibilidade_semanal[dia_semana % 7].discard(horario)

    def adicionar_restricao(self, dia_horario: datetime) -> None:
        self.restricoes.add(dia_horario)

    def remover_restricao(self, dia_horario: datetime) -> None:
        self.restricoes.discard(dia_horario)

    def esta_disponivel(self, dia_horario: datetime) -> bool:
        dia_semana: int = dia_horario.weekday()
        horario: time = dia_horario.time()

        return (
            horario in self.disponibilidade_semanal[dia_semana]
            and dia_horario not in self.restricoes
        )

    def get_lista_disponibilidade_semanal(self) -> List[List[time]]:
        return [list(disponibilidade) for disponibilidade in self.disponibilidade_semanal]

    def get_lista_restricoes(self) -> List[datetime]:
        return list(self.restricoes)

    def get_horarios(self) -> Set[time]:
        """
        Retorna o conjunto de todos os horários disponíveis
        independentemente do dia da semana.
        """
        if not self.disponibilidade_semanal:
            return set()

        return set.union(*self.disponibilidade_semanal)
