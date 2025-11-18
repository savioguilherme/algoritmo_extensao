from dados.fisioterapeuta import Fisioterapeuta
from dados.paciente import Paciente
from dados.pesquisador import Pesquisador
from dados.planner import Planner
def greedy_wrapper(func):
    def wrapper(fisios : list[Fisioterapeuta], 
                pesquisadores : list[Pesquisador], 
                pacientes : list[Paciente],
                planner : Planner):
        staff = {}
        for pesquisador in pesquisadores:
            staff[fisio.id_pessoa] = {"Name": pesquisador.nome, 
                                      "Role": "A", 
                                      "Patients": pesquisador.pacientes}
        for fisio in fisios:
            staff[fisio.id_pessoa] = {"Name": fisio.nome, 
                                      "Role": "B", 
                                      "Patients": fisio.pacientes}
        patients = {}
        for paciente in pacientes:
            patients[paciente.id_pessoa] = {"Name": paciente.nome, 
                                            "researcher": paciente.pesquisador_responsavel, 
                                            "physio": paciente.fisioterapeuta_responsavel}
        
        slots = planner.codigo_dos_horarios
        planningHorizon = planner.dias_uteis
        initialDay = planner.dias_uteis[0]

        N_i = {}
        for paciente in pacientes:
            N_i[paciente.id_pessoa] = planner.calcular_disponibilidade(paciente)
        N_pf = {}
        funcionarios = pesquisadores + fisios
        for funcionario in funcionarios:
            N_pf[funcionario.id_pessoa] = planner.calcular_disponibilidade(funcionario)
        
    return wrapper