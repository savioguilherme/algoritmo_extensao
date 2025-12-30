from datetime import datetime
import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from armazenamento.services.codigo_sessao_service import CodigoSessaoService
from armazenamento.postgresql.postgre_access_layer import PostgreAccessLayer
from armazenamento.services.usuario_service import UsuarioService
from armazenamento.services.paciente_service import PacienteService
from armazenamento.context.app_context import current_user_types_list
from armazenamento.dal.data_access_layer import DataAccessLayer
from armazenamento.services.usuario_tipo_service import UsuarioTipoService
from armazenamento.services.sessao_service import SessaoService

from dados.administrador import Administrador
from dados.fisioterapeuta import Fisioterapeuta
from dados.pesquisador import Pesquisador

load_dotenv()

db_url = os.getenv("DATABASE_URL", "")

engine = create_engine(
    db_url,
    pool_pre_ping=True, # evita conexões quebradas
    future=True
)

dal: DataAccessLayer = PostgreAccessLayer(engine)

servico_codigo_sessao = CodigoSessaoService(dal=dal)

servico_tipo_usuario = UsuarioTipoService(dal=dal)

servico_usuario = UsuarioService(dal=dal, user_type_service=servico_tipo_usuario)

id = servico_usuario.login("test04", "senha123")
print(f"Usuário logado com ID: {id}")

servico_usuario.deletar_usuario(1)
print("Usuário deletado com sucesso.")

# current_user_id.set(None)

# new_id = servico_usuario.inserir_adm(
#     Administrador(id_administrador=None, nome_administrador="Administrador Teste 04", email="test04@usp.br", data_nascimento="2000-09-22", tipo=2, login="test04", senha="senha123", status_administrador=True)
# )

# print(f"Administrador inserido com ID: {new_id}")

# new_id = servico_usuario.inserir_fisioterapeuta(
#     Fisioterapeuta(id_fisioterapeuta=None, nome_fisioterapeuta="Fisioterapeuta Teste 03", email="fisio.test03@usp.br", data_nascimento="2000-09-22", tipo=3, login="fisio.test03", senha="senha12345", status_fisioterapeuta=True)
# )

# print(f"Fisioterapeuta inserido com ID: {new_id}")

# new_id = servico_usuario.inserir_pesquisador(
#     Pesquisador(id_pesquisador=None, nome_pesquisador="Pesquisador Teste 03", email="pesq.test03@usp.br", data_nascimento="2000-09-22", tipo=4, login="pesq.test03", senha="senha12345", status_pesquisador=True)
# )

# print(f"Pesquisador inserido com ID: {new_id}")

# servico_usuario.atualizar_fisioterapeuta(
#     Fisioterapeuta(id_fisioterapeuta=13, nome_fisioterapeuta="Fisioterapeuta Modificado Again Teste 03", email="fisio.test03@usp.br", data_nascimento="2000-09-22", tipo=3, login="fisio.test03", senha="senha12345", status_fisioterapeuta=True)
# )

# modifyied_user = servico_usuario.consultar(13)
# print(f"Fisioterapeuta modificado: {modifyied_user}")

# servico_usuario.atualizar_pesquisador(
#     Pesquisador(id_pesquisador=14, nome_pesquisador="Pesquisador Modificado Again Teste 03", email="pesq.test03@usp.br", data_nascimento="2000-09-22", tipo=4, login="pesq.test03", senha="senha1234567", status_pesquisador=True)
# )

# modifyied_user = servico_usuario.consultar(14)
# print(f"Pesquisador modificado: {modifyied_user}")

# servico_usuario.atualizar_adm(
#     Administrador(id_administrador=11, nome_administrador="Adm Modificado Again Teste 03", email="adm.test03@usp.br", data_nascimento="2000-09-22", tipo=2, login="adm.test03", senha="senha1234567", status_administrador=True)
# )

# modifyied_user = servico_usuario.consultar(11)
# print(f"Adm modificado: {modifyied_user}")

# retrieved_id = servico_usuario.login("test04", "senha123")
# print(f"ID do usuário logado: {retrieved_id}")

