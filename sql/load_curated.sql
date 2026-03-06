INSERT INTO curated_schema.feature_engineered_transactions (
transaction_id,
time,
amount,
rolling_avg_amount_10,
amount_zscore,
time_since_last_txn,
high_value_flag,
amount_velocity,
v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18,
v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, class 
)

SELECT
transaction_id,
time,
amount,
--rolling  average amount over last 10 transactions
AVG(amount) OVER (
	ORDER BY time
	ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
) AS rolling_avg_amount_10,
--zscore  of amount
(amount - AVG(amount) OVER ())
/
NULLIF(STDDEV(AMOUNT) OVER (),0)
AS amount_zscore,
--time since previous transaction
time - LAG(time) OVER (
	ORDER BY time
) AS time_since_last_txn,
--high value flag 
CASE
	WHEN amount >
PERCENTILE_CONT(0.95)
WITHIN GROUP (ORDER BY amount) OVER ()
	THEN TRUE
	ELSE FALSE
END AS high_value_flag,
--amount velocity 
amount - LAG(amount) OVER (
	ORDER BY time
) AS amount_velocity,
v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18,
v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, class 
FROM staging_schema.cleaned_transactions
ORDER BY time;

