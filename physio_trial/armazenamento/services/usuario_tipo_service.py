import inject

from armazenamento.services.base.base_usuario_tipo_service import BaseUsuarioTipoService
from armazenamento.dal.data_access_layer import DataAccessLayer

class UsuarioTipoService(BaseUsuarioTipoService):
    @inject.autoparams()
    def __init__(self, dal: DataAccessLayer):
        super().__init__(dal)

    def listar_tipos(self) -> list[int]:
        """
        Lista todos os tipos de usuário identificados numericamente pelo ID de cada tipo.
        """

        results = self._dal.call_function("ufn_usuario_tipos_listar")

        return [row['id_tipo'] for row in results] if results is not None else []
