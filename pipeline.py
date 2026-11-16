# Fetch historical UK weather, validate, archive and upsert atomically.
import argparse
import hashlib
import json
import logging
import math
import os
import uuid
from datetime import date, datetime, timedelta, timezone
from getpass import getpass
from pathlib import Path
import psycopg
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
CITIES = {'London': (51.5074, -0.1278),
          'Manchester': (53.4808, -2.2426),
          'Edinburgh': (55.9533, -3.1883)}
FIELDS = ['temperature_2m_mean', 'precipitation_sum',
          'wind_speed_10m_max']


def connect():
    password = os.getenv('PGPASSWORD')
    if not password and not os.getenv('PGPASSFILE'):
        password = getpass('PostgreSQL password: ')
    return psycopg.connect(
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432'),
        dbname=os.getenv('PGDATABASE', 'weather_portfolio'),
        user=os.getenv('PGUSER', 'portfolio_user'),
        password=password
    )


def validate(payload, start, end):
    daily = payload['daily']
    expected = [(start + timedelta(days=i)).isoformat()
                for i in range((end-start).days + 1)]
    if daily['time'] != expected:
        raise ValueError('Missing, repeated or out-of-order dates')
    units = payload['daily_units']
    if [units[f] for f in FIELDS] != ['°C', 'mm', 'km/h']:
        raise ValueError('Unexpected weather units')
    if any(len(daily[f]) != len(expected) for f in FIELDS):
        raise ValueError('Daily arrays have different lengths')
    rows = []
    for i, day in enumerate(expected):
        values = [daily[f][i] for f in FIELDS]
        if any(type(v) not in (int, float) or not math.isfinite(v)
               for v in values):
            raise ValueError(f'Missing or nonfinite value: {day}')
        temp, rain, wind = values
        if not -90 <= temp <= 60 or rain < 0 or wind < 0:
            raise ValueError(f'Implausible weather value: {day}')
        rows.append((date.fromisoformat(day), temp, rain, wind))
    return rows


def collect(start, end):
    retry = Retry(total=3, backoff_factor=.5,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=['GET'], respect_retry_after_header=True)
    cache = ROOT / 'data' / 'raw'
    cache.mkdir(parents=True, exist_ok=True)
    all_rows = []
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=retry))
        for city, (lat, lon) in CITIES.items():
            params = {
                'latitude': lat, 'longitude': lon,
                'start_date': start.isoformat(),
                'end_date': end.isoformat(),
                'daily': ','.join(FIELDS), 'timezone': 'Europe/London',
                'models': 'era5', 'temperature_unit': 'celsius',
                'wind_speed_unit': 'kmh', 'precipitation_unit': 'mm'
            }
            response = session.get(
                'https://archive-api.open-meteo.com/v1/archive',
                params=params, timeout=(10, 60)
            )
            response.raise_for_status()
            body = response.content
            sha = hashlib.sha256(body).hexdigest()
            payload = response.json()
            rows = validate(payload, start, end)
            # Save bytes and request metadata for reproducible investigation.
            target = cache / f'{city}_{start}_{end}_{sha[:12]}.json'
            target.write_bytes(body)
            target.with_suffix('.metadata.json').write_text(json.dumps({
                'url': response.url, 'sha256': sha,
                'retrieved_at': datetime.now(timezone.utc).isoformat()
            }, indent=2))
            all_rows.extend((city, *row, sha) for row in rows)
            logging.info('%s validated %s daily rows', city, len(rows))
    return all_rows


def load(conn, rows):
    sql = '''INSERT INTO weather_daily
        (city,day,mean_temp_c,rain_mm,max_wind_kmh,source_sha256)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT(city,day) DO UPDATE SET
          mean_temp_c=EXCLUDED.mean_temp_c,
          rain_mm=EXCLUDED.rain_mm,
          max_wind_kmh=EXCLUDED.max_wind_kmh,
          source_sha256=EXCLUDED.source_sha256,
          loaded_at=now()'''
    with conn.cursor() as cur:
        cur.executemany(sql, rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', default='2025-01-01')
    parser.add_argument('--end', default='2025-12-31')
    parser.add_argument('--recent', action='store_true')
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    if args.recent:
        end = date.today() - timedelta(days=7)
        start = end - timedelta(days=13)
    else:
        start = date.fromisoformat(args.start)
        end = date.fromisoformat(args.end)
    if start > end or (end-start).days > 366:
        raise ValueError('Use an ordered range of at most 367 days')
    logs = ROOT / 'logs'
    logs.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.FileHandler(logs / 'pipeline.log'),
                  logging.StreamHandler()])
    started = datetime.now(timezone.utc)
    run_id = uuid.uuid4()
    conn = None
    try:
        if not args.validate_only:
            conn = connect()
        rows = collect(start, end)
        if conn is not None:
            # The whole requested range across all cities commits together.
            with conn.transaction():
                load(conn, rows)
                conn.execute('''INSERT INTO pipeline_runs VALUES
                    (%s,%s,%s,'success',%s,%s,%s,NULL)''',
                    (run_id, started, datetime.now(timezone.utc),
                     start, end, len(rows)))
        print(f'Validated {len(rows)} rows; database load: {conn is not None}')
    except Exception as exc:
        logging.exception('Pipeline failed')
        if conn is not None:
            conn.rollback()
            try:
                with conn.transaction():
                    conn.execute('''INSERT INTO pipeline_runs VALUES
                        (%s,%s,%s,'failed',%s,%s,0,%s)''',
                        (run_id, started, datetime.now(timezone.utc),
                         start, end, str(exc)[:500]))
            except Exception:
                logging.exception('Could not write failed run to database')
        raise
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()
