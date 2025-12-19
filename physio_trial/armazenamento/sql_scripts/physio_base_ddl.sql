-- =========================================================
-- 1) pessoa
-- =========================================================
create table pessoa(
  id_pessoa        integer generated always as identity primary key,
  email            varchar(100) not null unique,
  nome             varchar(100) not null,
  data_nascimento  date null,
  ativo            boolean null,
  inserido_em      timestamp not null,
  atualizado_em    timestamp null
);

create index idx_pessoa_nome on pessoa (nome);

-- =========================================================
-- 2) paciente (subtipo de pessoa)
-- =========================================================
create table paciente(
  id_paciente        integer primary key,
  status_abandono    boolean null,
  status_conclusao   boolean null,
  inserido_em        timestamp not null,
  atualizado_em      timestamp null,
  constraint fk_paciente_pessoa
  foreign key (id_paciente) references pessoa(id_pessoa)
  on update cascade on delete restrict
);

-- =========================================================
-- 3) usuario_tipo
-- =========================================================
create table usuario_tipo(
  id_tipo  integer generated always as identity primary key,
  nome     varchar(19) not null unique
);

-- =========================================================
-- 4) usuario (subtipo de pessoa)
-- =========================================================
create table usuario(
  id_usuario     integer primary key,
  tipo           integer not null,
  login          varchar(29) not null,
  senha          varchar(29) not null,
  inserido_em    timestamp not null,
  atualizado_em  timestamp null,
  constraint fk_usuario_pessoa
  foreign key (id_usuario) references pessoa(id_pessoa)
  on update cascade on delete restrict,
  constraint fk_usuario_tipo
  foreign key (tipo) references usuario_tipo(id_tipo)
  on update cascade on delete restrict
);

-- (opcional, mas recomendável) evitar login repetido
create unique index uq_usuario_login on usuario (login);

-- =========================================================
-- 5) usuario_tipo_historico
-- =========================================================
create table usuario_tipo_historico (
  id_mudanca            integer generated always as identity primary key,
  id_usuario_atualizado integer not null,
  instante_mudanca      timestamp not null,
  tipo_novo             integer not null,
  tipo_antigo           integer not null,
  constraint fk_uth_usuario
  foreign key (id_usuario_atualizado) references usuario(id_usuario)
  on update cascade on delete restrict,
  constraint fk_uth_tipo_novo
  foreign key (tipo_novo) references usuario_tipo(id_tipo)
  on update cascade on delete restrict,
  constraint fk_uth_tipo_antigo
  foreign key (tipo_antigo) references usuario_tipo(id_tipo)
  on update cascade on delete restrict,
  constraint ck_uth_tipos_diferentes
  check (tipo_novo <> tipo_antigo)
);

create index idx_uth_usuario_instante on usuario_tipo_historico (id_usuario_atualizado, instante_mudanca);

-- =========================================================
-- 6) sessao
-- =========================================================
create table sessao (
  id_sessao            integer generated always as identity primary key,
  codigo               varchar(256) not null,
  id_paciente          integer not null,
  dia                  date not null,
  horario              time not null,
  status_agendamento   boolean null,
  conclusao            boolean not null,
  inserido_em          timestamp not null,
  atualizado_em        timestamp null,
  constraint fk_sessao_paciente
  foreign key (id_paciente) references paciente(id_paciente)
  on update cascade on delete restrict
);

create index idx_sessao_paciente_dia on sessao (id_paciente, dia);

alter table sessao
add column id_pesquisador integer null;

alter table sessao
add column id_fisioterapeuta integer null;

alter table sessao
add constraint fk_id_pesquisador
foreign key (id_pesquisador)
references usuario(id_usuario)
on update cascade on delete restrict;

alter table sessao
add constraint fk_id_fisioterapeuta
foreign key (id_fisioterapeuta)
references usuario(id_usuario)
on update cascade on delete restrict;

-- =========================================================
-- 7) restricao_agendamento
-- =========================================================
create table restricao_agendamento (
  id_restricao  integer generated always as identity primary key,
  inicio        timestamp not null,
  fim           timestamp not null,
  motivo        text null,
  constraint ck_ra_intervalo
  check (inicio < fim)
);

create index idx_ra_paciente_inicio_fim on restricao_agendamento (id_paciente, inicio, fim);

alter table restricao_agendamento
add column inserido_em timestamp not null;

alter table restricao_agendamento
add column atualizado_em timestamp null;

