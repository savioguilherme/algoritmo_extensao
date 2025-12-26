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

from armazenamento.services.codigo_sessao_service import CodigoSessaoService
from armazenamento.services.mock.usuario_service_mock import UsuarioServiceMock
from armazenamento.services.mock.paciente_service_mock import PacienteServiceMock
from armazenamento.services.mock.sessao_service_mock import SessaoServiceMock
from armazenamento.services.mock.gerar_massa_mock import gerar_massa_mock

# inicialização do armazenamento

load_dotenv()

db_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    db_url,
    pool_pre_ping=True, # evita conexões quebradas
    future=True
)

dal = PostgreAccessLayer(engine)

def ioc_config(binder):
    codigo_sessao_service = CodigoSessaoService(dal)
    admins, fisios, pesquisadores, pacientes, sessoes = gerar_massa_mock(codigo_sessao_service)
    binder.bind(DataAccessLayer, dal)
    binder.bind(BaseCodigoSessaoService, codigo_sessao_service)
    binder.bind(BaseUsuarioService, UsuarioServiceMock(dal,admins,fisios,pesquisadores))
    binder.bind(BasePacienteService, PacienteServiceMock(dal,codigo_sessao_service,pacientes,fisios,pesquisadores))
    binder.bind(BaseSessaoService, SessaoServiceMock(dal,sessoes))

inject.configure(ioc_config)
