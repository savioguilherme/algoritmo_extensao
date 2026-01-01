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

-- PROCEDURE: public.usp_paciente_alterar(integer, character varying, character varying, date, boolean, boolean, integer, integer, jsonb, jsonb, jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_paciente_alterar(integer, character varying, character varying, date, boolean, boolean, integer, integer, jsonb, jsonb, jsonb);

CREATE OR REPLACE PROCEDURE public.usp_paciente_alterar(
	IN p_id_paciente integer,
	IN p_nome character varying,
	IN p_email character varying,
	IN p_data_nascimento date,
	IN p_status_abandono boolean,
	IN p_status_conclusao boolean,
	IN p_id_pesquisador integer,
	IN p_id_fisioterapeuta integer,
	IN p_disponibilidades jsonb,
	IN p_restricoes jsonb,
	IN p_sessoes jsonb)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_disp                 jsonb;
    v_hor                   text;
    v_dt               timestamp;
    v_dia               smallint;
    v_time                  time;
    v_id_disponibilidade integer;
	v_ids_disp         integer[];
    v_id_restricao       integer;
	v_ids_restr        integer[];
    v_sess                 jsonb;
    v_id_sessao          integer;
    v_codigo             integer;
    v_dia_sess              date;
    v_hora_sess             time;
    v_agendada           boolean;
    v_conclusao          boolean;
	v_row_count          integer;
BEGIN
    -- valida existência do paciente
    IF NOT EXISTS (SELECT 1 FROM public.paciente pa WHERE pa.id_paciente = p_id_paciente) THEN
        RAISE EXCEPTION 'Nenhum paciente com o ID %', p_id_paciente;
    END IF;

	IF p_status_abandono IS NOT NULL OR p_status_conclusao IS NOT NULL THEN
		UPDATE public.paciente
		SET
			status_abandono = COALESCE(p_status_abandono, status_abandono),
			status_conclusao = COALESCE(p_status_conclusao, status_conclusao),
			atualizado_em = now()
		WHERE id_paciente = p_id_paciente;
	END IF;

	IF (p_email IS NOT NULL AND LENGTH(trim(p_email)) > 0)
	OR (p_nome IS NOT NULL AND LENGTH(trim(p_nome)) > 0)
	OR p_data_nascimento IS NOT NULL
	THEN
	    -- Atualiza pessoa (somente se vier algo útil)
	    UPDATE public.pessoa
	    SET
	        email = COALESCE(NULLIF(trim(p_email), ''), email),
	        nome  = COALESCE(NULLIF(trim(p_nome), ''), nome),
	        data_nascimento = COALESCE(p_data_nascimento, data_nascimento),
	        atualizado_em = now()
	    WHERE id_pessoa = p_id_paciente;
	END IF;

    -- Acompanhamento (upsert)
    IF p_id_pesquisador IS NOT NULL OR p_id_fisioterapeuta IS NOT NULL THEN
        INSERT INTO public.acompanhamento_paciente(id_paciente, id_pesquisador, id_fisioterapeuta)
        VALUES (p_id_paciente, p_id_pesquisador, p_id_fisioterapeuta)
        ON CONFLICT (id_paciente)
        DO UPDATE
		SET
            id_pesquisador = EXCLUDED.id_pesquisador,
            id_fisioterapeuta = EXCLUDED.id_fisioterapeuta;
    END IF;

    ----------------------------------------------------------------------
    -- DISPONIBILIDADES: ativa somente as do payload
    ----------------------------------------------------------------------
    IF p_disponibilidades IS NOT NULL AND jsonb_typeof(p_disponibilidades) = 'array' THEN
		v_ids_disp  := array[]::integer[];
        
		FOR v_disp IN SELECT * FROM jsonb_array_elements(p_disponibilidades)
        LOOP
            v_dia := (v_disp->>'dia')::smallint;

            FOR v_hor IN SELECT * FROM jsonb_array_elements_text(v_disp->'horarios')
            LOOP
                v_time := v_hor::time without time zone;

                SELECT ds.id_disponibilidade
                  INTO v_id_disponibilidade
                  FROM public.disponibilidade_semanal ds
                 WHERE ds.dia_semana = v_dia
                   AND ds.inicio = v_time
                   -- Não leva o fim em consideração: AND ds.fim = (v_time + interval '1 hour')::time
                 LIMIT 1;

                IF v_id_disponibilidade IS NULL THEN
                    INSERT INTO public.disponibilidade_semanal(dia_semana, inicio, fim, inserido_em)
                    VALUES (v_dia, v_time, (v_time + interval '1 hour')::time without time zone, now())
                    RETURNING id_disponibilidade INTO v_id_disponibilidade;
                END IF;

                INSERT INTO public.disponibilidade_semanal_paciente(id_paciente, id_disponibilidade, ativa)
                VALUES (p_id_paciente, v_id_disponibilidade, true)
                ON CONFLICT (id_paciente, id_disponibilidade)
                DO UPDATE SET ativa = EXCLUDED.ativa;

				v_ids_disp := array_append(v_ids_disp, v_id_disponibilidade);
            END LOOP;
        END LOOP;

		UPDATE public.disponibilidade_semanal_paciente
		SET ativa = false
		WHERE id_paciente = p_id_paciente
		AND (
			array_length(v_ids_disp, 1) IS NULL
			OR
			(
				array_length(v_ids_disp, 1) IS NOT NULL
				AND
				NOT (id_disponibilidade = ANY(v_ids_disp))
			)
		);
    END IF;

    ----------------------------------------------------------------------
    -- RESTRIÇÕES: ativa somente as do payload
    ----------------------------------------------------------------------
    IF p_restricoes IS NOT NULL AND jsonb_typeof(p_restricoes) = 'array' THEN
		v_ids_restr := array[]::integer[];
	
        FOR v_hor IN SELECT * FROM jsonb_array_elements_text(p_restricoes)
        LOOP
            v_dt := v_hor::timestamp without time zone;

			SELECT ra.id_restricao
			  INTO v_id_restricao
			  FROM public.restricao_agendamento ra
			 WHERE ra.inicio = v_dt
			   -- Não leva o fim em consideração: AND ra.fim = (v_dt + interval '1 hour')::time
			 LIMIT 1;

			IF v_id_restricao IS NULL THEN
				INSERT INTO public.restricao_agendamento(inicio, fim, motivo, inserido_em)
            	VALUES (v_dt, v_dt + interval '1 hour', 'restrição genérica', now())
            	RETURNING id_restricao INTO v_id_restricao;
			END IF;

            INSERT INTO public.restricao_agendamento_paciente(id_paciente, id_restricao, ativa)
            VALUES (p_id_paciente, v_id_restricao, true)
			ON CONFLICT (id_paciente, id_restricao)
            DO UPDATE SET ativa = EXCLUDED.ativa;

			v_ids_restr := array_append(v_ids_restr, v_id_restricao);
        END LOOP;

		UPDATE restricao_agendamento_paciente
		SET ativa = false
		WHERE id_paciente = p_id_paciente
		AND (
			array_length(v_ids_restr, 1) IS NULL
			OR
			(
				array_length(v_ids_restr, 1) IS NOT NULL
				AND
				NOT (id_restricao = ANY(v_ids_restr))
			)
		);
    END IF;

    ----------------------------------------------------------------------
    -- SESSÕES: upsert por id_sessao (quando vier) ou por (codigo, id_paciente)
    ----------------------------------------------------------------------
    IF p_sessoes IS NOT NULL AND jsonb_typeof(p_sessoes) = 'array' THEN
        FOR v_sess IN SELECT * FROM jsonb_array_elements(p_sessoes)
        LOOP
            v_id_sessao := NULLIF(v_sess->>'id_sessao','')::integer;
            v_codigo    := NULLIF(v_sess->>'codigo','')::integer;

            v_dia_sess  := (v_sess->>'dia')::date;
            v_hora_sess := (v_sess->>'horario')::time without time zone;

            v_agendada  := COALESCE((v_sess->>'agendada')::boolean, false);
            v_conclusao := COALESCE((v_sess->>'conclusao')::boolean, false);

            IF v_id_sessao IS NOT NULL THEN
                UPDATE public.sessao
                   SET codigo = v_codigo,
                       dia = v_dia_sess,
                       horario = v_hora_sess,
                       status_agendamento = v_agendada,
                       conclusao = v_conclusao,
                       atualizado_em = now()
                 WHERE id_sessao = v_id_sessao
                   AND id_paciente = p_id_paciente;

				GET DIAGNOSTICS v_row_count = ROW_COUNT;

      			IF v_row_count = 0 THEN
				  RAISE EXCEPTION 'ID inválido para sessão cujo código é % e o paciente é o ID %', COALESCE(
					  (
						SELECT cod.codigo FROM public.codigo_sessao cod
						WHERE cod.id_codigo = v_codigo
					  ),
					  ''
				  ), p_id_paciente;
				END IF;
            ELSE
                -- sem id_sessao: usa a unique (codigo, id_paciente)
                INSERT INTO public.sessao(
                    id_paciente, codigo, dia, horario, status_agendamento, conclusao, inserido_em
                ) VALUES (
                    p_id_paciente, v_codigo, v_dia_sess, v_hora_sess, v_agendada, v_conclusao, now()
                )
                ON CONFLICT (codigo, id_paciente)
                DO UPDATE SET
                    dia = EXCLUDED.dia,
                    horario = EXCLUDED.horario,
                    status_agendamento = EXCLUDED.status_agendamento,
                    conclusao = EXCLUDED.conclusao,
                    atualizado_em = now();
            END IF;
        END LOOP;
    END IF;
END;
$BODY$;
ALTER PROCEDURE public.usp_paciente_alterar(integer, character varying, character varying, date, boolean, boolean, integer, integer, jsonb, jsonb, jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_paciente_alterar_acompanhamentos(jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_paciente_alterar_acompanhamentos(jsonb);

CREATE OR REPLACE PROCEDURE public.usp_paciente_alterar_acompanhamentos(
	IN p_lista_acompanhamentos jsonb)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    INSERT INTO public.acompanhamento_paciente (id_paciente, id_fisioterapeuta, id_pesquisador)
    SELECT
        (x->>'id_paciente')::int,
        (x->>'id_fisioterapeuta')::int,
        (x->>'id_pesquisador')::int
    FROM jsonb_array_elements(p_lista_acompanhamentos) AS x
    ON CONFLICT (id_paciente)
    DO UPDATE SET
        id_fisioterapeuta = EXCLUDED.id_fisioterapeuta,
        id_pesquisador    = EXCLUDED.id_pesquisador;
END;
$BODY$;
ALTER PROCEDURE public.usp_paciente_alterar_acompanhamentos(jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_sessoes_alterar_em_massa(jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_sessoes_alterar_em_massa(jsonb);

CREATE OR REPLACE PROCEDURE public.usp_sessoes_alterar_em_massa(
	IN p_lista_sessoes jsonb)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    UPDATE public.sessao se
    SET
        dia           = v.dia,
        horario       = v.horario,
		atualizado_em = now()
    FROM (
        SELECT
            (x->>'id_sessao')::int AS id_sessao,
            ((x->>'dia_horario')::timestamp)::date AS dia,
            ((x->>'dia_horario')::timestamp)::time AS horario
        FROM jsonb_array_elements(p_lista_sessoes) AS x
    ) v
    WHERE se.id_sessao = v.id_sessao;
END;
$BODY$;
ALTER PROCEDURE public.usp_sessoes_alterar_em_massa(jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_paciente_alterar_acompanhamentos_com_sessoes(jsonb, jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_paciente_alterar_acompanhamentos_com_sessoes(jsonb, jsonb);

CREATE OR REPLACE PROCEDURE public.usp_paciente_alterar_acompanhamentos_com_sessoes(
	IN p_lista_acompanhamentos jsonb,
	IN p_sessoes_atualizadas jsonb)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    CALL usp_paciente_alterar_acompanhamentos(p_lista_acompanhamentos);
	CALL usp_sessoes_alterar_em_massa(p_sessoes_atualizadas);
END;
$BODY$;
ALTER PROCEDURE public.usp_paciente_alterar_acompanhamentos_com_sessoes(jsonb, jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_paciente_inserir(character varying, character varying, date, integer, integer, jsonb, jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_paciente_inserir(character varying, character varying, date, integer, integer, jsonb, jsonb);

CREATE OR REPLACE PROCEDURE public.usp_paciente_inserir(
	IN p_nome character varying,
	IN p_email character varying,
	IN p_data_nascimento date,
	IN p_id_pesquisador integer,
	IN p_id_fisioterapeuta integer,
	IN p_disponibilidades jsonb,
	IN p_restricoes jsonb,
	OUT p_id_paciente integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_disp jsonb;
    v_hor  text;
    v_dt   timestamp;
    v_id_disponibilidade integer;
    v_id_restricao integer;
    v_dia smallint;
    v_time time;
BEGIN
    IF p_email IS NULL OR length(trim(p_email)) = 0 THEN
        RAISE EXCEPTION 'p_email não pode ser NULL/vazio';
    END IF;

    IF p_nome IS NULL OR length(trim(p_nome)) = 0 THEN
        RAISE EXCEPTION 'p_nome não pode ser NULL/vazio';
    END IF;

    INSERT INTO public.pessoa(email, nome, data_nascimento, inserido_em)
    VALUES (trim(p_email), trim(p_nome), p_data_nascimento, now())
    RETURNING id_pessoa INTO p_id_paciente;

    INSERT INTO public.paciente(id_paciente, status_abandono, status_conclusao, inserido_em)
    VALUES (p_id_paciente, false, false, now());

    IF p_id_pesquisador IS NOT NULL OR p_id_fisioterapeuta IS NOT NULL THEN
        INSERT INTO public.acompanhamento_paciente(id_paciente, id_pesquisador, id_fisioterapeuta)
        VALUES (p_id_paciente, p_id_pesquisador, p_id_fisioterapeuta);
    END IF;

    -- disponibilidades
    IF p_disponibilidades IS NOT NULL AND jsonb_typeof(p_disponibilidades) = 'array' THEN
        FOR v_disp IN SELECT * FROM jsonb_array_elements(p_disponibilidades)
        LOOP
            v_dia := (v_disp->>'dia')::smallint;

            FOR v_hor IN SELECT * FROM jsonb_array_elements_text(v_disp->'horarios')
            LOOP
                v_time := v_hor::time without time zone;

                SELECT ds.id_disponibilidade
                  INTO v_id_disponibilidade
                  FROM public.disponibilidade_semanal ds
                 WHERE ds.dia_semana = v_dia
                   AND ds.inicio = v_time
                   -- Não leva o fim em consideração: AND ds.fim = (v_time + interval '1 hour')::time
                 LIMIT 1;

                IF v_id_disponibilidade IS NULL THEN
                    INSERT INTO public.disponibilidade_semanal(dia_semana, inicio, fim, inserido_em)
                    VALUES (v_dia, v_time, (v_time + interval '1 hour')::time without time zone, now())
                    RETURNING id_disponibilidade INTO v_id_disponibilidade;
                END IF;

                INSERT INTO public.disponibilidade_semanal_paciente(id_paciente, id_disponibilidade, ativa)
                VALUES (p_id_paciente, v_id_disponibilidade, true)
                ON CONFLICT (id_paciente, id_disponibilidade)
                DO UPDATE SET ativa = EXCLUDED.ativa;
            END LOOP;
        END LOOP;
    END IF;

    -- restrições
    IF p_restricoes IS NOT NULL AND jsonb_typeof(p_restricoes) = 'array' THEN
        FOR v_hor IN SELECT * FROM jsonb_array_elements_text(p_restricoes)
        LOOP
            v_dt := v_hor::timestamp without time zone;

			SELECT ra.id_restricao
			  INTO v_id_restricao
			  FROM public.restricao_agendamento ra
			 WHERE ra.inicio = v_dt
			   -- Não leva o fim em consideração: AND ra.fim = (v_dt + interval '1 hour')::time
			 LIMIT 1;

			IF v_id_restricao IS NULL THEN
				INSERT INTO public.restricao_agendamento(inicio, fim, motivo, inserido_em)
            	VALUES (v_dt, v_dt + interval '1 hour', 'restrição genérica', now())
            	RETURNING id_restricao INTO v_id_restricao;
			END IF;

            INSERT INTO public.restricao_agendamento_paciente(id_paciente, id_restricao, ativa)
            VALUES (p_id_paciente, v_id_restricao, true)
			ON CONFLICT (id_paciente, id_restricao)
            DO UPDATE SET ativa = EXCLUDED.ativa;
        END LOOP;
    END IF;
END;
$BODY$;
ALTER PROCEDURE public.usp_paciente_inserir(character varying, character varying, date, integer, integer, jsonb, jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_usuario_alterar(integer, character varying, character varying, date, character varying, character varying, boolean, jsonb, jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_usuario_alterar(integer, character varying, character varying, date, character varying, character varying, boolean, jsonb, jsonb);

CREATE OR REPLACE PROCEDURE public.usp_usuario_alterar(
	IN p_id_usuario integer,
	IN p_email character varying,
	IN p_nome character varying,
	IN p_data_nascimento date,
	IN p_login character varying,
	IN p_senha character varying,
	IN p_ativo boolean,
	IN p_disponibilidades jsonb,
	IN p_restricoes jsonb)
LANGUAGE 'plpgsql'
AS $BODY$
declare
	v_disp                 jsonb;
    v_hor                   text;
    v_dt               timestamp;
    v_dia               smallint;
    v_time                  time;
    v_id_disponibilidade integer;
	v_ids_disp         integer[];
    v_id_restricao       integer;
	v_ids_restr        integer[];
begin
	if not exists (select 1 from public.usuario us where us.id_usuario = p_id_usuario) then
		raise exception 'Nenhum usuário com o ID %', p_id_usuario;
	end if;
	
	if (p_email is not null and length(trim(p_email)) > 0)
	 or (p_nome is not null and length(trim(p_nome)) > 0)
	 or p_data_nascimento is not null
	then
		update public.pessoa
		set
		  email = coalesce(nullif(trim(p_email), ''), email),
		  nome  = coalesce(nullif(trim(p_nome), ''), nome),
		  data_nascimento = coalesce(p_data_nascimento, data_nascimento),
		  atualizado_em = now()
		where id_pessoa = p_id_usuario;
	end if;
	
	if (p_login is not null and length(trim(p_login)) > 0)
	 or (p_senha is not null and length(trim(p_senha)) > 0)
	 or p_ativo is not null
	then
		update public.usuario u
		set
		  login = coalesce(nullif(trim(p_login), ''), login),
		  senha = coalesce(nullif(trim(p_senha), ''), senha),
		  ativo = coalesce(p_ativo, ativo),
		  atualizado_em = now()
		where u.id_usuario = p_id_usuario;
	end if;

  	-- disponibilidades
	IF p_disponibilidades IS NOT NULL AND jsonb_typeof(p_disponibilidades) = 'array' THEN
		v_ids_disp := array[]::integer[];
	
		FOR v_disp IN SELECT * FROM jsonb_array_elements(p_disponibilidades)
		LOOP
			v_dia := (v_disp->>'dia')::smallint;
	
			FOR v_hor IN SELECT * FROM jsonb_array_elements_text(v_disp->'horarios')
			LOOP
				v_time := v_hor::time without time zone;
	
				SELECT ds.id_disponibilidade
				  INTO v_id_disponibilidade
				  FROM public.disponibilidade_semanal ds
				 WHERE ds.dia_semana = v_dia
				   AND ds.inicio = v_time
				   -- Não leva o fim em consideração: AND ds.fim = (v_time + interval '1 hour')::time
				 LIMIT 1;
	
				IF v_id_disponibilidade IS NULL THEN
					INSERT INTO public.disponibilidade_semanal(dia_semana, inicio, fim, inserido_em)
					VALUES (v_dia, v_time, (v_time + interval '1 hour')::time without time zone, now())
					RETURNING id_disponibilidade INTO v_id_disponibilidade;
				END IF;
	
				INSERT INTO public.disponibilidade_semanal_usuario(id_usuario, id_disponibilidade, ativa)
				VALUES (p_id_usuario, v_id_disponibilidade, true)
				ON CONFLICT (id_usuario, id_disponibilidade)
				DO UPDATE SET ativa = EXCLUDED.ativa;

				v_ids_disp := array_append(v_ids_disp, v_id_disponibilidade);
			END LOOP;
		END LOOP;

		UPDATE public.disponibilidade_semanal_usuario
		SET ativa = false
		WHERE id_usuario = p_id_usuario
		AND (
			array_length(v_ids_disp, 1) IS NULL
			OR
			(
				array_length(v_ids_disp, 1) IS NOT NULL
				AND
				NOT (id_disponibilidade = ANY(v_ids_disp))
			)
		);
	END IF;
	
	-- restrições
	IF p_restricoes IS NOT NULL AND jsonb_typeof(p_restricoes) = 'array' THEN
		v_ids_restr := array[]::integer[];
	
		FOR v_hor IN SELECT * FROM jsonb_array_elements_text(p_restricoes)
		LOOP
			v_dt := v_hor::timestamp without time zone;
	
			SELECT ra.id_restricao
			  INTO v_id_restricao
			  FROM public.restricao_agendamento ra
			 WHERE ra.inicio = v_dt
			   -- Não leva o fim em consideração: AND ra.fim = (v_dt + interval '1 hour')::time
			 LIMIT 1;
	
			IF v_id_restricao IS NULL THEN
				INSERT INTO public.restricao_agendamento(inicio, fim, motivo, inserido_em)
				VALUES (v_dt, v_dt + interval '1 hour', 'restrição genérica', now())
				RETURNING id_restricao INTO v_id_restricao;
			END IF;
	
			INSERT INTO public.restricao_agendamento_usuario(id_usuario, id_restricao, ativa)
			VALUES (p_id_usuario, v_id_restricao, true)
			ON CONFLICT (id_usuario, id_restricao)
			DO UPDATE SET ativa = EXCLUDED.ativa;

			v_ids_restr := array_append(v_ids_restr, v_id_restricao);
		END LOOP;

		UPDATE restricao_agendamento_usuario
		SET ativa = false
		WHERE id_usuario = p_id_usuario
		AND (
			array_length(v_ids_restr, 1) IS NULL
			OR
			(
				array_length(v_ids_restr, 1) IS NOT NULL
				AND
				NOT (id_restricao = ANY(v_ids_restr))
			)
		);
	END IF;
end 
$BODY$;
ALTER PROCEDURE public.usp_usuario_alterar(integer, character varying, character varying, date, character varying, character varying, boolean, jsonb, jsonb)
    OWNER TO postgres;

-- PROCEDURE: public.usp_usuario_inserir(character varying, character varying, date, integer, character varying, character varying, boolean, jsonb, jsonb)

-- DROP PROCEDURE IF EXISTS public.usp_usuario_inserir(character varying, character varying, date, integer, character varying, character varying, boolean, jsonb, jsonb);

CREATE OR REPLACE PROCEDURE public.usp_usuario_inserir(
	IN p_email character varying,
	IN p_nome character varying,
	IN p_data_nascimento date,
	IN p_tipo integer,
	IN p_login character varying,
	IN p_senha character varying,
	IN p_ativo boolean,
	IN p_disponibilidades jsonb,
	IN p_restricoes jsonb,
	OUT p_id_usuario integer)
LANGUAGE 'plpgsql'
AS $BODY$
declare
	v_disp jsonb;
    v_hor  text;
    v_dt   timestamp;
    v_id_disponibilidade integer;
    v_id_restricao integer;
    v_dia smallint;
    v_time time;
begin
	if p_tipo = coalesce((
		select ut.id_tipo from usuario_tipo ut
		where ut.nome ilike '%admin%'
	), 0) and (
		p_restricoes is not null
		or
		p_disponibilidades is not null
	) then
		raise exception 'Admins não possuem disponibilidades nem restrições de agendamento!';
	end if;

	if p_email is null or length(trim(p_email)) = 0 then
		raise exception 'p_email não pode ser NULL/vazio';
	end if;
	
	if p_nome is null or length(trim(p_nome)) = 0 then
		raise exception 'p_nome não pode ser NULL/vazio';
	end if;
	
	if p_login is null or length(trim(p_login)) = 0 then
		raise exception 'p_login é obrigatório';
	end if;
	
	if p_senha is null or length(trim(p_senha)) = 0 then
		raise exception 'p_senha é obrigatória';
	end if;
	
	if p_tipo is null then
		raise exception 'p_tipo é obrigatório';
	end if;
	
	if not exists (select 1 from public.usuario_tipo where id_tipo = p_tipo) then
		raise exception 'Tipo de usuário inválido: %', p_tipo;
	end if;
	
	insert into public.pessoa(email, nome, data_nascimento, inserido_em)
	values (trim(p_email), trim(p_nome), p_data_nascimento, now())
	returning id_pessoa into p_id_usuario;
	
	insert into public.usuario(id_usuario, tipo, login, senha, ativo, inserido_em)
	values (
		p_id_usuario,
		p_tipo,
		trim(p_login),
		p_senha,
		coalesce(p_ativo, true),
		now()
	);

	-- disponibilidades
	IF p_disponibilidades IS NOT NULL AND jsonb_typeof(p_disponibilidades) = 'array' THEN
		FOR v_disp IN SELECT * FROM jsonb_array_elements(p_disponibilidades)
		LOOP
			v_dia := (v_disp->>'dia')::smallint;
	
			FOR v_hor IN SELECT * FROM jsonb_array_elements_text(v_disp->'horarios')
			LOOP
				v_time := v_hor::time without time zone;
	
				SELECT ds.id_disponibilidade
				  INTO v_id_disponibilidade
				  FROM public.disponibilidade_semanal ds
				 WHERE ds.dia_semana = v_dia
				   AND ds.inicio = v_time
				   -- Não leva o fim em consideração: AND ds.fim = (v_time + interval '1 hour')::time
				 LIMIT 1;
	
				IF v_id_disponibilidade IS NULL THEN
					INSERT INTO public.disponibilidade_semanal(dia_semana, inicio, fim, inserido_em)
					VALUES (v_dia, v_time, (v_time + interval '1 hour')::time without time zone, now())
					RETURNING id_disponibilidade INTO v_id_disponibilidade;
				END IF;
	
				INSERT INTO public.disponibilidade_semanal_usuario(id_usuario, id_disponibilidade, ativa)
				VALUES (p_id_usuario, v_id_disponibilidade, true)
				ON CONFLICT (id_usuario, id_disponibilidade)
				DO UPDATE SET ativa = EXCLUDED.ativa;
			END LOOP;
		END LOOP;
	END IF;
	
	-- restrições
	IF p_restricoes IS NOT NULL AND jsonb_typeof(p_restricoes) = 'array' THEN
		FOR v_hor IN SELECT * FROM jsonb_array_elements_text(p_restricoes)
		LOOP
			v_dt := v_hor::timestamp without time zone;
	
			SELECT ra.id_restricao
			  INTO v_id_restricao
			  FROM public.restricao_agendamento ra
			 WHERE ra.inicio = v_dt
			   -- Não leva o fim em consideração: AND ra.fim = (v_dt + interval '1 hour')::time
			 LIMIT 1;
	
			IF v_id_restricao IS NULL THEN
				INSERT INTO public.restricao_agendamento(inicio, fim, motivo, inserido_em)
				VALUES (v_dt, v_dt + interval '1 hour', 'restrição genérica', now())
				RETURNING id_restricao INTO v_id_restricao;
			END IF;
	
			INSERT INTO public.restricao_agendamento_usuario(id_usuario, id_restricao, ativa)
			VALUES (p_id_usuario, v_id_restricao, true)
			ON CONFLICT (id_usuario, id_restricao)
			DO UPDATE SET ativa = EXCLUDED.ativa;
		END LOOP;
	END IF;
end 
$BODY$;
ALTER PROCEDURE public.usp_usuario_inserir(character varying, character varying, date, integer, character varying, character varying, boolean, jsonb, jsonb)
    OWNER TO postgres;
