SELECT city, count(*) AS days,
 min(day) AS first_day, max(day) AS last_day
FROM weather_daily 
WHERE day >= DATE '2025-01-01' 
	AND day < '2026-01-01'
GROUP BY city 
ORDER BY city;

-- These thresholds are illustrative screening rules, not official warnings.
SELECT city, date_trunc('month',day)::date AS month,
 count(*) AS observed_days,
 round(avg(mean_temp_c)::numeric,1) AS mean_temp_c,
 round(sum(rain_mm)::numeric,1) AS rain_mm,
 count(*) FILTER (WHERE rain_mm >= 10) AS wet_days,
 count(*) FILTER (WHERE max_wind_kmh >= 40) AS windy_days
FROM weather_daily
WHERE day >= DATE '2025-01-01' AND day < DATE '2026-01-01'
GROUP BY city, date_trunc('month',day) ORDER BY city,month;

SELECT started_at,status,processed_rows,error
FROM pipeline_runs ORDER BY started_at DESC LIMIT 10;
