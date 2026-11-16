# Data dictionary

## Daily observations: weather_daily

One row represents one city point and calendar date. The primary key is (city, day).

| Field | Type | Meaning |
|---|---|---|
| city | TEXT | Label for one configured representative coordinate |
| day | DATE | Daily observation date using the requested timezone |
| mean_temp_c | DOUBLE PRECISION | Daily mean temperature at 2 m, °C |
| rain_mm | DOUBLE PRECISION | Total daily precipitation, mm; includes water equivalent of snow |
| max_wind_kmh | DOUBLE PRECISION | Daily maximum wind speed at 10 m, km/h; not gust speed |
| source_sha256 | TEXT | SHA-256 of the accepted response bytes |
| loaded_at | TIMESTAMPTZ | Database load/update timestamp |

Floating-point values represent approximate weather quantities. Rainfall and wind columns have nonnegative database checks. The application additionally validates dates, units, array lengths, finite numbers and broad temperature bounds of −90 to 60 °C.

## Run history: pipeline_runs

| Field | Meaning |
|---|---|
| run_id | UUID identifying a pipeline attempt |
| started_at / finished_at | Timezone-aware timestamps |
| status | success or failed |
| requested_start / requested_end | Requested date range |
| processed_rows | Input records submitted on success; not a count of new inserts |
| error | Error text on recorded failure; NULL for success |

A failed run can be recorded in the database only when a usable connection is available. Connection failures are recorded in the file log.

## Report fields

| Field | Meaning |
|---|---|
| month | Calendar month in YYYY-MM form |
| days / observed_days | Number of daily records contributing to the group |
| mean_temp_c | Mean of daily mean temperatures within the month |
| rain_mm / precipitation_mm | Sum of daily precipitation |
| wet_days | Number of days with precipitation ≥10 mm |
| windy_days | Number of days with maximum wind speed ≥40 km/h |
| daily_rows | Observation count in the replay export |
| successful_runs | Count of successful audit records at export |

The wet and windy thresholds are illustrative screening rules, not official warning criteria. Counts are not operational disruption days. Annual exports cover 2025 only; the default report contains 36 city-month rows.
