from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador
from greedy.greedy import greedy

from armazenamento.context.app_context import current_user_types_list
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.decorators.auth_method import auth_method

import inject
import datetime

@auth_method
@inject.params(usuario_service = BaseUsuarioService, paciente_service = BasePacienteService)
def wrapper(
    usuario_service: BaseUsuarioService,
    paciente_service: BasePacienteService,
    dia_inicial: datetime.date = datetime.date.today(),
    intervalo: int = 500,
) -> bool:
    usuario_tipos: list[int] = current_user_types_list.get() or []
    if not usuario_tipos or usuario_tipos is None:
        raise PermissionError("Tipos de usuário não encontrados no contexto da aplicação.")

    # recupera dados do bd
    usuarios = usuario_service.listar_usuarios(lista_tipos=[usuario_tipos[1], usuario_tipos[2]], apenas_ativos=True)
    fisios = [usuario for usuario in usuarios if isinstance(usuario, Fisioterapeuta) and usuario.tipo == usuario_tipos[1]]
    pesquisadores = [usuario for usuario in usuarios if isinstance(usuario, Pesquisador) and usuario.tipo == usuario_tipos[2]]
    pacientes = [paciente for paciente in paciente_service.listar_pacientes(apenas_ativos=True) if paciente.sessoes_paciente is not None and len(paciente.sessoes_paciente) == 12]

    # constroi staff e patients

    staff = {}
    for pesquisador in pesquisadores:
        staff[pesquisador.id_pessoa] = { "Role": "A" }
    for fisio in fisios:
        staff[fisio.id_pessoa] = { "Role": "B" }
    patients = {}
    for paciente in pacientes:
        patients[paciente.id_pessoa] = {
            "Name": paciente.nome,
            "researcher": paciente.pesquisador_responsavel.id_pessoa if paciente.pesquisador_responsavel else None,
            "physio": paciente.fisioterapeuta_responsavel.id_pessoa if paciente.fisioterapeuta_responsavel else None
        }

    print("Wrapper interval", intervalo) #dbg

    planningHorizon = [dia_inicial + datetime.timedelta(days=delta) for delta in range(intervalo)]
    horarios_fisios = [fisio.restricoes_fisioterapeuta.get_horarios() for fisio in fisios]
    horarios_pesquisadores = [pesquisador.restricoes_pesquisador.get_horarios() for pesquisador in pesquisadores]
    horarios_pacientes = [paciente.restricoes_paciente.get_horarios() for paciente in pacientes]
    horarios = set.union(*horarios_fisios,*horarios_pesquisadores,*horarios_pacientes)
    slots = {horario : {} for horario in horarios} # slot tem indices datetime.time em vez de string

    # constroi dicionários de disponibilidade

    N_i = {}
    for paciente in pacientes:
        N_i[paciente.id_pessoa] = calcular_disponibilidade(planningHorizon, slots, paciente.restricoes_paciente)
    N_pf = {}
    # TODO: duplicação de código por nomes diferentes para o campo de restrições
    for pesquisador in pesquisadores:
        N_pf[pesquisador.id_pessoa] = calcular_disponibilidade(planningHorizon, slots, pesquisador.restricoes_pesquisador)
    for fisio in fisios:
        N_pf[fisio.id_pessoa] = calcular_disponibilidade(planningHorizon, slots, fisio.restricoes_fisioterapeuta)

    # verifica seções, atualiza disponibilidade e constroi schedule

    schedule = {}
    for paciente in pacientes:
        schedule_paciente = {}
        # assume que não existem duas seções com o mesmo código
        for sessao in paciente.sessoes_paciente:
            codigo = sessao.codigo
            codigo_dia = codigo[0:1] + "D" + codigo[1:]
            codigo_horario = codigo[0:1] + "H" + codigo[1:]
            # aqui não tem problema definir tanto o fisioterapeuta quanto o pesquisador, visto que a heurística é inteligente o suficiente para escolher de acordo com o código da seção
            fisio = sessao.paciente.fisioterapeuta_responsavel
            pesquisador = sessao.paciente.pesquisador_responsavel
            schedule_paciente[codigo_dia] = None
            schedule_paciente[codigo_horario] = None
            if sessao.status_agendamento:
                dia = as_date(sessao.dia)
                slot = as_time(sessao.horario)
                if dia_inicial <= dia:
                    N_i[paciente.id_pessoa][dia][slot] = False
                    N_pf[fisio.id_pessoa][dia][slot] = False
                    N_pf[pesquisador.id_pessoa][dia][slot] = False
                schedule_paciente[codigo_dia] = dia
                schedule_paciente[codigo_horario] = slot
        schedule[paciente.id_pessoa] = schedule_paciente

    patients, schedule = greedy(dia_inicial, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)

    # atualiza pacientes com base nos resultados da heurística
    acompanhamentos: list[dict[str, int]] = [
        {
            'id_paciente': paciente.id_pessoa,
            'id_fisioterapeuta': patients[paciente.id_pessoa]['physio'],
            'id_pesquisador': patients[paciente.id_pessoa]['researcher']
        }
        for paciente in pacientes
        if
            paciente.fisioterapeuta_responsavel.id_pessoa != patients[paciente.id_pessoa]['physio'] or
            paciente.pesquisador_responsavel.id_pessoa != patients[paciente.id_pessoa]['researcher']
    ]
    
    sessoes_atualizadas: list[dict[str, int | str | bool]] = []

    for paciente in pacientes:
        for sessao in paciente.sessoes_paciente:
            if sessao.conclusao or sessao.status_agendamento:
                continue # ignora sessões concluídas ou já agendadas
            codigo = sessao.codigo
            codigo_dia = codigo[0:1] + "D" + codigo[1:]
            codigo_horario = codigo[0:1] + "H" + codigo[1:]
            patient_schedule = schedule[paciente.id_pessoa]
            dia = patient_schedule[codigo_dia]
            horario = patient_schedule[codigo_horario]
            if dia == sessao.dia and horario == sessao.horario:
                continue
            if dia is None or horario is None:
                continue
            dia_horario = datetime.datetime.combine(dia,horario)
            sessao.status_agendamento = True
            sessoes_atualizadas.append({
                'id_sessao': sessao.id_sessao,
                'dia_horario': dia_horario.isoformat(),
                'status_agendamento': sessao.status_agendamento
            })

    return paciente_service.atualizar_acompanhamentos_com_sessoes(
        lista_acompanhamentos=acompanhamentos,
        sessoes_atualizadas=sessoes_atualizadas
    )

def calcular_disponibilidade(dias, horarios, restricoes):
    disponibilidade = {}
    for dia in dias:
        disponibilidade_dia = {}
        for horario in horarios:
            esta_disponivel = restricoes.esta_disponivel(datetime.datetime.combine(dia,horario))
            disponibilidade_dia[horario] = esta_disponivel
        disponibilidade[dia] = disponibilidade_dia
    return disponibilidade
