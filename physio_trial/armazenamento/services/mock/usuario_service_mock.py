import bcrypt

from armazenamento.context.app_context import current_user_id
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.dal.data_access_layer import DataAccessLayer

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

class UsuarioServiceMock(BaseUsuarioService):
    def __init__(
        self,
        dal: DataAccessLayer,
        administradores: list[Administrador],
        fisioterapeutas: list[Fisioterapeuta],
        pesquisadores: list[Pesquisador],
    ):
        super().__init__(dal)
        self.usuarios = [administradores, fisioterapeutas, pesquisadores]

    def login(self, username: str, password: str) -> int | None:
        pass

    def logout(self) -> None:
        pass

    def listar_usuarios(self, lista_tipos: list[int]) -> list[Administrador | Fisioterapeuta | Pesquisador]:
        lista = []
        for tipo in lista_tipos:
            lista += self.usuarios[tipo]
        return lista

    def consultar_adm(self, id_adm: int):
        pass

    def inserir_adm(self, adm: Administrador) -> int:
        pass

    def atualizar_adm(self, adm: Administrador) -> None:
        pass

    def consultar_fisioterapeuta(self, id_fisio: int):
        pass

    def inserir_fisioterapeuta(self, fisio: Fisioterapeuta) -> int:
        pass

    def atualizar_fisioterapeuta(self, fisio: Fisioterapeuta) -> None:
        pass

    def consultar_pesquisador(self, id_pesq: int):
        pass

    def inserir_pesquisador(self, pesq: Pesquisador) -> int:
        pass

    def atualizar_pesquisador(self, pesq: Pesquisador) -> None:
        pass

    def deletar_usuario(self, id_usuario_desativado: int) -> None:
        pass
