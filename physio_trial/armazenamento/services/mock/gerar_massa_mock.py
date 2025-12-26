from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador
from dados.paciente import Paciente
from dados.sessao import Sessao
from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService

from inject import autoparams
from datetime import time

@autoparams()
def gerar_massa_mock(codigo_sessao_service: BaseCodigoSessaoService):
    manha = time(8)
    tarde = time(14)
    noite = time(19)

    # Administradores
    admins = [
        Administrador(1, "Cláudio", "claudio", "senha123", True),
        Administrador(2, "Sérgio", "serginho123", "senhaforte2", True),
        Administrador(3, "Mariana", "mariana.adm", "admin@123", True)
    ]

    # Fisioterapeutas
    fisios = [
        Fisioterapeuta(4, "João", "joao.fisio", "fisio#123", True),
        Fisioterapeuta(5, "Ana", "ana.fisio", "ana@fisio", True),
        Fisioterapeuta(6, "Carlos", "carlos.fisio", "senha@123", True)
    ]

    # Restrições dos Fisioterapeutas
    fisios[0].restricoes_fisioterapeuta.adicionar_disponibilidade(0, manha)
    fisios[0].restricoes_fisioterapeuta.adicionar_disponibilidade(0, tarde)
    fisios[0].restricoes_fisioterapeuta.adicionar_disponibilidade(2, manha)
    fisios[0].restricoes_fisioterapeuta.adicionar_disponibilidade(2, tarde)

    fisios[1].restricoes_fisioterapeuta.adicionar_disponibilidade(1, manha)
    fisios[1].restricoes_fisioterapeuta.adicionar_disponibilidade(1, tarde)
    fisios[1].restricoes_fisioterapeuta.adicionar_disponibilidade(3, manha)
    fisios[1].restricoes_fisioterapeuta.adicionar_disponibilidade(3, tarde)

    fisios[2].restricoes_fisioterapeuta.adicionar_disponibilidade(0, manha)
    fisios[2].restricoes_fisioterapeuta.adicionar_disponibilidade(1, manha)
    fisios[2].restricoes_fisioterapeuta.adicionar_disponibilidade(2, manha)
    fisios[2].restricoes_fisioterapeuta.adicionar_disponibilidade(3, manha)
    fisios[2].restricoes_fisioterapeuta.adicionar_disponibilidade(4, manha)

    # Pesquisadores
    pesquisadores = [
        Pesquisador(7, "Pedro", "pedro.pesq", "pesq@123", True),
        Pesquisador(8, "Beatriz", "beatriz.pesq", "senha#forte", True)
    ]

    # Restrições dos Pesquisadores
    pesquisadores[0].restricoes_pesquisador.adicionar_disponibilidade(0, manha)
    pesquisadores[0].restricoes_pesquisador.adicionar_disponibilidade(1, manha)
    pesquisadores[0].restricoes_pesquisador.adicionar_disponibilidade(4, tarde)

    pesquisadores[1].restricoes_pesquisador.adicionar_disponibilidade(2, manha)
    pesquisadores[1].restricoes_pesquisador.adicionar_disponibilidade(3, tarde)
    pesquisadores[1].restricoes_pesquisador.adicionar_disponibilidade(4, noite)

    # Pacientes
    pacientes = [
        Paciente(9, "Maria"),
        Paciente(10, "José"),
        Paciente(11, "Antônio"),
        Paciente(12, "Fernanda")
    ]

    # Restrições dos pacientes
    pacientes[0].restricoes_paciente.adicionar_disponibilidade(0, manha)
    pacientes[0].restricoes_paciente.adicionar_disponibilidade(1, tarde)

    pacientes[1].restricoes_paciente.adicionar_disponibilidade(2, manha)
    pacientes[1].restricoes_paciente.adicionar_disponibilidade(3, tarde)

    pacientes[2].restricoes_paciente.adicionar_disponibilidade(0, tarde)
    pacientes[2].restricoes_paciente.adicionar_disponibilidade(3, tarde)
    pacientes[2].restricoes_paciente.adicionar_disponibilidade(4, manha)

    pacientes[3].restricoes_paciente.adicionar_disponibilidade(1, manha)
    pacientes[3].restricoes_paciente.adicionar_disponibilidade(4, noite)

    codigos = codigo_sessao_service.listar_codigos_sessoes()
    sessoes = []
    id_sessao = 0
    for paciente in pacientes:
        for codigo in codigos:
            sessao = Sessao(id_sessao, codigo, paciente, None, None, False, False)
            paciente.sessoes_paciente.append(sessao)
            sessoes.append(sessao)
            id_sessao += 1

    return admins, fisios, pesquisadores, pacientes, sessoes
