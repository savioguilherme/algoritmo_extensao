import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from armazenamento.services.codigo_sessao_service import CodigoSessaoService
from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer
from armazenamento.services.usuario_service import UsuarioService
from armazenamento.context.app_context import current_user_id

# from dados.administrador import Administrador

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

# new_id = servico_usuario.inserir_adm(
#     Administrador(id_administrador=None, nome_administrador="Administrador Teste 04", email="test04@usp.br", data_nascimento="2000-09-22", tipo=2, login="test04", senha="senha123", status_administrador=True)
# )

# print(f"Administrador inserido com ID: {new_id}")

retrieved_id = servico_usuario.login("test04", "senha123")
print(f"ID do usuário logado: {retrieved_id}")

servico_usuario.logout()
