begin
-- =========================
-- 3) pessoas (8)
-- =========================
-- 1 admin, 2 fisios, 2 pesquisadores, 3 pacientes
insert into public.pessoa (email, nome, data_nascimento, inserido_em, atualizado_em)
values
  ('admin@usp.com', 'Admin USP', '1990-01-10', now(), null),
  ('fisio1@usp.com', 'Fisio 1', '1992-03-05', now(), null),
  ('fisio2@usp.com', 'Fisio 2', '1991-11-22', now(), null),
  ('pesq1@usp.com', 'Pesquisador 1', '1988-06-18', now(), null),
  ('pesq2@usp.com', 'Pesquisador 2', '1993-09-30', now(), null),
  ('pac1@usp.com', 'Paciente 1', '2002-02-14', now(), null),
  ('pac2@usp.com', 'Paciente 2', '1999-07-07', now(), null),
  ('pac3@usp.com', 'Paciente 3', '2005-12-01', now(), null)
on conflict (email) do nothing;
select * from usuario_tipo;
-- =========================
-- 4) usuarios (5) e pacientes (3)
-- =========================
-- Mapeia ids pelas emails recém inseridas
with p as (
  select id_pessoa, email
  from public.pessoa
  where email in (
    'admin@usp.com','fisio1@usp.com','fisio2@usp.com','pesq1@usp.com','pesq2@usp.com',
    'pac1@usp.com','pac2@usp.com','pac3@usp.com'
  )
),
tipos as (
  select id_tipo, nome
  from public.usuario_tipo
)
insert into public.usuario (id_usuario, tipo, login, senha, inserido_em, atualizado_em, ativo)
select
  p.id_pessoa,
  case p.email
    when 'admin@usp.com' then (select id_tipo from tipos where nome ilike '%admin%')
    when 'fisio1@usp.com' then (select id_tipo from tipos where nome ilike '%sioterapeu%')
    when 'fisio2@usp.com' then (select id_tipo from tipos where nome ilike '%sioterapeu%')
    when 'pesq1@usp.com' then (select id_tipo from tipos where nome ilike '%esquisa%')
    when 'pesq2@usp.com' then (select id_tipo from tipos where nome ilike '%esquisa%')
  end,
  case p.email
    when 'admin@usp.com' then 'admin'
    when 'fisio1@usp.com' then 'fisio1'
    when 'fisio2@usp.com' then 'fisio2'
    when 'pesq1@usp.com' then 'pesq1'
    when 'pesq2@usp.com' then 'pesq2'
  end,
  'Physi0_Test',
  now(), null, true
from p
where p.email in ('admin@usp.com','fisio1@usp.com','fisio2@usp.com','pesq1@usp.com','pesq2@usp.com')
on conflict (id_usuario) do nothing;

with p as (
  select id_pessoa, email
  from public.pessoa
  where email in ('pac1@usp.com','pac2@usp.com','pac3@usp.com')
)
insert into public.paciente (id_paciente, status_abandono, status_conclusao, inserido_em, atualizado_em)
select
  id_pessoa,
  false,
  false,
  now(),
  null
from p
on conflict (id_paciente) do nothing;

-- =========================
-- 5) disponibilidade_semanal (cria 8 slots) + vínculo usuário/paciente
-- =========================
-- 4 disponibilidades para usuários (1 fisio + 1 pesq para cada um) = 4
-- 2 disponibilidades para pacientes (para pac1 e pac2) = 2
-- (total 6). Vou criar 8 pra sobrar 2 e facilitar testes.
-- Observação: id_disponibilidade é identity, então não precisa informar.

-- Cria disponibilidades (manhã/tarde) em dias distintos
insert into public.disponibilidade_semanal (dia_semana, inicio, fim, inserido_em, atualizado_em)
values
  (0, '08:00', '12:00', now(), null), -- seg
  (2, '14:00', '18:00', now(), null), -- qua
  (1, '09:00', '11:00', now(), null), -- ter
  (3, '13:00', '17:00', now(), null), -- qui
  (4, '08:30', '10:30', now(), null), -- sex
  (0, '15:00', '17:00', now(), null), -- seg
  (2, '08:00', '10:00', now(), null), -- qua
  (5, '09:00', '12:00', now(), null)  -- sab
;

-- Linkar disponibilidades aos usuários/pacientes
-- Vamos pegar os ids criados mais recentemente
with disp as (
  select id_disponibilidade
  from public.disponibilidade_semanal
  order by id_disponibilidade desc
  limit 8
),
disp_ord as (
  select id_disponibilidade, row_number() over(order by id_disponibilidade) as rn
  from disp
),
ids as (
  select
    (select id_pessoa from public.pessoa where email='fisio1@usp.com') as fisio1,
    (select id_pessoa from public.pessoa where email='pesq1@usp.com') as pesq1,
    (select id_pessoa from public.pessoa where email='fisio2@usp.com') as fisio2,
    (select id_pessoa from public.pessoa where email='pesq2@usp.com') as pesq2,
    (select id_pessoa from public.pessoa where email='pac1@usp.com') as pac1,
    (select id_pessoa from public.pessoa where email='pac2@usp.com') as pac2
)
insert into public.disponibilidade_semanal_usuario (id_usuario, id_disponibilidade, ativa)
select ids.fisio1, d.id_disponibilidade, true from ids join disp_ord d on d.rn = 1
union all
select ids.pesq1,  d.id_disponibilidade, true from ids join disp_ord d on d.rn = 2
union all
select ids.fisio2, d.id_disponibilidade, true from ids join disp_ord d on d.rn = 3
union all
select ids.pesq2,  d.id_disponibilidade, true from ids join disp_ord d on d.rn = 4
;

