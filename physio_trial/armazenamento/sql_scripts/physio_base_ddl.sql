--
-- PostgreSQL database dump
--

--
-- TOC entry 238 (class 1259 OID 16598)
-- Name: acompanhamento_paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acompanhamento_paciente (
    id_paciente integer NOT NULL,
    id_pesquisador integer,
    id_fisioterapeuta integer,
    CONSTRAINT ck_acp_pesq_fisio_distintos CHECK ((id_fisioterapeuta <> id_pesquisador))
);


ALTER TABLE public.acompanhamento_paciente OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16568)
-- Name: auditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoria (
    id_auditoria integer NOT NULL,
    id_usuario_auditado integer NOT NULL,
    id_tabela integer NOT NULL,
    data_hora timestamp without time zone NOT NULL,
    tupla_inicial jsonb NOT NULL,
    tupla_final jsonb NOT NULL,
    sincronizado boolean
);


ALTER TABLE public.auditoria OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16567)
-- Name: auditoria_id_auditoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auditoria ALTER COLUMN id_auditoria ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.auditoria_id_auditoria_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 239 (class 1259 OID 16620)
-- Name: codigo_sessao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.codigo_sessao (
    id_codigo integer NOT NULL,
    codigo character varying(3) NOT NULL
);

ALTER TABLE public.codigo_sessao OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16512)
-- Name: dia_semana; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dia_semana (
    id_dia smallint NOT NULL,
    nome character varying(19) NOT NULL,
    CONSTRAINT ck_dia_semana_range CHECK (((id_dia >= 0) AND (id_dia <= 6)))
);


ALTER TABLE public.dia_semana OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16518)
-- Name: disponibilidade_semanal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disponibilidade_semanal (
    id_disponibilidade integer NOT NULL,
    dia_semana smallint NOT NULL,
    inicio time without time zone NOT NULL,
    fim time without time zone NOT NULL,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone,
    CONSTRAINT ck_ds_intervalo CHECK ((inicio < fim))
);


ALTER TABLE public.disponibilidade_semanal OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16517)
-- Name: disponibilidade_semanal_id_disponibilidade_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.disponibilidade_semanal ALTER COLUMN id_disponibilidade ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.disponibilidade_semanal_id_disponibilidade_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 232 (class 1259 OID 16530)
-- Name: disponibilidade_semanal_paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disponibilidade_semanal_paciente (
    id_paciente integer NOT NULL,
    id_disponibilidade integer NOT NULL,
    ativa boolean
);


ALTER TABLE public.disponibilidade_semanal_paciente OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16545)
-- Name: disponibilidade_semanal_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disponibilidade_semanal_usuario (
    id_usuario integer NOT NULL,
    id_disponibilidade integer NOT NULL,
    ativa boolean
);


ALTER TABLE public.disponibilidade_semanal_usuario OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16561)
-- Name: nome_tabela; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nome_tabela (
    id_nome_tabela integer NOT NULL,
    nome character varying(55) NOT NULL
);


ALTER TABLE public.nome_tabela OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16560)
-- Name: nome_tabela_id_nome_tabela_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.nome_tabela ALTER COLUMN id_nome_tabela ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.nome_tabela_id_nome_tabela_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 16398)
-- Name: paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente (
    id_paciente integer NOT NULL,
    status_abandono boolean,
    status_conclusao boolean,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone
);


ALTER TABLE public.paciente OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: pessoa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pessoa (
    id_pessoa integer NOT NULL,
    email character varying(100) NOT NULL,
    nome character varying(100) NOT NULL,
    data_nascimento date,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone
);


ALTER TABLE public.pessoa OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: pessoa_id_pessoa_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.pessoa ALTER COLUMN id_pessoa ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.pessoa_id_pessoa_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 16468)
-- Name: restricao_agendamento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restricao_agendamento (
    id_restricao integer NOT NULL,
    inicio timestamp without time zone NOT NULL,
    fim timestamp without time zone NOT NULL,
    motivo text,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone,
    CONSTRAINT ck_ra_intervalo CHECK ((inicio < fim))
);


ALTER TABLE public.restricao_agendamento OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16467)
-- Name: restricao_agendamento_id_restricao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.restricao_agendamento ALTER COLUMN id_restricao ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.restricao_agendamento_id_restricao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 16482)
-- Name: restricao_agendamento_paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restricao_agendamento_paciente (
    id_paciente integer NOT NULL,
    id_restricao integer NOT NULL,
    ativa boolean
);


ALTER TABLE public.restricao_agendamento_paciente OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16497)
-- Name: restricao_agendamento_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restricao_agendamento_usuario (
    id_usuario integer NOT NULL,
    id_restricao integer NOT NULL,
    ativa boolean
);


