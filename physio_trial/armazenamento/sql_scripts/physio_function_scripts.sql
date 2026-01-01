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

-- FUNCTION: public.ufn_paciente_consultar(integer)

-- DROP FUNCTION IF EXISTS public.ufn_paciente_consultar(integer);

CREATE OR REPLACE FUNCTION public.ufn_paciente_consultar(
	p_id_paciente integer)
    RETURNS TABLE(id_paciente integer, nome character varying, email character varying, data_nascimento date, status_abandono boolean, status_conclusao boolean, restricoes timestamp without time zone[], disponibilidades jsonb[], fisioterapeuta jsonb, pesquisador jsonb, sessoes jsonb[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        pa.id_paciente,
        p.nome,
        p.email,
        p.data_nascimento,
        pa.status_abandono,
        pa.status_conclusao,

        /* restricoes: [inicios...] */
        COALESCE(
            (
                SELECT array_agg(t.dt ORDER BY t.ord, t.dt)
                FROM (
                    SELECT ra.inicio AS dt, 1 AS ord
                    FROM public.restricao_agendamento_paciente rap
                    JOIN public.restricao_agendamento ra
                    ON ra.id_restricao = rap.id_restricao
                    WHERE rap.id_paciente = pa.id_paciente
                    AND rap.ativa
                ) t
            ),
            ARRAY[]::timestamp without time zone[]
        ) AS restricoes,

        /* disponibilidades: jsonb[] com {dia:int, horarios: time[]} */
        COALESCE(
            (
                SELECT array_agg(
                    jsonb_build_object(
                        'dia', x.dia_semana,
                        'horarios', to_jsonb(x.horarios)
                    )
                    ORDER BY x.dia_semana
                )
                FROM (
                    SELECT
                        ds.dia_semana,
                        array_agg(ds.inicio ORDER BY ds.inicio) AS horarios
                    FROM public.disponibilidade_semanal_paciente dsp
                    JOIN public.disponibilidade_semanal ds
                      ON ds.id_disponibilidade = dsp.id_disponibilidade
                    WHERE dsp.id_paciente = pa.id_paciente
                      AND COALESCE(dsp.ativa, true) = true
                    GROUP BY ds.dia_semana
                ) x
            ),
            ARRAY[]::jsonb[]
        ) AS disponibilidades,

		/* fisioterapeuta (jsonb) via acompanhamento_paciente.id_fisioterapeuta */
        (
            SELECT jsonb_build_object(
                'id_usuario', u.id_usuario,
                'tipo', u.tipo,
                'login', u.login,
                'ativo', u.ativo,
                'nome', pu.nome,
                'email', pu.email,
                'data_nascimento', pu.data_nascimento
            )
            FROM public.usuario u
            JOIN public.pessoa pu ON pu.id_pessoa = u.id_usuario
            WHERE u.id_usuario = acp.id_fisioterapeuta
        ) AS fisioterapeuta,

		/* pesquisador (jsonb) via acompanhamento_paciente.id_pesquisador */
        (
            SELECT jsonb_build_object(
                'id_usuario', u.id_usuario,
                'tipo', u.tipo,
                'login', u.login,
                'ativo', u.ativo,
                'nome', pu.nome,
                'email', pu.email,
                'data_nascimento', pu.data_nascimento
            )
            FROM public.usuario u
            JOIN public.pessoa pu ON pu.id_pessoa = u.id_usuario
            WHERE u.id_usuario = acp.id_pesquisador
        ) AS pesquisador,

		/* sessoes: jsonb[] com os dados de cada sessão */
        COALESCE(
            (
                SELECT array_agg(
                    jsonb_build_object(
                        'id_sessao', y.id_sessao,
                        'dia', y.dia,
						'horario', y.horario,
						'status_agendamento', y.agendada,
						'conclusao', y.conclusao,
						'cod_sigla', y.cod_sigla
                    )
                    ORDER BY y.codigo
                )
                FROM (
                    SELECT
                        se.id_sessao,
						se.dia,
						se.horario,
						se.status_agendamento as agendada,
						se.conclusao,
						se.codigo,
						cs.codigo as cod_sigla
                    FROM public.sessao se
					JOIN public.codigo_sessao cs
					ON cs.id_codigo = se.codigo
                    WHERE se.id_paciente = pa.id_paciente
                ) y
            ),
            ARRAY[]::jsonb[]
        ) AS sessoes

    FROM public.pessoa p
    JOIN public.paciente pa
    ON pa.id_paciente = p.id_pessoa
	LEFT JOIN public.acompanhamento_paciente acp
    ON acp.id_paciente = pa.id_paciente
    WHERE pa.id_paciente = p_id_paciente;
END;
$BODY$;

ALTER FUNCTION public.ufn_paciente_consultar(integer)
    OWNER TO postgres;

-- FUNCTION: public.ufn_paciente_listar(boolean)

-- DROP FUNCTION IF EXISTS public.ufn_paciente_listar(boolean);

CREATE OR REPLACE FUNCTION public.ufn_paciente_listar(
	p_apenas_ativos boolean)
    RETURNS TABLE(id_paciente integer, nome character varying, email character varying, data_nascimento date, status_abandono boolean, status_conclusao boolean, restricoes timestamp without time zone[], disponibilidades jsonb[], fisioterapeuta jsonb, pesquisador jsonb, sessoes jsonb[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        pa.id_paciente,
        p.nome,
        p.email,
        p.data_nascimento,
        pa.status_abandono,
        pa.status_conclusao,

        /* restricoes: [inicios...] */
        COALESCE(
            (
                SELECT array_agg(t.dt ORDER BY t.ord, t.dt)
                FROM (
                    SELECT ra.inicio AS dt, 1 AS ord
                    FROM public.restricao_agendamento_paciente rap
                    JOIN public.restricao_agendamento ra
                    ON ra.id_restricao = rap.id_restricao
                    WHERE rap.id_paciente = pa.id_paciente
                    AND rap.ativa
                ) t
            ),
            ARRAY[]::timestamp without time zone[]
        ) AS restricoes,

        /* disponibilidades: jsonb[] com {dia:int, horarios: time[]} */
        COALESCE(
            (
                SELECT array_agg(
                    jsonb_build_object(
                        'dia', x.dia_semana,
                        'horarios', to_jsonb(x.horarios)
                    )
                    ORDER BY x.dia_semana
                )
                FROM (
                    SELECT
                        ds.dia_semana,
                        array_agg(ds.inicio ORDER BY ds.inicio) AS horarios
                    FROM public.disponibilidade_semanal_paciente dsp
                    JOIN public.disponibilidade_semanal ds
                      ON ds.id_disponibilidade = dsp.id_disponibilidade
                    WHERE dsp.id_paciente = pa.id_paciente
                      AND COALESCE(dsp.ativa, true) = true
                    GROUP BY ds.dia_semana
                ) x
            ),
            ARRAY[]::jsonb[]
        ) AS disponibilidades,

		/* fisioterapeuta (jsonb) via acompanhamento_paciente.id_fisioterapeuta */
        (
            SELECT jsonb_build_object(
                'id_usuario', u.id_usuario,
                'tipo', u.tipo,
                'login', u.login,
                'ativo', u.ativo,
                'nome', pu.nome,
                'email', pu.email,
                'data_nascimento', pu.data_nascimento
            )
            FROM public.usuario u
            JOIN public.pessoa pu ON pu.id_pessoa = u.id_usuario
            WHERE u.id_usuario = acp.id_fisioterapeuta
        ) AS fisioterapeuta,

		/* pesquisador (jsonb) via acompanhamento_paciente.id_pesquisador */
        (
            SELECT jsonb_build_object(
                'id_usuario', u.id_usuario,
                'tipo', u.tipo,
                'login', u.login,
                'ativo', u.ativo,
                'nome', pu.nome,
                'email', pu.email,
                'data_nascimento', pu.data_nascimento
            )
            FROM public.usuario u
            JOIN public.pessoa pu ON pu.id_pessoa = u.id_usuario
            WHERE u.id_usuario = acp.id_pesquisador
        ) AS pesquisador,

		/* sessoes: jsonb[] com os dados de cada sessão */
        COALESCE(
            (
                SELECT array_agg(
                    jsonb_build_object(
                        'id_sessao', y.id_sessao,
                        'dia', y.dia,
						'horario', y.horario,
						'status_agendamento', y.agendada,
						'conclusao', y.conclusao,
						'cod_sigla', y.cod_sigla
                    )
                    ORDER BY y.codigo
                )
                FROM (
                    SELECT
                        se.id_sessao,
						se.dia,
						se.horario,
						se.status_agendamento as agendada,
						se.conclusao,
						se.codigo,
						cs.codigo as cod_sigla
                    FROM public.sessao se
					JOIN public.codigo_sessao cs
					ON cs.id_codigo = se.codigo
                    WHERE se.id_paciente = pa.id_paciente
                ) y
            ),
            ARRAY[]::jsonb[]
        ) AS sessoes

    FROM public.pessoa p
    JOIN public.paciente pa
    ON pa.id_paciente = p.id_pessoa
	LEFT JOIN public.acompanhamento_paciente acp
    ON acp.id_paciente = pa.id_paciente
    WHERE p_apenas_ativos IS NULL
    OR NOT p_apenas_ativos
    OR (
		p_apenas_ativos
		AND (pa.status_abandono IS NULL OR NOT pa.status_abandono)
		AND (pa.status_conclusao IS NULL OR NOT pa.status_conclusao)
    );
END;
$BODY$;

ALTER FUNCTION public.ufn_paciente_listar(boolean)
    OWNER TO postgres;

-- FUNCTION: public.ufn_usuario_consultar(integer)

-- DROP FUNCTION IF EXISTS public.ufn_usuario_consultar(integer);

CREATE OR REPLACE FUNCTION public.ufn_usuario_consultar(
	p_id_usuario integer)
    RETURNS TABLE(id_usuario integer, nome character varying, email character varying, data_nascimento date, tipo integer, login character varying, senha character varying, ativo boolean, restricoes timestamp without time zone[], disponibilidades jsonb[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin
	return query
	select
		u.id_usuario,
		p.nome,
		p.email,
		p.data_nascimento,
		u.tipo,
		u.login,
		u.senha,
		u.ativo,

		/* restricoes (somente se não for admin) */
        CASE
            WHEN lower(ut.nome) IN ('admin', 'administrador') THEN
                ARRAY[]::timestamp without time zone[]
            ELSE
                COALESCE(
                    (
                        SELECT array_agg(ra.inicio ORDER BY ra.inicio)
                        FROM public.restricao_agendamento_usuario rau
                        JOIN public.restricao_agendamento ra
                          ON ra.id_restricao = rau.id_restricao
                        WHERE rau.id_usuario = u.id_usuario
                          AND COALESCE(rau.ativa, true) = true
                    ),
                    ARRAY[]::timestamp without time zone[]
                )
        END AS restricoes,

        /* disponibilidades (somente se não for admin) */
        CASE
            WHEN lower(ut.nome) IN ('admin', 'administrador') THEN
                ARRAY[]::jsonb[]
            ELSE
                COALESCE(
                    (
                        SELECT array_agg(
                            jsonb_build_object(
                                'dia', x.dia_semana,
                                'horarios', to_jsonb(x.horarios)
                            )
                            ORDER BY x.dia_semana
                        )
                        FROM (
                            SELECT
                                ds.dia_semana,
                                array_agg(ds.inicio ORDER BY ds.inicio) AS horarios
                            FROM public.disponibilidade_semanal_usuario dsu
                            JOIN public.disponibilidade_semanal ds
                              ON ds.id_disponibilidade = dsu.id_disponibilidade
                            WHERE dsu.id_usuario = u.id_usuario
                              AND COALESCE(dsu.ativa, true) = true
                            GROUP BY ds.dia_semana
                        ) x
                    ),
                    ARRAY[]::jsonb[]
                )
        END AS disponibilidades

	from usuario u
	join pessoa p
	on u.id_usuario = p.id_pessoa
	join public.usuario_tipo ut
    on ut.id_tipo = u.tipo
	where u.id_usuario = p_id_usuario;
end
$BODY$;

ALTER FUNCTION public.ufn_usuario_consultar(integer)
    OWNER TO postgres;

-- FUNCTION: public.ufn_usuario_consultar_por_login(character varying)

-- DROP FUNCTION IF EXISTS public.ufn_usuario_consultar_por_login(character varying);

CREATE OR REPLACE FUNCTION public.ufn_usuario_consultar_por_login(
	p_login character varying)
    RETURNS TABLE(id_usuario integer, tipo integer, login character varying, senha character varying, ativo boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin
	return query
	select
		u.id_usuario,
		u.tipo,
		u.login,
		u.senha,
		u.ativo
	from usuario u
	where u.login = trim(p_login);
end
$BODY$;

ALTER FUNCTION public.ufn_usuario_consultar_por_login(character varying)
    OWNER TO postgres;

-- FUNCTION: public.ufn_usuario_listar(boolean, integer[])

-- DROP FUNCTION IF EXISTS public.ufn_usuario_listar(boolean, integer[]);

CREATE OR REPLACE FUNCTION public.ufn_usuario_listar(
	p_apenas_ativos boolean,
	p_tipos integer[])
    RETURNS TABLE(id_usuario integer, nome character varying, email character varying, data_nascimento date, tipo integer, login character varying, senha character varying, ativo boolean, restricoes timestamp without time zone[], disponibilidades jsonb[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        u.id_usuario,
        p.nome,
        p.email,
        p.data_nascimento,
        u.tipo,
        u.login,
        u.senha,
        u.ativo,

        /* restricoes (somente se não for admin) */
        CASE
            WHEN lower(ut.nome) IN ('admin', 'administrador') THEN
                ARRAY[]::timestamp without time zone[]
            ELSE
                COALESCE(
                    (
                        SELECT array_agg(ra.inicio ORDER BY ra.inicio)
                        FROM public.restricao_agendamento_usuario rau
                        JOIN public.restricao_agendamento ra
                          ON ra.id_restricao = rau.id_restricao
                        WHERE rau.id_usuario = u.id_usuario
                          AND COALESCE(rau.ativa, true) = true
                    ),
                    ARRAY[]::timestamp without time zone[]
                )
        END AS restricoes,

        /* disponibilidades (somente se não for admin) */
        CASE
            WHEN lower(ut.nome) IN ('admin', 'administrador') THEN
                ARRAY[]::jsonb[]
            ELSE
                COALESCE(
                    (
                        SELECT array_agg(
                            jsonb_build_object(
                                'dia', x.dia_semana,
                                'horarios', to_jsonb(x.horarios)
                            )
                            ORDER BY x.dia_semana
                        )
                        FROM (
                            SELECT
                                ds.dia_semana,
                                array_agg(ds.inicio ORDER BY ds.inicio) AS horarios
                            FROM public.disponibilidade_semanal_usuario dsu
                            JOIN public.disponibilidade_semanal ds
                              ON ds.id_disponibilidade = dsu.id_disponibilidade
                            WHERE dsu.id_usuario = u.id_usuario
                              AND COALESCE(dsu.ativa, true) = true
                            GROUP BY ds.dia_semana
                        ) x
                    ),
                    ARRAY[]::jsonb[]
                )
        END AS disponibilidades

    FROM public.usuario u
    JOIN public.pessoa p
      ON u.id_usuario = p.id_pessoa
    JOIN public.usuario_tipo ut
      ON ut.id_tipo = u.tipo
    WHERE u.tipo = ANY(p_tipos)
    AND (p_apenas_ativos IS NULL
    OR NOT p_apenas_ativos
    OR (
		p_apenas_ativos
		AND
		(u.ativo IS NULL OR u.ativo)
    ))
    ORDER BY u.tipo, p.nome ASC;
END;
$BODY$;

ALTER FUNCTION public.ufn_usuario_listar(boolean, integer[])
    OWNER TO postgres;

-- FUNCTION: public.ufn_usuario_tipos_listar()

-- DROP FUNCTION IF EXISTS public.ufn_usuario_tipos_listar();

CREATE OR REPLACE FUNCTION public.ufn_usuario_tipos_listar(
	)
    RETURNS TABLE(id_tipo integer, nome character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin
	return query
	select ut.* from usuario_tipo ut
	order by ut.id_tipo;
end
$BODY$;

ALTER FUNCTION public.ufn_usuario_tipos_listar()
    OWNER TO postgres;
