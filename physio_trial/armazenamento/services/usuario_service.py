import inject

from armazenamento.services.base.base_usuario_service import BaseUsuarioService

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class UsuarioService(BaseUsuarioService):

    @inject.autoparams()
    def __init__(self, dal):
        super().__init__(dal)

    def listar_usuarios(self, lista_tipos: list[int]) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        return self._dal.usuario_dal.listar_usuarios(lista_tipos)

    def consultar_adm(self, id_adm: int):
        return self._dal.usuario_dal.consultar_adm(id_adm)

    def inserir_adm(self, adm: Administrador) -> int:
        return self._dal.usuario_dal.inserir_adm(adm)

    def atualizar_adm(self, adm: Administrador) -> None:
        self._dal.usuario_dal.atualizar_adm(adm)

    def consultar_fisioterapeuta(self, id_fisio: int):
        return self._dal.usuario_dal.consultar_fisioterapeuta(id_fisio)

    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        return self._dal.usuario_dal.inserir_fisioterapeuta(fisio)

    def atualizar_fisioterapeuta(self, fisio: Fisioterapeuta) -> None:
        self._dal.usuario_dal.atualizar_fisioterapeuta(fisio)

    def consultar_pesquisador(self, id_pesq: int):
        return self._dal.usuario_dal.consultar_pesquisador(id_pesq)

    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        return self._dal.usuario_dal.inserir_pesquisador(pesq)

    def atualizar_pesquisador(self, pesq: Pesquisador) -> None:
        self._dal.call_procedure()

    def deletar_usuario(self, id_usuario_desativado: int) -> None:
        return self._dal.call_procedure(
            "usp_usuario_deletar",
            p_id_usuario_desativado=id_usuario_desativado
        )