ALTER TABLE public.restricao_agendamento_usuario OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16456)
-- Name: sessao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessao (
    id_sessao integer NOT NULL,
    id_paciente integer NOT NULL,
    dia date NOT NULL,
    horario time without time zone NOT NULL,
    status_agendamento boolean,
    conclusao boolean NOT NULL,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone,
    codigo integer
);


ALTER TABLE public.sessao OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16455)
-- Name: sessao_id_sessao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.sessao ALTER COLUMN id_sessao ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sessao_id_sessao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 16416)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    tipo integer NOT NULL,
    login character varying(29) NOT NULL,
    senha character varying(29) NOT NULL,
    inserido_em timestamp without time zone NOT NULL,
    atualizado_em timestamp without time zone,
    ativo boolean
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16409)
-- Name: usuario_tipo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_tipo (
    id_tipo integer NOT NULL,
    nome character varying(19) NOT NULL
);


ALTER TABLE public.usuario_tipo OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16433)
-- Name: usuario_tipo_historico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_tipo_historico (
    id_mudanca integer NOT NULL,
    id_usuario_atualizado integer NOT NULL,
    instante_mudanca timestamp without time zone NOT NULL,
    tipo_novo integer NOT NULL,
    tipo_antigo integer NOT NULL,
    CONSTRAINT ck_uth_tipos_diferentes CHECK ((tipo_novo <> tipo_antigo))
);


ALTER TABLE public.usuario_tipo_historico OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16432)
-- Name: usuario_tipo_historico_id_mudanca_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_tipo_historico ALTER COLUMN id_mudanca ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usuario_tipo_historico_id_mudanca_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 218 (class 1259 OID 16408)
-- Name: usuario_tipo_id_tipo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_tipo ALTER COLUMN id_tipo ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usuario_tipo_id_tipo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

--
-- TOC entry 3586 (class 0 OID 0)
-- Dependencies: 236
-- Name: auditoria_id_auditoria_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auditoria_id_auditoria_seq', 1, false);


--
-- TOC entry 3587 (class 0 OID 0)
-- Dependencies: 230
-- Name: disponibilidade_semanal_id_disponibilidade_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.disponibilidade_semanal_id_disponibilidade_seq', 1, false);


--
-- TOC entry 3588 (class 0 OID 0)
-- Dependencies: 234
-- Name: nome_tabela_id_nome_tabela_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nome_tabela_id_nome_tabela_seq', 1, false);


--
-- TOC entry 3589 (class 0 OID 0)
-- Dependencies: 215
-- Name: pessoa_id_pessoa_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pessoa_id_pessoa_seq', 1, false);


--
-- TOC entry 3590 (class 0 OID 0)
-- Dependencies: 225
-- Name: restricao_agendamento_id_restricao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.restricao_agendamento_id_restricao_seq', 1, false);


--
-- TOC entry 3591 (class 0 OID 0)
-- Dependencies: 223
-- Name: sessao_id_sessao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessao_id_sessao_seq', 1, false);


--
-- TOC entry 3592 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuario_tipo_historico_id_mudanca_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_tipo_historico_id_mudanca_seq', 1, false);


--
-- TOC entry 3593 (class 0 OID 0)
-- Dependencies: 218
-- Name: usuario_tipo_id_tipo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_tipo_id_tipo_seq', 1, true);


--
-- TOC entry 3386 (class 2606 OID 16603)
-- Name: acompanhamento_paciente acompanhamento_paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acompanhamento_paciente
    ADD CONSTRAINT acompanhamento_paciente_pkey PRIMARY KEY (id_paciente);


--
-- TOC entry 3382 (class 2606 OID 16574)
-- Name: auditoria auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT auditoria_pkey PRIMARY KEY (id_auditoria);


--
-- TOC entry 3388 (class 2606 OID 16624)
-- Name: codigo_sessao codigo_sessao_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.codigo_sessao
    ADD CONSTRAINT codigo_sessao_codigo_key UNIQUE (codigo);


--
-- TOC entry 3390 (class 2606 OID 16626)
-- Name: codigo_sessao codigo_sessao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.codigo_sessao
    ADD CONSTRAINT codigo_sessao_pkey PRIMARY KEY (id_codigo);


--
-- TOC entry 3370 (class 2606 OID 16516)
-- Name: dia_semana dia_semana_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dia_semana
    ADD CONSTRAINT dia_semana_pkey PRIMARY KEY (id_dia);


--
-- TOC entry 3375 (class 2606 OID 16534)
-- Name: disponibilidade_semanal_paciente disponibilidade_semanal_paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_paciente
    ADD CONSTRAINT disponibilidade_semanal_paciente_pkey PRIMARY KEY (id_paciente, id_disponibilidade);


