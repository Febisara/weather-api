CREATE TABLE IF NOT EXISTS weather_daily (
 city TEXT NOT NULL,
 day DATE NOT NULL,
 mean_temp_c DOUBLE PRECISION NOT NULL,
 rain_mm DOUBLE PRECISION NOT NULL CHECK(rain_mm >= 0),
 max_wind_kmh DOUBLE PRECISION NOT NULL CHECK(max_wind_kmh >= 0),
 source_sha256 TEXT NOT NULL,
 loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 PRIMARY KEY(city,day)
);
CREATE TABLE IF NOT EXISTS pipeline_runs (
 run_id UUID PRIMARY KEY,
 started_at TIMESTAMPTZ NOT NULL,
 finished_at TIMESTAMPTZ NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('success','failed')),
 requested_start DATE NOT NULL,
 requested_end DATE NOT NULL,
 processed_rows INTEGER NOT NULL,
 error TEXT
);
