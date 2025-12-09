from dataclasses import dataclass
from datetime import date, time

@dataclass
class Sessao:

    '''Classe que representa uma das 11 sessoes'''

    codigo: str
    dia: date | None = None
    horario: time | None = None
    status: bool = False