--
-- TOC entry 3372 (class 2606 OID 16523)
-- Name: disponibilidade_semanal disponibilidade_semanal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal
    ADD CONSTRAINT disponibilidade_semanal_pkey PRIMARY KEY (id_disponibilidade);


--
-- TOC entry 3377 (class 2606 OID 16549)
-- Name: disponibilidade_semanal_usuario disponibilidade_semanal_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_usuario
    ADD CONSTRAINT disponibilidade_semanal_usuario_pkey PRIMARY KEY (id_usuario, id_disponibilidade);


--
-- TOC entry 3379 (class 2606 OID 16565)
-- Name: nome_tabela nome_tabela_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nome_tabela
    ADD CONSTRAINT nome_tabela_pkey PRIMARY KEY (id_nome_tabela);


--
-- TOC entry 3349 (class 2606 OID 16402)
-- Name: paciente paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id_paciente);


--
-- TOC entry 3345 (class 2606 OID 16396)
-- Name: pessoa pessoa_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_email_key UNIQUE (email);


--
-- TOC entry 3347 (class 2606 OID 16394)
-- Name: pessoa pessoa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_pkey PRIMARY KEY (id_pessoa);


--
-- TOC entry 3366 (class 2606 OID 16486)
-- Name: restricao_agendamento_paciente restricao_agendamento_paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_paciente
    ADD CONSTRAINT restricao_agendamento_paciente_pkey PRIMARY KEY (id_paciente, id_restricao);


--
-- TOC entry 3364 (class 2606 OID 16475)
-- Name: restricao_agendamento restricao_agendamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento
    ADD CONSTRAINT restricao_agendamento_pkey PRIMARY KEY (id_restricao);


--
-- TOC entry 3368 (class 2606 OID 16501)
-- Name: restricao_agendamento_usuario restricao_agendamento_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_usuario
    ADD CONSTRAINT restricao_agendamento_usuario_pkey PRIMARY KEY (id_usuario, id_restricao);


--
-- TOC entry 3362 (class 2606 OID 16460)
-- Name: sessao sessao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessao
    ADD CONSTRAINT sessao_pkey PRIMARY KEY (id_sessao);


--
-- TOC entry 3356 (class 2606 OID 16420)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3359 (class 2606 OID 16438)
-- Name: usuario_tipo_historico usuario_tipo_historico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo_historico
    ADD CONSTRAINT usuario_tipo_historico_pkey PRIMARY KEY (id_mudanca);


--
-- TOC entry 3351 (class 2606 OID 16415)
-- Name: usuario_tipo usuario_tipo_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo
    ADD CONSTRAINT usuario_tipo_nome_key UNIQUE (nome);


--
-- TOC entry 3353 (class 2606 OID 16413)
-- Name: usuario_tipo usuario_tipo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo
    ADD CONSTRAINT usuario_tipo_pkey PRIMARY KEY (id_tipo);


--
-- TOC entry 3383 (class 1259 OID 16586)
-- Name: idx_auditoria_tabela_data; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_auditoria_tabela_data ON public.auditoria USING btree (id_tabela, data_hora);


--
-- TOC entry 3384 (class 1259 OID 16585)
-- Name: idx_auditoria_usuario_data; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_auditoria_usuario_data ON public.auditoria USING btree (id_usuario_auditado, data_hora);


--
-- TOC entry 3373 (class 1259 OID 16529)
-- Name: idx_ds_dia_inicio_fim; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ds_dia_inicio_fim ON public.disponibilidade_semanal USING btree (dia_semana, inicio, fim);


--
-- TOC entry 3343 (class 1259 OID 16397)
-- Name: idx_pessoa_nome; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pessoa_nome ON public.pessoa USING btree (nome);


--
-- TOC entry 3360 (class 1259 OID 16466)
-- Name: idx_sessao_paciente_dia; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessao_paciente_dia ON public.sessao USING btree (id_paciente, dia);


--
-- TOC entry 3357 (class 1259 OID 16454)
-- Name: idx_uth_usuario_instante; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_uth_usuario_instante ON public.usuario_tipo_historico USING btree (id_usuario_atualizado, instante_mudanca);


--
-- TOC entry 3380 (class 1259 OID 16566)
-- Name: uq_nome_tabela_nome; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_nome_tabela_nome ON public.nome_tabela USING btree (nome);


--
-- TOC entry 3354 (class 1259 OID 16431)
-- Name: uq_usuario_login; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_usuario_login ON public.usuario USING btree (login);


--
-- TOC entry 3408 (class 2606 OID 16580)
-- Name: auditoria fk_auditoria_tabela; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT fk_auditoria_tabela FOREIGN KEY (id_tabela) REFERENCES public.nome_tabela(id_nome_tabela) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3409 (class 2606 OID 16575)
-- Name: auditoria fk_auditoria_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT fk_auditoria_usuario FOREIGN KEY (id_usuario_auditado) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3397 (class 2606 OID 16627)
-- Name: sessao fk_codigo_sessao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessao
    ADD CONSTRAINT fk_codigo_sessao FOREIGN KEY (codigo) REFERENCES public.codigo_sessao(id_codigo) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3403 (class 2606 OID 16524)
