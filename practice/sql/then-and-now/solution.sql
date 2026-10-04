WITH counted AS (
  SELECT
    model_id,
    mdl_name,
    version,
    accuracy,
    train_at
  FROM ml_models
  WHERE accuracy IS NOT NULL
  AND train_at IS NOT NULL
  AND TRIM(train_at) <> ''
),
ranked AS (
  SELECT
    model_id,
    mdl_name,
    accuracy,
    train_at,
    ROW_NUMBER() OVER (
      PARTITION BY mdl_name
      ORDER BY train_at DESC, model_id DESC
    ) AS rn
  FROM counted
),
aggregated AS (
  SELECT
    mdl_name,
    AVG(accuracy) AS avg_lifetime_accuracy,
    MAX(
      CASE
        WHEN rn = 1 THEN accuracy
      END
      ) AS latest_accuracy,
    AVG(
      CASE
        WHEN rn > 1 THEN accuracy
      END
      ) AS earlier_avg,
    COUNT(*) AS n_versions
  FROM ranked
  GROUP BY mdl_name
)

SELECT
  mdl_name AS model_name,
  ROUND(
    avg_lifetime_accuracy,
    2
    ) AS avg_lifetime_accuracy,
  ROUND(latest_accuracy, 2) AS latest_accuracy,
  ROUND(
    CASE
      WHEN n_versions = 1 THEN 0
      ELSE latest_accuracy - earlier_avg
    END,
    2
    ) AS difference
FROM aggregated
ORDER BY model_name
