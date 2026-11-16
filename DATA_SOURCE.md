# Data source

Data provided by [Open-Meteo](https://open-meteo.com/) using the ERA5 reanalysis model from ECMWF/Copernicus Climate Change Service.

- Documentation: https://open-meteo.com/en/docs/historical-weather-api
- Endpoint: https://archive-api.open-meteo.com/v1/archive
- Underlying source: [ERA5, Copernicus Climate Data Store](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels)
- Retrieval date: 16 November 2026, verified from the response metadata.
- Requested period: 1 January–31 December 2025.
- Model: era5, explicitly requested.
- Requested timezone: Europe/London.
- Fields: temperature_2m_mean, precipitation_sum, wind_speed_10m_max.
- Units: °C, mm and km/h respectively.

| Point label | Requested latitude | Requested longitude |
|---|---:|---:|
| London | 51.5074 | -0.1278 |
| Manchester | 53.4808 | -2.2426 |
| Edinburgh | 55.9533 | -3.1883 |

These coordinates identify representative points. Reanalysis provides modelled historical conditions, not city-wide measurements or a single weather station's observations. Returned grid coordinates can differ from requested point coordinates.

## Attribution and terms

Open-Meteo provides API data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The free API service has separate non-commercial usage terms and rate limits. See [service terms](https://open-meteo.com/en/terms), checked on 16 November 2026, before reuse or deployment. Data licensing and permission to use a particular API service tier are distinct.

The report transforms daily data into monthly means, precipitation sums and threshold counts. It does not imply endorsement by Open-Meteo, ECMWF or Copernicus.

## Source evidence

Nine raw-response files and nine metadata companions were supplied: three captures per city. Their SHA-256 hashes matched the bytes, and the daily weather values were identical between captures for each city.

[outputs/source_manifest.json](outputs/source_manifest.json) preserves filenames, request URLs, retrieval times and hashes from the submitted metadata. Raw responses remain in the local working project's data/raw folder and are excluded from this publication copy. Hash changes between captures do not necessarily indicate weather revisions; response metadata can also change.
