from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from dados.sessao import Sessao
from greedy.greedy import greedy

from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_sessao_service import BaseSessaoService

from inject import autoparams
import datetime
import itertools

@autoparams
def wrapper(
    codigo_sessao_service: BaseCodigoSessaoService,
    usuario_service: BaseUsuarioService,
    paciente_service: BasePacienteService,
    sessao_service: BaseSessaoService,
    dia_inicial = datetime.date.today(),
    intervalo = 500,
):

    # recupera dados do bd

    fisios = usuario_service.listar_usuarios([1])
    pesquisadores = usuario_service.listar_usuarios([2])
    pacientes_bruto = paciente_service.listar_pacientes()
    pacientes = [paciente for paciente in pacientes_bruto if paciente.status_pessoa and not paciente.conclusao_pesquisa and not paciente.abandono_pesquisa]

    # constroi staff e patients

    staff = {}
    for pesquisador in pesquisadores:
        staff[pesquisador.id_pessoa] = { "Role": "A" }
    for fisio in fisios:
        staff[fisio.id_pessoa] = { "Role": "B" }
    patients = {}
    for paciente in pacientes:
        patients[paciente.id_pessoa] = {
            "researcher": paciente.pesquisador_responsavel.id_pessoa if paciente.pesquisador_responsavel else None, 
            "physio": paciente.fisioterapeuta_responsavel.id_pessoa if paciente.fisioterapeuta_responsavel else None, 
        }

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
                dia_horario = datetime.datetime.combine(sessao.dia, sessao.horario)
                dia = sessao.dia
                slot = sessao.horario
                if sessao.conclusao or sessao.dia < dia_inicial:
                    schedule_paciente[codigo_dia] = dia
                    schedule_paciente[codigo_horario] = slot
                elif fisioterapeuta.restricoes_fisioterapeuta.esta_disponivel(dia_horario) and pesquisador.restricoes_pesquisador.esta_disponivel(dia_horario) and paciente.restricoes_paciente.esta_disponivel(dia_horario):
                    N_i[paciente.id_pessoa][dia][slot] = False
                    N_pf[fisio.id_pessoa][dia][slot] = False
                    N_pf[pesquisador.id_pessoa][dia][slot] = False
                    schedule_paciente[codigo_dia] = dia
                    schedule_paciente[codigo_horario] = slot
        schedule[paciente.id_pessoa] = schedule_paciente

    s, patients, schedule, _ = greedy(dia_inicial, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)

    if not s:
        return False

    # atualiza pacientes com base nos resultados da heurística

    for paciente in pacientes:
        patient_id = paciente.id_pessoa
        physio_id = patients[patient_id]["physio"]
        researcher_id = patients[patient_id]["researcher"]
        # como a heurística foi bem sucedida, physio_id e researcher_id não são Null
        paciente_service.alterar_fisioterapeuta(patient_id,physio_id)
        paciente_service.alterar_pesquisador(patient_id,researcher_id)
        for sessao in paciente.sessoes_paciente:
            if sessao.conclusao:
                continue
            codigo = sessao.codigo
            codigo_dia = codigo[0:1] + "D" + codigo[1:]
            codigo_horario = codigo[0:1] + "H" + codigo[1:]
            patient_schedule = schedule[patient_id]
            dia = patient_schedule[codigo_dia]
            horario = patient_schedule[codigo_horario]
            dia_horario = datetime.datetime.combine(dia,horario)
            sessao_service.agendar_dia_horario(sessao.id_sessao,dia_horario)

    return True

def calcular_disponibilidade(dias, horarios, restricoes):
    disponibilidade = {}
    for dia in dias:
        disponibilidade_dia = {}
        for horario in horarios:
            esta_disponivel = restricoes.esta_disponivel(datetime.datetime.combine(dia,horario))
            disponibilidade_dia[horario] = esta_disponivel
        disponibilidade[dia] = disponibilidade_dia
    return disponibilidade
