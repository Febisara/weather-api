# Decision log

## 16 November 2026 — Source and coverage

I used the fixed year 2025, three representative city points and the ERA5 model. A fixed complete year allows consistent coverage checks. The data is historical reanalysis, not direct city-wide station measurements or a forecast.

I requested explicit units and timezone and retained response snapshots and metadata locally. Each response hash identifies downloaded bytes rather than the observation key.

## Observation identity and replay

I used (city, day) as the composite primary key. A random row ID or response filename would not prevent multiple observations for the same point-date.

ON CONFLICT updates existing values, source hashes and load timestamps. The submitted replay export has 1,095 daily records and two successful runs. Run history changes even when observation counts remain unchanged.

## Validate before loading

I used validation for exact date coverage, units, array lengths, finite numeric values and broad physical bounds. The four supplied tests passed. The pipeline collects and validates all cities before starting the normal data-write transaction.

Source snapshots are written after response validation. Invalid responses are not guaranteed to be archived; exceptions are logged.

## Connection troubleshooting

The first failed database attempt used 5433 as the host. I corrected the host to localhost and supplied the database port separately. The local workflow subsequently loaded successfully.

A deliberate attempt on port 59999 failed with a connection timeout, recorded in pipeline.log. This is evidence of connection-failure handling, not proof of rollback after a partial database load.

## Constraint and transaction exercise

I attempted to set precipitation to −1 for London on 1 January 2025. I encountered an aborted transaction and used ROLLBACK to recover. I confirmed in the guided workflow that the original nonnegative value remained unchanged.

The original before-and-after database screenshots were not included in the review bundle, so this outcome is recorded as my confirmation rather than independent database verification.

## Reporting choices

I sum precipitation and average daily mean temperatures. The illustrative thresholds are precipitation ≥10 mm and maximum wind speed ≥40 km/h.

London January's SQL result matched the Python report: 31 days, mean temperature approximately 4.2387 °C, 78.5 mm precipitation, one wet-threshold day and two windy-threshold days. Tiny floating-point display differences are not corrected by changing source values.

## Scope and assistance

The published project is a manually run historical weather pipeline covering 2025. Scheduling and the attempted configurable-year reporting extension are excluded from the final deliverable.

I used the supplied course implementation and AI guidance for setup, troubleshooting and documentation. The final review checked raw snapshots, hashes and exported results independently, without connecting to my PostgreSQL server.
