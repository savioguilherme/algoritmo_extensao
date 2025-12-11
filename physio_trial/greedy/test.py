from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from greedy.wrapper import wrapper

import datetime

from dados.agenda import Agenda

def test():
    fisioterapeuta = Fisioterapeuta(1, None, None, None)
    pesquisador = Pesquisador(2, None, None, None)
    paciente = Paciente(3, None, None, None, None, None)

    segunda = 0
    quarta = 2
    manha = datetime.time(10)

    fisioterapeuta.agenda.adicionar_disponibilidade(segunda,manha)
    fisioterapeuta.agenda.adicionar_disponibilidade(quarta,manha)
    fisioterapeuta.agenda.adicionar_restricao(datetime.datetime(2025,12,24,10))
    pesquisador.agenda.adicionar_disponibilidade(segunda,manha)
    pesquisador.agenda.adicionar_disponibilidade(quarta,manha)
    paciente.agenda.adicionar_disponibilidade(segunda,manha)
    paciente.agenda.adicionar_disponibilidade(quarta,manha)

    sucesso = wrapper([fisioterapeuta],[pesquisador],[paciente],datetime.date(2025,11,25))

    print("\nheurística funcionou" if sucesso else "heurística falhou")
    if(sucesso):
        print("fisioterapeuta:", paciente.fisioterapeuta.id_pessoa)
        print("pesquisador:", paciente.pesquisador.id_pessoa)
        print("secoes:")
        for codigo in paciente.sessoes:
            print("{}: {}".format(codigo,paciente.sessoes[codigo].horario))