user_types_list = current_user_types_list.get()

listed_users = servico_usuario.listar_usuarios(user_types_list[1:], False)

for user in listed_users:
    print(user)
    if user.tipo in user_types_list[1:]:
        if isinstance(user, Fisioterapeuta):
            print(f"Restrições do usuário Fisio {user.nome}: {user.restricoes_fisioterapeuta.restricoes}")
            print(f"Disponibilidade semanal do usuário Fisio {user.nome}: {user.restricoes_fisioterapeuta.disponibilidade_semanal}")
        else:
            print(f"Restrições do usuário Pesq {user.nome}: {user.restricoes_pesquisador.restricoes}")
            print(f"Disponibilidade semanal do usuário Pesq {user.nome}: {user.restricoes_pesquisador.disponibilidade_semanal}")

user_type_service = UsuarioTipoService(dal=dal)

user_types_list: list[int] = user_type_service.listar_tipos()

for user_type in user_types_list:
    print(f"Tipo de usuário ID: {user_type}")

fisioterapeuta: Fisioterapeuta = servico_usuario.consultar(3)
pesquisador: Pesquisador = servico_usuario.consultar(5)
admin: Administrador = servico_usuario.consultar(1)

print(f"Fisioterapeuta consultado: {fisioterapeuta}")
print(f"Restrições do Fisioterapeuta {fisioterapeuta.nome}: {fisioterapeuta.restricoes_fisioterapeuta.restricoes}")
print(f"Disponibilidade semanal do Fisioterapeuta {fisioterapeuta.nome}: {fisioterapeuta.restricoes_fisioterapeuta.disponibilidade_semanal}")

print(f"Pesquisador consultado: {pesquisador}")
print(f"Restrições do Pesquisador {pesquisador.nome}: {pesquisador.restricoes_pesquisador.restricoes}")
print(f"Disponibilidade semanal do Pesquisador {pesquisador.nome}: {pesquisador.restricoes_pesquisador.disponibilidade_semanal}")

print(f"Administrador consultado: {admin}")

paciente_service = PacienteService(dal=dal)

listed_patients = paciente_service.listar_pacientes(False)

for patient in listed_patients:
    print(patient)
    print(f"Restrições do paciente {patient.nome}: {patient.restricoes_paciente.restricoes}")
    print(f"Disponibilidade semanal do paciente {patient.nome}: {patient.restricoes_paciente.disponibilidade_semanal}")

patient = paciente_service.consultar(7)

print(f"Paciente consultado: {patient}")
print(f"Restrições do paciente {patient.nome}: {patient.restricoes_paciente.restricoes}")
print(f"Disponibilidade semanal do paciente {patient.nome}: {patient.restricoes_paciente.disponibilidade_semanal}")
print(f"Pesquisador responsável: {patient.pesquisador_responsavel}")
print(f"Fisioterapeuta responsável: {patient.fisioterapeuta_responsavel}")

for cod in servico_codigo_sessao.listar_codigos_sessoes():
    print(cod)

acompanhamentos: list[dict[str, int]] = [
        {
            'id_paciente': 7,
            'id_fisioterapeuta': 13,
            'id_pesquisador': 5
        },
        {
            'id_paciente': 6,
            'id_fisioterapeuta': 2,
            'id_pesquisador': 14
        },
        {
            'id_paciente': 8,
            'id_fisioterapeuta': 3,
            'id_pesquisador': 4
        }
    ]

paciente_service.atualizar_acompanhamentos(lista_acompanhamentos=acompanhamentos)

sessoes_atualizadas: list[dict[str, int | datetime]] = [
    {'id_sessao': 1, 'dia_horario': datetime(2025, 12, 22, 9, 1).isoformat()},
    {'id_sessao': 2, 'dia_horario': datetime(2025, 12, 29, 9, 29).isoformat()}
]

session_service = SessaoService(dal=dal)

session_service.atualizar_sessoes_agendadas(sessoes_atualizadas=sessoes_atualizadas)

servico_usuario.logout()
