import inject
from dados.pessoa import Pessoa
from dados.sessao import Sessao
from dados.restricoes_dias_horarios import RestricoesDiasHorarios
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador
from armazenamento.services.base.base_paciente_service import BasePacienteService
# from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService

class Paciente(Pessoa):
    '''Classe que representa um paciente'''

    @inject.autoparams()
    def __init__(
        self,
        id_paciente,
        nome_paciente,
        pesquisador: Pesquisador,
        fisioterapeuta: Fisioterapeuta,
        status_paciente,
        servico_paciente: BasePacienteService,
        codigos_sessoes: list[str] = None,
        tipo = "paciente"
    ):
        super().__init__(id_paciente, nome_paciente, tipo, status_paciente)

        self.pesquisador_responsavel = pesquisador
        self.fisioterapeuta_responsavel = fisioterapeuta
        self.restricoes_paciente = RestricoesDiasHorarios()
        self.servico_paciente = servico_paciente

        # Modificar aqui?
        self.sessoes_paciente = [
            Sessao(
                id_sessao=None,
                codigo=cod,
                paciente=self,
                dia=None,
                horario=None,
                status_agendamento=False,
                conclusao=False
            )  
            for cod in codigos_sessoes # servico_codigo_sessao.listar_codigos_sessoes() #List Comprehension Python 
        ]
        self.conclusao_pesquisa = False
        self.abandono_pesquisa = False
    
    def restricao_paciente(self, horarios, dias):
        pass

    def verificar_conclusao_pesquisa(self):
        for i in self.sessoes_paciente:
            if i.conclusao is False:
                return
            self.conclusao = True
    
    def cadastrar_abandono_pesquisa(self):
        self.abandono = True
        self.desabilitar_paciente()
        self.servico_paciente.cadastrar_abandono_pesquisa(self.id_pessoa)
    
    # Inútil?
    def desabilitar_paciente(self): 
        self.status_pessoa = False

    def alterar_pesquisador(self, pesquisador: Pesquisador): 
        self.pesquisador_responsavel = pesquisador
        self.servico_paciente.alterar_pesquisador(self.id_pessoa, pesquisador.id_pessoa)

    def alterar_fisioterapeuta(self, fisioterapeuta: Fisioterapeuta): 
        self.fisioterapeuta_responsavel= fisioterapeuta
        self.servico_paciente.alterar_fisioterapeuta(self.id_pessoa, fisioterapeuta.id_pessoa)

    def __repr__(self):
        return f"Paciente(id={self.id_pessoa}, nome='{self.nome}')"
