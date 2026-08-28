/*
ENUNCIADO:
A veces, las transacciones de pago se repiten por accidente debido a errores del usuario, 
fallos de API o reintentos que provocan un cobro duplicado en la tarjeta de crédito.

Utilizando la tabla 'transactions', identifica los pagos realizados en el mismo comercio (merchant_id), 
con la misma tarjeta de crédito (credit_card_id) y por el mismo monto (amount) dentro de un intervalo 
de 10 minutos entre sí. Cuenta el número total de dichos pagos repetidos.

SUPUESTOS:
La primera transacción no debe contarse como pago repetido. Esto significa que si hay dos 
transacciones en el mismo comercio, con la misma tarjeta y el mismo monto dentro de 10 minutos, 
solo habrá 1 pago repetido.

TABLA: transactions
- transaction_id (integer)
- merchant_id (integer)
- credit_card_id (integer)
- amount (integer)
- transaction_timestamp (datetime)
*/

WITH ranked_transactions AS (
  SELECT 
    transaction_id,
    merchant_id,
    credit_card_id,
    amount,
    transaction_timestamp,
    LAG(transaction_timestamp) OVER (
      PARTITION BY merchant_id, credit_card_id, amount 
      ORDER BY transaction_timestamp
    ) AS prev_transaction_timestamp
  FROM transactions
)
SELECT 
  COUNT(*) AS payment_count
FROM ranked_transactions
WHERE prev_transaction_timestamp IS NOT NULL
  AND EXTRACT(EPOCH FROM (transaction_timestamp - prev_transaction_timestamp)) / 60 <= 10;