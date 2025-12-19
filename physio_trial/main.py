import os
from dotenv import load_dotenv
import inject
from sqlalchemy import create_engine
from interfacegrafica.app import App
from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer
from armazenamento.services.base.base_paciente_service import BasePacienteService
from armazenamento.services.paciente_service import PacienteService
from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
from armazenamento.services.codigo_sessao_service import CodigoSessaoService

load_dotenv()

db_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    db_url,
    pool_pre_ping=True, # evita conexões quebradas
    future=True
)

dal: DataAccessLayer = PostgreAccessLayer(engine)

def ioc_config(binder):
    binder.bind(DataAccessLayer, dal)
    binder.bind(BasePacienteService, PacienteService(dal))
    binder.bind(BaseCodigoSessaoService, CodigoSessaoService(dal))
    # ainda preciso configurar outros serviços...

def register_ioc():
    inject.configure(ioc_config)

if __name__ == "__main__":
    register_ioc()
    app = App()
    app.mainloop()
