# Data quality and verification

Review date: 16 November 2026.

## Evidence checks

| Check | Result |
|---|---|
| Response captures | Nine: three per city |
| SHA-256 metadata versus raw bytes | All nine match |
| Exact ordered date coverage | 365 dates per response, 1 January–31 December 2025 |
| Units and numeric validation | All submitted responses pass |
| Daily values across repeat captures | Identical within each city |
| Unique city-date records in reconstructed data | 1,095 |
| Monthly CSV | 36 rows; every value matches independent aggregation |
| Annual CSV | All precipitation sums and threshold counts match |
| London January SQL spot check | Matches the monthly report |
| City coverage export | Three cities, 365 days each |
| Replay export | 1,095 daily rows and two successful runs |
| Run-history export | Two success records, each processing 1,095 rows |
| Validation tests | Four passed |
| Chart | Visually checked against monthly results; labels and units readable |

The report's London January precipitation is 78.5 mm. The SQL export displays 78.50000000000001; this is a floating-point representation difference, not a substantive mismatch.

## Test-output interpretation

outputs/validation_tests.txt ends with four tests run and OK. Its first lines contain PowerShell NativeCommandError formatting around unittest's standard-error output. All four individual tests report ok; the wrapper is not an assertion failure.

During review, the submitted pure validate function was extracted unchanged and run against the four submitted tests and all archived responses. Database-dependent imports were excluded because Psycopg was unavailable in the review runtime. This tests validation logic; it is not a full pipeline integration run.

## Failure evidence

The submitted local log records a failed attempt to resolve host 5433, followed by successful city validations. It also records the deliberate connection timeout on port 59999.

These failures occur before a usable database connection. The absence of failed entries in pipeline_runs is therefore consistent with the code. File logs provide the fallback evidence.

The author confirmed unchanged observation counts and the negative-precipitation rollback outcome. The SQL spot-check and replay CSVs were supplied; a separate before-and-after constraint-test export was not.

## Verification limits

The review recomputed outputs from the saved API responses; it did not call the live API or connect to PostgreSQL. It did not test a fresh installation of requirements-lock.txt, the Windows scheduler or a forced mid-load pipeline rollback.

The current report checks total row count and duplicate city-date keys. It does not independently require exactly 365 dates for each configured city. The submitted snapshots and coverage exports meet that stronger condition, but the report guard could be strengthened in future.

The database stores current accepted values, not complete revision history. Scheduling, alerting and independent extensions were not completed. The provided production-style features demonstrate a learning workflow rather than production readiness.
