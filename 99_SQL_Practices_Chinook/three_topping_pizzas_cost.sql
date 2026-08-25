/*
ENUNCIADO:
Eres un consultor para una gran cadena de pizzerías que va a lanzar una promoción 
en la que todas las pizzas de 3 ingredientes se venderán a un precio fijo, y estás 
intentando entender los costes involucrados.

Dada una lista de ingredientes para pizza, considera todas las posibles combinaciones 
de pizzas de 3 ingredientes y calcula el coste total de esos 3 ingredientes. 
Ordena los resultados mostrando el coste total más alto primero; en caso de empate, 
ordena las combinaciones de ingredientes en orden alfabético ascendente.

Resuelve los empates enumerando los ingredientes en orden alfabético, comenzando 
por el primer ingrediente, seguido del segundo y del tercero.

P.D. Ten cuidado con el espaciado (o la falta de él) entre cada ingrediente. 
Consulta el ejemplo de salida.

Notas:
- No muestres pizzas donde se repita algún ingrediente. Por ejemplo: 'Pepperoni,Pepperoni,Onion Pizza'.
- Los ingredientes dentro de la combinación deben estar ordenados alfabéticamente. 
  Por ejemplo: 'Chicken,Onions,Sausage'. No se acepta 'Onion,Sausage,Chicken'.

Tabla pizza_toppings:
- topping_name (varchar(255))
- ingredient_cost (decimal(10,2))

Ejemplo de Entrada (pizza_toppings):
topping_name | ingredient_cost
------------------------------
Pepperoni    | 0.50
Sausage      | 0.70
Chicken      | 0.55
Extra Cheese | 0.40

Ejemplo de Salida:
pizza                           | total_cost
--------------------------------------------
Chicken,Pepperoni,Sausage       | 1.75
Chicken,Extra Cheese,Sausage    | 1.65
Extra Cheese,Pepperoni,Sausage  | 1.60
Chicken,Extra Cheese,Pepperoni  | 1.45
*/

SELECT p1.topping_name|| ','|| p2.topping_name|| ','||p3.topping_name AS pizza,
    p1.ingredient_cost+p2.ingredient_cost+p3.ingredient_cost as total_cost
FROM pizza_toppings AS p1
INNER JOIN pizza_toppings AS p2
  ON p1.topping_name < p2.topping_name 
INNER JOIN pizza_toppings AS p3
  ON p2.topping_name < p3.topping_name
order by total_cost DESC, pizza ASC
;