import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from armazenamento.services.codigo_sessao_service import CodigoSessaoService
from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer
from armazenamento.services.usuario_service import UsuarioService
from armazenamento.context.app_context import current_user_id

load_dotenv()

db_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    db_url,
    pool_pre_ping=True, # evita conexões quebradas
    future=True
)

servico_codigo_sessao = CodigoSessaoService(PostgreAccessLayer(engine))

for cod in servico_codigo_sessao.listar_codigos_sessoes():
    print(cod)

servico_usuario = UsuarioService(PostgreAccessLayer(engine))

current_user_id.set(1)

servico_usuario.deletar_usuario(1)
print("Usuário deletado com sucesso.")

current_user_id.set(None)
