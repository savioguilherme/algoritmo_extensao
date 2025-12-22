-- FUNCTION: public.trg_auditoria_inserir()

-- DROP FUNCTION IF EXISTS public.trg_auditoria_inserir();

CREATE OR REPLACE FUNCTION public.trg_auditoria_inserir()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
declare
  v_old jsonb;
  v_new jsonb;
begin
  if TG_OP = 'INSERT' then
    v_old := '{}'::jsonb;
    v_new := to_jsonb(NEW);

  elsif TG_OP = 'UPDATE' then
    v_old := to_jsonb(OLD);
    v_new := to_jsonb(NEW);

  elsif TG_OP = 'DELETE' then
    v_old := to_jsonb(OLD);
    v_new := '{}'::jsonb;

  end if;

  insert into auditoria (
    id_usuario_auditado,
    id_tabela,
    data_hora,
    tupla_inicial,
    tupla_final,
    sincronizado
  ) values (
    coalesce(current_setting('app.user_id', true)::integer, 0),
    coalesce(
		(
			select id_nome_tabela from nome_tabela where nome = TG_TABLE_NAME
		),
		0
	),
    now(),
    v_old,
    v_new,
    true
  );

  if TG_OP = 'DELETE' then
    return OLD;
  end if;

  return NEW;
end;
$BODY$;

ALTER FUNCTION public.trg_auditoria_inserir()
    OWNER TO postgres;

create trigger trg_auditoria_usuario
after insert or update or delete on pessoa
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on usuario
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on paciente
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on acompanhamento_paciente
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on disponibilidade_semanal
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on disponibilidade_semanal_paciente
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on disponibilidade_semanal_usuario
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on restricao_agendamento
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on restricao_agendamento_paciente
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on restricao_agendamento_usuario
for each row
execute function trg_auditoria_inserir();

create trigger trg_auditoria_usuario
after insert or update or delete on sessao
for each row
execute function trg_auditoria_inserir();
