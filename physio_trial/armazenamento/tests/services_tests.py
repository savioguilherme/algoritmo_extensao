from datetime import datetime, date, time
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
from dados.paciente import Paciente

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
#     Administrador(id_administrador=None, nome_administrador="Administrador Teste Novo 29", email="test.novo29@usp.br", data_nascimento="2000-09-22", tipo=current_user_types_list.get()[0], login="test.novo29", senha="senha29test", status_administrador=True)
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

servico_usuario.atualizar_fisioterapeuta(
    Fisioterapeuta(id_fisioterapeuta=2, nome_fisioterapeuta="Fisioterapeuta Modificado Again Teste 001", email="fisio.test01@usp.br", data_nascimento=date(2000, 8, 14), tipo=current_user_types_list.get()[1], login="fisio.test001", senha=None, status_fisioterapeuta=True)
)

# modifyied_user = servico_usuario.consultar(13)
# print(f"Fisioterapeuta modificado: {modifyied_user}")

# servico_usuario.atualizar_pesquisador(
#     Pesquisador(id_pesquisador=14, nome_pesquisador="Pesquisador Modificado Again Teste 03", email="pesq.test03@usp.br", data_nascimento="2000-09-22", tipo=4, login="pesq.test03", senha="senha1234567", status_pesquisador=True)
# )

# modifyied_user = servico_usuario.consultar(14)
# print(f"Pesquisador modificado: {modifyied_user}")

servico_usuario.atualizar_adm(
    Administrador(id_administrador=1, nome_administrador="Adm Teste 2", email="admin.02@usp.br", data_nascimento=date(2000, 9, 22), tipo=current_user_types_list.get()[0], login="adm.002", senha="admin123", status_administrador=False)
)

data_array: list[int] = [int(data) for data in "14/05/2000".split("/")]

# novo_fisio: Fisioterapeuta = Fisioterapeuta(id_fisioterapeuta=1, nome_fisioterapeuta='Fisio.04', email="fisio.04@usp.br", data_nascimento=date(data_array[2], data_array[1], data_array[0]), login="fisio.04", senha="fisio123", status_fisioterapeuta=True, tipo=current_user_types_list.get()[1])

# fisio_id = servico_usuario.inserir_fisioterapeuta(fisio=novo_fisio)

# print(f"Novo fisio: {fisio_id}")

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
    {'id_sessao': 1, 'dia_horario': datetime(2025, 12, 22, 9, 1).isoformat(), 'status_agendamento': True},
    {'id_sessao': 2, 'dia_horario': datetime(2025, 12, 29, 9, 29).isoformat(), 'status_agendamento': True}
]

session_service = SessaoService(dal=dal)

session_service.atualizar_sessoes_agendadas(sessoes_atualizadas=sessoes_atualizadas)

paciente_service = PacienteService(dal=dal)

# ------------------------------------------------------
# Dados de teste
# ------------------------------------------------------
fisio = Fisioterapeuta(
    id_fisioterapeuta=3,
    nome_fisioterapeuta="Fisio 2",
    email="fisio2@usp.br",
    data_nascimento=date(1990, 1, 1),
    tipo=3,
    login="fisio2",
    senha="x",
    status_fisioterapeuta=True
)

pesq = Pesquisador(
    id_pesquisador=5,
    nome_pesquisador="Pesquisador 2",
    email="pesq2@usp.br",
    data_nascimento=date(1985, 5, 5),
    tipo=4,
    login="pesq2",
    senha="x",
    status_pesquisador=True
)

# Disponibilidades: dia da semana -> horários
disponibilidades = [
    {"dia": 0, "horarios": ["08:00", "09:00"]},  # segunda
    {"dia": 2, "horarios": ["14:00"]},           # quarta
]

# Restrições (timestamps)
restricoes = [
    "2025-12-22T10:00:00",
    "2025-12-29T15:00:00"
]

paciente = Paciente(
    id_paciente=None,
    nome_paciente="Paciente Teste Proc 09",
    email="paciente.09@usp.br",
    data_nascimento=date(2001, 6, 15),
    pesquisador=pesq,
    fisioterapeuta=fisio
)

paciente.restricoes_paciente.disponibilidade_semanal = [
    {time(8, 0), time(9, 0)},  # seg
    set(),                     # ter
    {time(14, 0)},             # qua
    set(),
    set(),
    set(),
    set()
]

paciente.restricoes_paciente.restricoes = {
    datetime.fromisoformat(r) for r in restricoes
}

# ------------------------------------------------------
# Execução da procedure
# ------------------------------------------------------
# novo_id = paciente_service.cadastrar_paciente(paciente=paciente)
paciente.id_pessoa = 31
_ = paciente_service.atualizar_paciente(paciente=paciente, status_abandono=False, status_conclusao=False)

# print(f"Paciente inserido com ID: {novo_id}")
print(f"Paciente atualizado com ID: {paciente.id_pessoa}")

# ------------------------------------------------------
# Validação pós-inserção
# ------------------------------------------------------
paciente_db = paciente_service.consultar(paciente.id_pessoa)

print("Paciente retornado:")
print(paciente_db)

print("Pesquisador responsável:", paciente_db.pesquisador_responsavel)
print("Fisioterapeuta responsável:", paciente_db.fisioterapeuta_responsavel)

print("Disponibilidades semanais:")
for i, dia in enumerate(paciente_db.restricoes_paciente.disponibilidade_semanal):
    print(f"Dia {i}: {dia}")

print("Restrições:")
for r in paciente_db.restricoes_paciente.restricoes:
    print(r)

paciente_service.atualizar_acompanhamentos_com_sessoes(
    lista_acompanhamentos=acompanhamentos,
    sessoes_atualizadas=sessoes_atualizadas
)

servico_usuario.logout()
