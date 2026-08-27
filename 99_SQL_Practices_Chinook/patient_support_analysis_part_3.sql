
-- Plataforma: DataLemur (UnitedHealth Group SQL Interview Question)
-- Dificultad: Media

/*
===============================================================================
ENUNCIADO DEL PROBLEMA: Patient Support Analysis (Part 3)
===============================================================================

UnitedHealth Group (UHG) tiene un programa llamado Advocate4Me que permite a los 
asegurados (miembros) llamar a un asesor y recibir soporte para sus necesidades 
de atención médica (reclamaciones, cobertura de medicamentos, autorizaciones, etc.).

Escribe una consulta en SQL para obtener el número de llamadas/usuarios únicos 
(policy_holder_id) que realizaron una llamada dentro de un intervalo de 7 días 
respecto a su llamada anterior. 

Si un usuario realizó más de dos llamadas dentro del período de 7 días, debes 
contarlo SOLO UNA VEZ en el resultado final.

ESQUEMA DE LA TABLA (callers):
-------------------------------------------------------------------------------
Columna            | Tipo
-------------------------------------------------------------------------------
policy_holder_id   | integer
case_id            | varchar
call_category      | varchar
call_date          | timestamp
call_duration_secs | integer
-------------------------------------------------------------------------------
*/

WITH previous_calls AS (
  SELECT 
    policy_holder_id,
    call_date,
    LAG(call_date) OVER (
      PARTITION BY policy_holder_id 
      ORDER BY call_date ASC
    ) AS prev_call_date
  FROM callers
)
SELECT 
  COUNT(DISTINCT policy_holder_id) AS policy_holder_count
FROM previous_calls
WHERE prev_call_date IS NOT NULL 
  AND call_date <= prev_call_date + INTERVAL '7 days';