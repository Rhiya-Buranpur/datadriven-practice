WITH post_counts AS (
  SELECT
    endpoint,
    COUNT(*) AS call_count
  FROM api_calls
  WHERE UPPER(method) = 'POST'
  GROUP BY endpoint
),
ranked AS (
  SELECT
    endpoint,
    call_count,
    RANK() OVER (ORDER BY call_count) AS rnk
  FROM post_counts
)

SELECT
  endpoint,
  call_count,
  rnk
FROM ranked
WHERE rnk <= 3
ORDER BY rnk, endpoint
