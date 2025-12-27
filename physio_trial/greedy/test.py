import inject
import datetime

import armazenamento
from armazenamento.services.base.base_paciente_service import BasePacienteService

from greedy.wrapper import wrapper

@inject.autoparams
def teste_wrapper(paciente_service: BasePacienteService):

    sucesso = wrapper()

    if sucesso:
        print("Heurística funcionou")
        pacientes = paciente_service.listar_pacientes()
        for paciente in pacientes:
            print("Paciente {}".format(paciente.nome))
            print("Fisioterapeuta: {}".format(paciente.fisioterapeuta_responsavel.nome))
            print("Pesquisador: {}".format(paciente.pesquisador_responsavel.nome))
            for sessao in paciente.sessoes_paciente:
                dia_horario = datetime.datetime.combine(sessao.dia, sessao.horario)
                paciente_disp = "disponível" if paciente.restricoes_paciente.esta_disponivel(dia_horario) else "ocupado"
                fisio_disp = "disponível" if paciente.fisioterapeuta_responsavel.restricoes_fisioterapeuta.esta_disponivel(dia_horario) else "ocupado"
                pesquisador_disp = "disponível" if paciente.pesquisador_responsavel.restricoes_pesquisador.esta_disponivel(dia_horario) else "ocupado"
                print("Sessão {}: {} paciente:{} fisio:{} pesquisador:{}".format(sessao.codigo, dia_horario.strftime("%d/%m/%Y %H:%M"), paciente_disp, fisio_disp, pesquisador_disp))
    else:
        print("Heurística falhou")

teste_wrapper()
