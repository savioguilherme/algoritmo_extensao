# from psycopg.types.json import Jsonb
# from inject import autoparams
# from datetime import datetime, date, time
# 
# from armazenamento.context.app_context import current_user_id, current_user_type, current_user_types_list, current_session_codes_list
# from armazenamento.services.base.base_usuario_service import BaseUsuarioService
# from armazenamento.services.base.base_usuario_tipo_service import BaseUsuarioTipoService
# from armazenamento.services.base.base_codigo_sessao_service import BaseCodigoSessaoService
# from armazenamento.dal.data_access_layer import DataAccessLayer
# from armazenamento.decorators.auth_method import auth_method
# 
# from dados.administrador import Administrador
# from dados.fisioterapeuta import Fisioterapeuta
# from dados.pesquisador import Pesquisador
# 
# @autoparams
# def init(
#     user_type_service: BaseUsuarioTipoService, 
#     codigo_sessao_service: BaseCodigoSessaoService
# ):
#     current_user_types_list.set(user_type_service.listar_tipos())
#     current_session_codes_list.set(codigo_sessao_service.listar_codigos_sessoes())
# 


import bcrypt

def hashp(p):
    return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# init()

