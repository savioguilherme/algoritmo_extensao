from dataclasses import dataclass
from datetime import date, time

@dataclass
class Sessao:
    '''Classe que representa uma das 11 sessoes'''
    
    id_sessao: str | None = None
    codigo: str | None = None
    dia: date | None = None
    horario: time | None = None
    status_agendamento: bool = False
    conclusao: bool = False