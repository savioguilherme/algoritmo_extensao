import inject

from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.dal.data_access_layer import DataAccessLayer

class CodigoSessaoService(BaseCodigoSessaoService):
    @inject.autoparams()
    def __init__(self, dal: DataAccessLayer):
        super().__init__(dal)

    def listar_codigos_sessoes(self) -> list[str]:
        """
        Lista todos os códigos de sessão disponíveis.
        """

        results = self._dal.call_function("ufn_codigos_sessoes_listar")

        return [row['codigo_sessao'] for row in results] if results is not None else []
