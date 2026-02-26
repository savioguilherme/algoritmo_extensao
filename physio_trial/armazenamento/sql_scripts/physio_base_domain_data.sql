insert into public.usuario_tipo(nome)
values ('Administrador'), ('Fisioterapeuta'), ('Pesquisador');

insert into public.nome_tabela(nome)
values ('acompanhamento_paciente'), ('disponibilidade_semanal'),
('disponibilidade_semanal_paciente'), ('disponibilidade_semanal_usuario'),
('paciente'), ('pessoa'), ('restricao_agendamento'), ('restricao_agendamento_paciente'),
('restricao_agendamento_usuario'), ('sessao'), ('usuario');

insert into public.dia_semana(id_dia, nome)
values (0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'),
(3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo');

insert into public.codigo_sessao(id_codigo, codigo)
values (1, 'S00'), (2, 'S01'), (3, 'S02'), (4, 'S03'),
(5, 'S04'), (6, 'S05'), (7, 'S06'), (8, 'S07'), (9, 'S08'),
(10, 'F00'), (11, 'F01');

select * from public.usuario_tipo;

select * from public.nome_tabela;

select * from public.dia_semana;

select * from public.codigo_sessao;
