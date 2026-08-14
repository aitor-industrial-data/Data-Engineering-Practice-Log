-- =====================================================================
-- Título: Usuarios Activos Mensuales (MAU) - Facebook (Julio 2022)
-- Motor objetivo: PostgreSQL / Estándar SQL
-- =====================================================================

/*
=====================================================================
Descripción del Problema:
---------------------------------------------------------------------
Supón que se te proporciona una tabla con información sobre las 
acciones de los usuarios en Facebook. Escribe una consulta SQL para 
obtener el número de Usuarios Activos Mensuales (MAUs) en julio de 2022, 
mostrando el mes en formato numérico (por ejemplo: 1, 2, 3...).

Pista: Un usuario activo se define como aquel usuario que ha realizado 
acciones (como 'sign-in', 'like' o 'comment') tanto en el mes actual 
como en el mes anterior.
=====================================================================
*/

with month as (
SELECT*,
  EXTRACT(MONTH FROM event_date) as month,
  EXTRACT(MONTH FROM event_date)-1 as last_month
FROM user_actions
)


select m.month,
  count(DISTINCT(m.user_id)) as monthly_active_users
FROM month m
left join month lm on m.last_month = lm.month and m.user_id = lm.user_id
where lm.user_id is not null and m.month=7
group by m.month
;