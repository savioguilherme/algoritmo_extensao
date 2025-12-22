-- PROCEDURE: public.usp_usuario_deletar(integer)

-- DROP PROCEDURE IF EXISTS public.usp_usuario_deletar(integer);

CREATE OR REPLACE PROCEDURE public.usp_usuario_deletar(
	IN p_id_usuario_desativado integer)
LANGUAGE 'plpgsql'
AS $BODY$
declare
	v_usuario_id integer;
begin
	v_usuario_id := p_id_usuario_desativado;
	
	if not exists(
		select 1
		from usuario us
		where us.id_usuario = v_usuario_id
	) then
		raise exception 'Não existe usuário com id %.', v_usuario_id;
	end if;

	update usuario u
	set
		ativo = false,
		atualizado_em = now()
	where u.id_usuario = v_usuario_id;
end
$BODY$;
ALTER PROCEDURE public.usp_usuario_deletar(integer)
    OWNER TO postgres;
