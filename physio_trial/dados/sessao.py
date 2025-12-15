from dataclasses import dataclass
from datetime import date, time
from typing import TYPE_CHECKING

if TYPE_CHECKING: #evita import circular
    from dados.paciente import Paciente

@dataclass
class Sessao:
    id_sessao: str | None = None
    codigo: str | None = None
    paciente: "Paciente" | None = None
    dia: date | None = None
    horario: time | None = None
    status_agendamento: bool = False
    conclusao: bool = False