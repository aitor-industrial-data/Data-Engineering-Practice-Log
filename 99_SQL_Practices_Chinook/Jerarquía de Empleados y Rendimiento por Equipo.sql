
/*
================================================================================
EJERCICIO SQL: BASE DE DATOS CHINOOK
Reto: Jerarquía de Empleados y Rendimiento por Equipo (Self-Join)
================================================================================

CONTEXTO:
El departamento de Recursos Humanos de Chinook quiere evaluar la estructura 
organizativa de la empresa y medir el impacto comercial de cada Manager / 
Supervisor. Para ello, necesitan un informe que identifique a todos los 
empleados que tienen personal a su cargo y calcule el rendimiento total en 
ventas generado por su equipo directo.

--------------------------------------------------------------------------------
ENUNCIADO:
Escribe una consulta SQL que devuelva una lista con todos los empleados que 
ejerzan como supervisores/managers (aquellos cuyo EmployeeId aparezca en el 
campo ReportsTo de otros empleados) y agregue las ventas de sus subordinados 
directos.

REQUISITOS DE LA CONSULTA:

1. Self-Join (Autounión):
   - Une la tabla Employee consigo misma para conectar a cada supervisor 
     (e_manager) con sus empleados directos (e_subordinate) mediante la condición:
     e_manager.EmployeeId = e_subordinate.ReportsTo

2. Cálculo de Ventas del Equipo:
   - Las ventas se obtienen a través de los clientes asignados a los empleados 
     subordinados: Invoice -> Customer (donde Customer.SupportRepId = e_subordinate.EmployeeId).
   - Atención: Debe utilizarse un LEFT JOIN para calcular las ventas, de modo que 
     si un manager tiene subordinados que no gestionan clientes directamente 
     (por ejemplo, personal de TI), el manager siga apareciendo en el resultado 
     con $0.00 en ventas.

3. Columnas de salida:
   - ManagerId: ID del manager (e_manager.EmployeeId).
   - NombreManager: Nombre completo concatenado (e_manager.FirstName + ' ' + e_manager.LastName).
   - CargoManager: Cargo del supervisor (e_manager.Title).
   - NumSubordinados: Número total de empleados directos a su cargo 
     (COUNT(DISTINCT e_subordinate.EmployeeId)).
   - TotalVentasEquipo: Suma total facturada ($) por los clientes asignados a 
     sus subordinados directos, redondeada a 2 decimales 
     (COALESCE(ROUND(SUM(i.Total), 2), 0.00)).

4. Filtrado y Ordenación:
   - Muestra únicamente empleados que tengan al menos 1 subordinado directo.
   - Ordena el resultado de mayor a menor según el TotalVentasEquipo.

--------------------------------------------------------------------------------
PISTAS CONCEPTUALES:
1. La estructura básica de la autounión es:
   FROM Employee e_manager
   INNER JOIN Employee e_subordinate ON e_manager.EmployeeId = e_subordinate.ReportsTo
2. Continúa la cadena de uniones desde e_subordinate con:
   LEFT JOIN Customer c ON e_subordinate.EmployeeId = c.SupportRepId
   LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
3. Agrupa por las columnas descriptivas del manager:
   (e_manager.EmployeeId, e_manager.FirstName, e_manager.LastName, e_manager.Title).
================================================================================
*/


WITH EquipoManager AS (
    -- 1. Relacionamos cada Manager con sus Subordinados Directos
    SELECT 
        sup.EmployeeId AS ManagerId,
        sup.FirstName || ' ' || sup.LastName AS NombreManager,
        sup.Title AS CargoManager,
        sub.EmployeeId AS SubordinateId
    FROM Employee sup
    INNER JOIN Employee sub ON sub.ReportsTo = sup.EmployeeId
)

-- 2. Conectamos los subordinados con sus ventas (usando LEFT JOIN)
SELECT 
    em.ManagerId,
    em.NombreManager,
    em.CargoManager,
    COUNT(DISTINCT em.SubordinateId) AS NumSubordinados,
    COALESCE(ROUND(SUM(i.Total), 2), 0.00) AS TotalVentasEquipo
FROM EquipoManager em
LEFT JOIN Customer c ON c.SupportRepId = em.SubordinateId
LEFT JOIN Invoice i ON i.CustomerId = c.CustomerId
GROUP BY em.ManagerId, em.NombreManager, em.CargoManager
ORDER BY TotalVentasEquipo DESC;


;