"""
PROBLEMA INTEGRADOR: AUDITORÍA DE VENTAS Y COMISIONES DE VENDEDORES

Trabajas en el departamento de BI de una empresa. Debes procesar las ventas brutas ('ventas.csv')
y cruzarlas con la tabla de vendedores ('vendedores.csv') para generar un informe consolidado por departamento.

Entrada 1 ('vendedores.csv'):
vendedor_id,nombre,departamento,comision_pct
v_10,Ana Lopez,Electrónica,0.05
v_20,Carlos Ruiz,Hogar,0.03
v_30,Maria Gomez,Electrónica,0.05

Entrada 2 ('ventas.csv'):
venta_id,vendedor_id,monto_bruto,estado,fecha
vt_101,v_10,1000.00,COMPLETADA,2026-08-01
vt_102,v_20,500.00,COMPLETADA,2026-08-02
vt_103,v_10,200.00,CANCELADA,2026-08-03
vt_104,v_99,300.00,COMPLETADA,2026-08-04
vt_105,v_30,N/A,COMPLETADA,2026-08-05
vt_106,v_30,1500.00,COMPLETADA,2026-08-06

Requisitos de Limpieza y Negocio:
1. Indexación (Hash Join):
   - Carga 'vendedores.csv' en un mapa por 'vendedor_id'.
   - Convierte 'comision_pct' a float.

2. Filtrado y Validación de Ventas:
   - Descarta ventas donde 'estado' sea diferente de "COMPLETADA".
   - Limpia 'monto_bruto' a float. Descarta filas no numéricas o con monto <= 0.

3. Cruzado (LEFT JOIN) y Regla de Negocio:
   - Busca el vendedor en el mapa.
   - Si el 'vendedor_id' NO existe (ej. v_99):
     * 'departamento' = "SIN_ASIGNAR"
     * 'comision_generada' = 0.00
   - Si el vendedor EXISTE:
     * 'comision_generada' = monto_bruto * comision_pct

4. Agregación por Departamento (GROUP BY departamento):
   Para cada departamento calcula:
   - 'total_ventas_brutas': Suma de los montos de ventas válidas (redondeado a 2 decimales).
   - 'total_comisiones': Suma de las comisiones generadas (redondeado a 2 decimales).
   - 'vendedores_unicos': Lista o conjunto de nombres de vendedores únicos que aportaron ventas. 
     (Si no existe el vendedor, usa "DESCONOCIDO").

5. Ordenación Final:
   - Ordena el reporte final de MAYOR a MENOR por 'total_ventas_brutas'.

"""
import csv

# 1. Indexación de Vendedores (Hash Map)
mapa_vendedores = {}
with open("vendedores.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        mapa_vendedores[fila["vendedor_id"]] = {
            "nombre": fila["nombre"],
            "departamento": fila["departamento"],
            "comision_pct": float(fila["comision_pct"])
        }

# 2. Acumulación por Departamento (GROUP BY)
resumen_deptos = {}

with open("ventas.csv", "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        if fila["estado"] != "COMPLETADA":
            continue

        try:
            monto_bruto = float(fila["monto_bruto"])
            if monto_bruto <= 0:
                continue
        except ValueError:
            continue

        vendedor_id = fila["vendedor_id"]
        vendedor = mapa_vendedores.get(vendedor_id)

        # Determinar departamento, comisión y nombre según si existe o no
        if vendedor is None:
            departamento = "SIN_ASIGNAR"
            comision_generada = 0.00
            nombre_vendedor = "DESCONOCIDO"
        else:
            departamento = vendedor["departamento"]
            comision_generada = monto_bruto * vendedor["comision_pct"]
            nombre_vendedor = vendedor["nombre"]

        # Inicializar el departamento en el acumulador si no existe
        if departamento not in resumen_deptos:
            resumen_deptos[departamento] = {
                "total_ventas_brutas": 0.0,
                "total_comisiones": 0.0,
                "vendedores_unicos": set()
            }

        # Acumular
        resumen_deptos[departamento]["total_ventas_brutas"] += monto_bruto
        resumen_deptos[departamento]["total_comisiones"] += comision_generada
        resumen_deptos[departamento]["vendedores_unicos"].add(nombre_vendedor)

# 3. Formateo y Transformación Final
reporte = []
for depto, datos in resumen_deptos.items():
    reporte.append({
        "departamento": depto,
        "total_ventas_brutas": round(datos["total_ventas_brutas"], 2),
        "total_comisiones": round(datos["total_comisiones"], 2),
        "vendedores_unicos": list(datos["vendedores_unicos"])
    })

# 4. Ordenación de MAYOR a MENOR por ventas brutas
reporte_ordenado = sorted(reporte, key=lambda x: x["total_ventas_brutas"], reverse=True)

for r in reporte_ordenado:
    print(r)