-- Name: disponibilidade_semanal fk_ds_dia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal
    ADD CONSTRAINT fk_ds_dia FOREIGN KEY (dia_semana) REFERENCES public.dia_semana(id_dia) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3404 (class 2606 OID 16540)
-- Name: disponibilidade_semanal_paciente fk_dsp_disp; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_paciente
    ADD CONSTRAINT fk_dsp_disp FOREIGN KEY (id_disponibilidade) REFERENCES public.disponibilidade_semanal(id_disponibilidade) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3405 (class 2606 OID 16535)
-- Name: disponibilidade_semanal_paciente fk_dsp_paciente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_paciente
    ADD CONSTRAINT fk_dsp_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3406 (class 2606 OID 16555)
-- Name: disponibilidade_semanal_usuario fk_dsu_disp; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_usuario
    ADD CONSTRAINT fk_dsu_disp FOREIGN KEY (id_disponibilidade) REFERENCES public.disponibilidade_semanal(id_disponibilidade) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3407 (class 2606 OID 16550)
-- Name: disponibilidade_semanal_usuario fk_dsu_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disponibilidade_semanal_usuario
    ADD CONSTRAINT fk_dsu_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3410 (class 2606 OID 16614)
-- Name: acompanhamento_paciente fk_id_fisioterapeuta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acompanhamento_paciente
    ADD CONSTRAINT fk_id_fisioterapeuta FOREIGN KEY (id_fisioterapeuta) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3411 (class 2606 OID 16604)
-- Name: acompanhamento_paciente fk_id_paciente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acompanhamento_paciente
    ADD CONSTRAINT fk_id_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3412 (class 2606 OID 16609)
-- Name: acompanhamento_paciente fk_id_pesquisador; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acompanhamento_paciente
    ADD CONSTRAINT fk_id_pesquisador FOREIGN KEY (id_pesquisador) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3391 (class 2606 OID 16403)
-- Name: paciente fk_paciente_pessoa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT fk_paciente_pessoa FOREIGN KEY (id_paciente) REFERENCES public.pessoa(id_pessoa) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3399 (class 2606 OID 16487)
-- Name: restricao_agendamento_paciente fk_rap_paciente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_paciente
    ADD CONSTRAINT fk_rap_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3400 (class 2606 OID 16492)
-- Name: restricao_agendamento_paciente fk_rap_restricao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_paciente
    ADD CONSTRAINT fk_rap_restricao FOREIGN KEY (id_restricao) REFERENCES public.restricao_agendamento(id_restricao) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3401 (class 2606 OID 16507)
-- Name: restricao_agendamento_usuario fk_rau_restricao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_usuario
    ADD CONSTRAINT fk_rau_restricao FOREIGN KEY (id_restricao) REFERENCES public.restricao_agendamento(id_restricao) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3402 (class 2606 OID 16502)
-- Name: restricao_agendamento_usuario fk_rau_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricao_agendamento_usuario
    ADD CONSTRAINT fk_rau_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3398 (class 2606 OID 16461)
-- Name: sessao fk_sessao_paciente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessao
    ADD CONSTRAINT fk_sessao_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3392 (class 2606 OID 16421)
-- Name: usuario fk_usuario_pessoa; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT fk_usuario_pessoa FOREIGN KEY (id_usuario) REFERENCES public.pessoa(id_pessoa) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3393 (class 2606 OID 16426)
-- Name: usuario fk_usuario_tipo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT fk_usuario_tipo FOREIGN KEY (tipo) REFERENCES public.usuario_tipo(id_tipo) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3394 (class 2606 OID 16449)
-- Name: usuario_tipo_historico fk_uth_tipo_antigo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo_historico
    ADD CONSTRAINT fk_uth_tipo_antigo FOREIGN KEY (tipo_antigo) REFERENCES public.usuario_tipo(id_tipo) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3395 (class 2606 OID 16444)
-- Name: usuario_tipo_historico fk_uth_tipo_novo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo_historico
    ADD CONSTRAINT fk_uth_tipo_novo FOREIGN KEY (tipo_novo) REFERENCES public.usuario_tipo(id_tipo) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3396 (class 2606 OID 16439)
-- Name: usuario_tipo_historico fk_uth_usuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_tipo_historico
    ADD CONSTRAINT fk_uth_usuario FOREIGN KEY (id_usuario_atualizado) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Completed on 2025-12-19 00:06:08

--
-- PostgreSQL database dump complete
--
