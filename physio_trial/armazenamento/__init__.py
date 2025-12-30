import os
from dotenv import load_dotenv
import inject
from sqlalchemy import create_engine

from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer

from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.services.base.base_usuario_service import BaseUsuarioService
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.base.base_sessao_service import BaseSessaoService
from armazenamento.services.base.base_usuario_tipo_service import BaseUsuarioTipoService

from armazenamento.services.codigo_sessao_service import CodigoSessaoService
from armazenamento.services.paciente_service import PacienteService
from armazenamento.services.sessao_service import SessaoService
from armazenamento.services.usuario_service import UsuarioService
from armazenamento.services.usuario_tipo_service import UsuarioTipoService

load_dotenv()

db_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    db_url,
    pool_pre_ping=True, # evita conexões quebradas
    future=True
)

dal: DataAccessLayer = PostgreAccessLayer(engine)
user_type_service: BaseUsuarioTipoService = UsuarioTipoService(dal)
session_code_service: BaseCodigoSessaoService = CodigoSessaoService(dal)

def ioc_config(binder):
    binder.bind(DataAccessLayer, dal)
    binder.bind(BaseCodigoSessaoService, session_code_service)
    binder.bind(BaseUsuarioTipoService, user_type_service)
    binder.bind(BaseUsuarioService, UsuarioService(dal, user_type_service, session_code_service))
    binder.bind(BasePacienteService, PacienteService(dal))
    binder.bind(BaseSessaoService, SessaoService(dal))

inject.configure(ioc_config)
