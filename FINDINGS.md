# Historical weather exposure in three UK locations

## Scope

This project compares modelled historical weather at representative points for London, Manchester and Edinburgh during 2025. Each point has 365 daily records, giving 1,095 observations and 36 city-month summaries. The responses were retrieved from Open-Meteo on 16 November 2026 with the ERA5 model, explicit units and the Europe/London timezone.

The analysis supports further investigation of seasonal exposure. It does not measure delivery delays, business losses or official warning events. Precipitation includes the water equivalent of snow; the internal column name rain_mm does not imply that every event was liquid rain.

## Annual precipitation

The selected Manchester point had the highest annual total, at 921.3 mm. Edinburgh recorded 727.1 mm and London 573.7 mm. Manchester therefore recorded 347.6 mm more precipitation than London in this extraction.

These totals describe the specified points and year. They do not establish a permanent ranking of city climates, nor do they capture differences within each city. An operations team could use the comparison to prioritise more detailed route- or site-level investigation, but should not infer that Manchester necessarily experienced more disruption.

Source: [Annual weather](outputs/annual_weather.csv).

## Monthly pattern

Manchester's highest monthly total was December, at 134.4 mm, closely followed by September at 133.6 mm. Its April total was 19.7 mm. This variation shows why an annual total alone does not describe when precipitation was concentrated.

Edinburgh and London both reached their highest monthly precipitation in November, at 132.8 mm and 96.5 mm respectively. The timing differs from Manchester's maximum, so one shared annual planning assumption would hide useful differences between the selected locations.

One year cannot establish a recurring seasonal pattern. A useful next investigation would compare multiple complete years using consistent model and coordinate settings, then examine whether similar monthly patterns recur.

Source: [Monthly weather](outputs/monthly_weather.csv).

## Screening thresholds

Using the illustrative threshold of at least 10 mm precipitation per day, Manchester had 22 qualifying days, London 15 and Edinburgh 12. London therefore had more threshold days than Edinburgh despite a lower annual total. Total volume and the frequency of larger daily events answer different questions.

At the separate maximum-wind-speed threshold of at least 40 km/h, Edinburgh had nine qualifying days, Manchester eight and London four. These are daily maximum wind speeds at 10 m, not gust measurements. Neither threshold is an official alert criterion, and changing either threshold would change the counts.

## Validation and next action

Archived response hashes matched their metadata. Recomputed monthly and annual summaries matched the exported reports. The replay export retained 1,095 observations across two successful runs, and the four supplied validation tests passed.

To examine an operational relationship, obtain dated delivery or service outcomes, routes, site locations, traffic conditions, volumes and service commitments. Align those records to relevant weather exposure before testing associations and alternative explanations. This project alone cannot attribute disruption to weather.

Scheduling and independent extensions were not completed. The deliverable is a manually run, validated historical reporting pipeline with documented replay and failure handling.
