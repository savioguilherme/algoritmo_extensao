from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from dados.sessao import Sessao
from greedy.greedy import greedy

import datetime
import itertools

codigos = ["S00","S01","S02","S03","S04","S05","S06","S07","S08","S09","F00","F01"]

def wrapper(
	fisios,
	pesquisadores,
	pacientes,
	dia_inicial : datetime.date,
	intervalo = 500
):

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
	horarios_fisios = [fisio.agenda.get_horarios() for fisio in fisios]
	horarios_pesquisadores = [pesquisador.agenda.get_horarios() for pesquisador in pesquisadores]
	horarios_pacientes = [paciente.agenda.get_horarios() for paciente in pacientes]
	horarios = set.union(*horarios_fisios,*horarios_pesquisadores,*horarios_pacientes)
	slots = {horario : {} for horario in horarios} # slot tem indices datetime.time em vez de string

	# constroi dicionários de disponibilidade

	N_i = {}
	for paciente in pacientes:
		N_i[paciente.id_pessoa] = calcular_disponibilidade(planningHorizon, slots, paciente.agenda)
	N_pf = {}
	for funcionario in itertools.chain(pesquisadores, fisios):
		N_pf[funcionario.id_pessoa] = calcular_disponibilidade(planningHorizon, slots, funcionario.agenda)

	# verifica seções, atualiza disponibilidade e constroi schedule

	schedule = {}
	for paciente in pacientes:
		schedule_paciente = {}
		for codigo in codigos:
			codigo_dia = codigo[0:1] + "D" + codigo[1:]
			codigo_horario = codigo[0:1] + "H" + codigo[1:]
			if codigo in paciente.sessoes.keys():
				sessao = paciente.sessoes[codigo]
				fisio = sessao.fisioterapeuta
				pesquisador = sessao.pesquisador
				dia_horario = sessao.horario
				dia = dia_horario.date()
				slot = dia_horario.time()
				if sessao.horario.date() < dia_inicial:
					schedule_paciente[codigo_dia] = dia
					schedule_paciente[codigo_horario] = slot
				elif fisioterapeuta.agenda.esta_disponivel(dia_horario) and pesquisador.agenda.esta_disponivel(dia_horario) and paciente.agenda.esta_disponivel(dia_horario):
					N_i[paciente.id_pessoa][dia][slot] = False
					N_pf[fisio.id_pessoa][dia][slot] = False
					N_pf[pesquisador.id_pessoa][dia][slot] = False
					schedule_paciente[codigo_dia] = dia
					schedule_paciente[codigo_horario] = slot
				else:
					schedule_paciente[codigo_dia] = None
					schedule_paciente[codigo_horario] = None
			else:
				schedule_paciente[codigo_dia] = None
				schedule_paciente[codigo_horario] = None
		schedule[paciente.id_pessoa] = schedule_paciente

	s, patients, schedule, _ = greedy(dia_inicial, planningHorizon, slots, staff, patients, N_i, N_pf, schedule)

	if not s:
		return False

	# atualiza pacientes com base nos resultados da heurística

	fisio_dict = {fisio.id_pessoa: fisio for fisio in fisios}
	pesquisador_dict = {pesquisador.id_pessoa: pesquisador for pesquisador in pesquisadores}

	for paciente in pacientes:
		patient_id = paciente.id_pessoa
		physio_id = patients[patient_id]["physio"]
		researcher_id = patients[patient_id]["researcher"]
		# como a heurística foi bem sucedida, physio_id e researcher_id não são Null
		paciente.fisioterapeuta = fisio_dict[physio_id]
		paciente.pesquisador = pesquisador_dict[researcher_id]
		for codigo in codigos:
			codigo_dia = codigo[0:1] + "D" + codigo[1:]
			codigo_horario = codigo[0:1] + "H" + codigo[1:]
			patient_schedule = schedule[patient_id]
			dia = patient_schedule[codigo_dia]
			horario = patient_schedule[codigo_horario]
			dia_horario = datetime.datetime.combine(dia,horario)

			pesquisador = None
			fisioterapeuta = None
			if codigo[0] == 'F' or codigo == "S00" or codigo == "S09":
				pesquisador = paciente.pesquisador
			else:
				fisioterapeuta = paciente.fisioterapeuta

			sessao = Sessao(codigo, dia_horario, pesquisador, fisioterapeuta, paciente)
			paciente.sessoes[codigo] = sessao

	return True

def calcular_disponibilidade(dias, horarios, agenda):
	disponibilidade = {}
	for dia in dias:
		disponibilidade_dia = {}
		for horario in horarios:
			esta_disponivel = agenda.esta_disponivel(datetime.datetime.combine(dia,horario))
			disponibilidade_dia[horario] = esta_disponivel
		disponibilidade[dia] = disponibilidade_dia
	return disponibilidade
