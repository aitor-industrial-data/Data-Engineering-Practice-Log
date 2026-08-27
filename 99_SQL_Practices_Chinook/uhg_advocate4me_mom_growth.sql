-- =============================================================================
-- Archivo: uhg_advocate4me_mom_growth.sql
-- Descripción: Cálculo de la tasa de crecimiento intermensual (MoM) para llamadas
--              de larga duración (> 300 segundos) en el programa Advocate4Me de UHG.
-- =============================================================================

/*
ENUNCIADO DEL PROBLEMA:
-----------------------
UnitedHealth Group (UHG) tiene un programa llamado Advocate4Me, el cual permite a los 
asegurados (o miembros) llamar a un asesor para recibir asistencia en sus necesidades 
de atención médica: soporte en reclamaciones y beneficios, cobertura de medicamentos, 
pre y post-autorizaciones, expedientes médicos, asistencia de emergencia o servicios 
del portal de miembros.

Para analizar el rendimiento del programa, escribe una consulta que determine la tasa 
de crecimiento mes a mes (MoM) específicamente para llamadas largas. Una llamada larga 
se define como cualquier llamada con una duración mayor a 5 minutos (300 segundos).

Muestra el año y el mes en formato numérico y en orden cronológico, junto con el 
porcentaje de crecimiento redondeado a 1 decimal.

TABLA: callers
- policy_holder_id : integer
- case_id          : varchar
- call_category    : varchar
- call_date        : timestamp
- call_duration_secs: integer
*/

WITH long_calls AS (
  SELECT 
    EXTRACT(YEAR FROM call_date) AS yr,
    EXTRACT(MONTH FROM call_date) AS mth,
    COUNT(case_id) AS curr_mth_calls,
    LAG(COUNT(case_id)) OVER (
      ORDER BY EXTRACT(MONTH FROM call_date)) AS prev_mth_calls
FROM callers
WHERE call_duration_secs > 300
GROUP BY 
  EXTRACT(YEAR FROM call_date),
  EXTRACT(MONTH FROM call_date)
)

SELECT
  yr,
  mth,
  ROUND(100.0 * 
    (curr_mth_calls - prev_mth_calls)/prev_mth_calls,1) AS long_calls_growth_pct
FROM long_calls
ORDER BY yr, mth;