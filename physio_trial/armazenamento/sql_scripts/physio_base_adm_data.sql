insert into public.pessoa (email, nome, data_nascimento, inserido_em, atualizado_em)
values
  ('admin@usp.com', 'Admin USP', '1990-01-10', now(), null)
on conflict (email) do nothing;

insert into public.usuario (id_usuario, tipo, login, senha, inserido_em, atualizado_em, ativo)
select
  id_pessoa,
  (select id_tipo from public.usuario_tipo where nome ilike '%admin%'),
  'admin',
  '$2b$12$ftZTRST5DiXy5HaZpourkOoZ52NdzCkQC1NHsV9SfJm0bkAZBMiIq', -- senha "batata"
  now(), null, true
from public.pessoa
  where email = 'admin@usp.com'
on conflict (id_usuario) do nothing;

select * from usuario;
