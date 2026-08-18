/*
================================================================================
ENUNCIADO DEL PROBLEMA:
================================================================================
Se proporcionan dos tablas: 

1. `advertiser`: Contiene información sobre los anunciantes y su estado de pago.
2. `daily_pay`: Contiene la información de pago del día actual para los anunciantes 
   (solo incluye a los anunciantes que han realizado un pago hoy).

OBJETIVO:
Escribe una consulta para actualizar el estado de pago de los anunciantes basándote 
en la información de la tabla `daily_pay`. La salida debe incluir el ID de usuario 
(`user_id`) y su nuevo estado de pago (`new_status`), ordenada por el ID de usuario.

CATEGORÍAS DE ESTADO DE PAGO:
- NEW: Anunciantes recién registrados que han realizado su primer pago.
- EXISTING: Anunciantes que realizaron pagos en el pasado y han pagado hoy.
- CHURN: Anunciantes que realizaron pagos en el pasado pero NO han pagado hoy.
- RESURRECT: Anunciantes que estaban inactivitos/cancelados pero han vuelto a pagar hoy.

REGLAS Y TRANSICIONES DE ESTADO:
- Sin pago en el día T: Si un anunciante no realiza un pago hoy (no está en `daily_pay`), 
  independientemente de su estado anterior, su nuevo estado pasa a ser 'CHURN'.
- Con pago en el día T:
  * Si NO existía previamente en la tabla `advertiser`: Pasa a ser 'NEW'.
  * Si existía y su estado anterior era 'CHURN': Pasa a ser 'RESURRECT'.
  * Si existía y su estado anterior era 'NEW', 'EXISTING' o 'RESURRECT': Pasa a ser 'EXISTING'.
================================================================================
*/

SELECT 
    COALESCE(a.user_id, d.user_id) AS user_id,
    CASE 
        -- Sin pago hoy -> CHURN
        WHEN d.paid IS NULL THEN 'CHURN'
        
        -- Primer pago registrado (no existía en advertiser) -> NEW
        WHEN a.status IS NULL THEN 'NEW'
        
        -- Estaba en CHURN y vuelve a pagar -> RESURRECT
        WHEN a.status = 'CHURN' THEN 'RESURRECT'
        
        -- Pagó hoy y venía de NEW, EXISTING o RESURRECT -> EXISTING
        ELSE 'EXISTING'
    END AS new_status
FROM advertiser a
FULL OUTER JOIN daily_pay d 
    ON a.user_id = d.user_id
ORDER BY user_id ASC;