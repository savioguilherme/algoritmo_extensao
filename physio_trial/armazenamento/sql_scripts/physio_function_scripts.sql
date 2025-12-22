-- FUNCTION: public.ufn_codigos_sessoes_listar()

-- DROP FUNCTION IF EXISTS public.ufn_codigos_sessoes_listar();

CREATE OR REPLACE FUNCTION public.ufn_codigos_sessoes_listar(
	)
    RETURNS TABLE(id_cod integer, codigo_sessao character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin
	return query
	select id_codigo as id_cod, codigo as codigo_sessao
	from public.codigo_sessao;
end
$BODY$;

ALTER FUNCTION public.ufn_codigos_sessoes_listar()
    OWNER TO postgres;