-- =========================================================
-- 8) restricao_agendamento_paciente (associação)
-- =========================================================
create table restricao_agendamento_paciente (
  id_paciente   integer not null,
  id_restricao  integer not null,
  ativa         boolean null,
  primary key (id_paciente, id_restricao),
  constraint fk_rap_paciente
  foreign key (id_paciente) references paciente(id_paciente)
  on update cascade on delete restrict,
  constraint fk_rap_restricao
  foreign key (id_restricao) references restricao_agendamento(id_restricao)
  on update cascade on delete restrict
);

-- =========================================================
-- 9) restricao_agendamento_usuario (associação)
-- =========================================================
create table restricao_agendamento_usuario (
  id_usuario    integer not null,
  id_restricao  integer not null,
  ativa         boolean null,
  primary key (id_usuario, id_restricao),
  constraint fk_rau_usuario
  foreign key (id_usuario) references usuario(id_usuario)
  on update cascade on delete restrict,
  constraint fk_rau_restricao
  foreign key (id_restricao) references restricao_agendamento(id_restricao)
  on update cascade on delete restrict
);

-- =========================================================
-- 10) dia_semana
-- =========================================================
create table dia_semana (
  id_dia  smallint primary key,
  nome    varchar(19) not null
);

-- (opcional) garantir valores 0..6 ou 1..7; escolha um padrão
alter table dia_semana
add constraint ck_dia_semana_range check (id_dia between 0 and 6);

-- =========================================================
-- 11) disponibilidade_semanal
-- =========================================================
create table disponibilidade_semanal (
  id_disponibilidade  integer generated always as identity primary key,
  dia_semana          smallint not null,
  inicio              time not null,
  fim                 time not null,
  constraint fk_ds_dia
  foreign key (dia_semana) references dia_semana(id_dia)
  on update cascade on delete restrict,
  constraint ck_ds_intervalo check (inicio < fim)
);

create index idx_ds_dia_inicio_fim on disponibilidade_semanal (dia_semana, inicio, fim);

alter table disponibilidade_semanal
add column inserido_em timestamp not null;

alter table disponibilidade_semanal
add column atualizado_em timestamp null;

-- =========================================================
-- 12) disponibilidade_semanal_paciente (associação)
-- =========================================================
create table disponibilidade_semanal_paciente (
  id_paciente         integer not null,
  id_disponibilidade  integer not null,
  ativa               boolean null,
  primary key (id_paciente, id_disponibilidade),
  constraint fk_dsp_paciente
  foreign key (id_paciente) references paciente(id_paciente)
  on update cascade on delete restrict,
  constraint fk_dsp_disp
  foreign key (id_disponibilidade) references disponibilidade_semanal(id_disponibilidade)
  on update cascade on delete restrict
);

-- =========================================================
-- 13) disponibilidade_semanal_usuario (associação)
-- =========================================================
create table disponibilidade_semanal_usuario (
  id_usuario          integer not null,
  id_disponibilidade  integer not null,
  ativa               boolean null,
  primary key (id_usuario, id_disponibilidade),
  constraint fk_dsu_usuario
  foreign key (id_usuario) references usuario(id_usuario)
  on update cascade on delete restrict,
  constraint fk_dsu_disp
  foreign key (id_disponibilidade) references disponibilidade_semanal(id_disponibilidade)
  on update cascade on delete restrict
);

-- =========================================================
-- 14) nome_tabela
-- =========================================================
create table nome_tabela (
  id_nome_tabela  integer generated always as identity primary key,
  nome            varchar(55) not null
);

-- (opcional) normalmente faz sentido ser unique
create unique index uq_nome_tabela_nome on nome_tabela (nome);

-- =========================================================
-- 15) auditoria
-- =========================================================
create table auditoria (
  id_auditoria        integer generated always as identity primary key,
  id_usuario_auditado integer not null,
  id_tabela           integer not null,
  data_hora           timestamp not null,
  tupla_inicial       jsonb not null,
  tupla_final         jsonb not null,
  sincronizado        boolean null,
  constraint fk_auditoria_usuario
  foreign key (id_usuario_auditado) references usuario(id_usuario)
  on update cascade on delete restrict,
  constraint fk_auditoria_tabela
  foreign key (id_tabela) references nome_tabela(id_nome_tabela)
  on update cascade on delete restrict
);

create index idx_auditoria_usuario_data on auditoria (id_usuario_auditado, data_hora);
create index idx_auditoria_tabela_data on auditoria (id_tabela, data_hora);
-- =========================================================