with disp as (
  select id_disponibilidade
  from public.disponibilidade_semanal
  order by id_disponibilidade desc
  limit 8
),
disp_ord as (
  select id_disponibilidade, row_number() over(order by id_disponibilidade) as rn
  from disp
),
ids as (
  select
    (select id_pessoa from public.pessoa where email='pac1@usp.com') as pac1,
    (select id_pessoa from public.pessoa where email='pac2@usp.com') as pac2
)
insert into public.disponibilidade_semanal_paciente (id_paciente, id_disponibilidade, ativa)
select ids.pac1, d.id_disponibilidade, true from ids join disp_ord d on d.rn = 5
union all
select ids.pac2, d.id_disponibilidade, true from ids join disp_ord d on d.rn = 6
;

-- =========================
-- 6) restricao_agendamento + vínculos
-- =========================
-- 2 restrições paciente (pac1, pac2)
-- 4 restrições usuário (fisio1,fisio2,pesq1,pesq2)
insert into public.restricao_agendamento (inicio, fim, motivo, inserido_em, atualizado_em)
values
  (now() + interval '1 day' + time '10:00', now() + interval '1 day' + time '12:00', 'Consulta médica', now(), null),  -- r1
  (now() + interval '2 day' + time '14:00', now() + interval '2 day' + time '16:00', 'Compromisso pessoal', now(), null), -- r2
  (now() + interval '1 day' + time '08:00', now() + interval '1 day' + time '09:00', 'Reunião', now(), null), -- r3
  (now() + interval '3 day' + time '13:00', now() + interval '3 day' + time '15:00', 'Aula', now(), null), -- r4
  (now() + interval '2 day' + time '09:00', now() + interval '2 day' + time '10:00', 'Entrevista', now(), null), -- r5
  (now() + interval '4 day' + time '16:00', now() + interval '4 day' + time '17:00', 'Orientação', now(), null) -- r6
;

with r as (
  select id_restricao
  from public.restricao_agendamento
  order by id_restricao desc
  limit 6
),
r_ord as (
  select id_restricao, row_number() over(order by id_restricao) as rn
  from r
),
ids as (
  select
    (select id_pessoa from public.pessoa where email='pac1@usp.com') as pac1,
    (select id_pessoa from public.pessoa where email='pac2@usp.com') as pac2,
    (select id_pessoa from public.pessoa where email='fisio1@usp.com') as fisio1,
    (select id_pessoa from public.pessoa where email='fisio2@usp.com') as fisio2,
    (select id_pessoa from public.pessoa where email='pesq1@usp.com') as pesq1,
    (select id_pessoa from public.pessoa where email='pesq2@usp.com') as pesq2
)
insert into public.restricao_agendamento_paciente (id_paciente, id_restricao, ativa)
select ids.pac1, ro.id_restricao, true from ids join r_ord ro on ro.rn = 1
union all
select ids.pac2, ro.id_restricao, true from ids join r_ord ro on ro.rn = 2
;

with r as (
  select id_restricao
  from public.restricao_agendamento
  order by id_restricao desc
  limit 6
),
r_ord as (
  select id_restricao, row_number() over(order by id_restricao) as rn
  from r
),
ids as (
  select
    (select id_pessoa from public.pessoa where email='fisio1@usp.com') as fisio1,
    (select id_pessoa from public.pessoa where email='fisio2@usp.com') as fisio2,
    (select id_pessoa from public.pessoa where email='pesq1@usp.com') as pesq1,
    (select id_pessoa from public.pessoa where email='pesq2@usp.com') as pesq2
)
insert into public.restricao_agendamento_usuario (id_usuario, id_restricao, ativa)
select ids.fisio1, ro.id_restricao, true from ids join r_ord ro on ro.rn = 3
union all
select ids.fisio2, ro.id_restricao, true from ids join r_ord ro on ro.rn = 4
union all
select ids.pesq1,  ro.id_restricao, true from ids join r_ord ro on ro.rn = 5
union all
select ids.pesq2,  ro.id_restricao, true from ids join r_ord ro on ro.rn = 6
;

-- =========================
-- 8) sessao (4 sessões: 2 para pac1 e 2 para pac2)
-- =========================
with ids as (
  select
    (select id_pessoa from public.pessoa where email='pac1@usp.com') as pac1,
    (select id_pessoa from public.pessoa where email='pac2@usp.com') as pac2
)
insert into public.sessao (id_paciente, dia, horario, status_agendamento, conclusao, inserido_em, codigo)
select ids.pac1, current_date + 1, '09:00:00'::time without time zone, true,  false, now(), 1 from ids
union all
select ids.pac1, current_date + 8, '09:30:00'::time without time zone, true,  false, now(), 2 from ids
union all
select ids.pac2, current_date + 2, '15:00:00'::time without time zone, true,  false, now(), 1 from ids
union all
select ids.pac2, current_date + 9, '15:30:00'::time without time zone, true,  false, now(), 2 from ids
;

-- =========================
-- 9) acompanhamento_paciente (opcional, mas útil p/ testes)
-- =========================
-- associa pac1 e pac2 a 1 pesq e 1 fisio (mantendo distintos)
insert into public.acompanhamento_paciente (id_paciente, id_pesquisador, id_fisioterapeuta)
values
(
  (select id_pessoa from public.pessoa where email='pac1@usp.com'),
  (select id_pessoa from public.pessoa where email='pesq1@usp.com'),
  (select id_pessoa from public.pessoa where email='fisio1@usp.com')
),
(
  (select id_pessoa from public.pessoa where email='pac2@usp.com'),
  (select id_pessoa from public.pessoa where email='pesq2@usp.com'),
  (select id_pessoa from public.pessoa where email='fisio2@usp.com')
)
on conflict (id_paciente) do nothing;

commit;
