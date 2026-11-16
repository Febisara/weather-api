from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pipeline import connect

ROOT = Path(__file__).resolve().parent
out = ROOT / 'outputs'
out.mkdir(exist_ok=True)
with connect() as conn:
    with conn.cursor() as cur:
        cur.execute('''SELECT city,day,mean_temp_c,rain_mm,max_wind_kmh
            FROM weather_daily WHERE day >= '2025-01-01'
            AND day < '2026-01-01' ORDER BY city,day''')
        data = cur.fetchall()
        columns = [col.name for col in cur.description]
df = pd.DataFrame(data, columns=columns)
if len(df) != 1095 or df.duplicated(['city','day']).any():
    raise ValueError('Load the complete 2025 dataset before reporting')
df['month'] = pd.to_datetime(df['day']).dt.to_period('M').astype(str)
df['wet_day'] = df['rain_mm'] >= 10
df['windy_day'] = df['max_wind_kmh'] >= 40
monthly = df.groupby(['city','month']).agg(
    days=('day','size'), mean_temp_c=('mean_temp_c','mean'),
    rain_mm=('rain_mm','sum'), wet_days=('wet_day','sum'),
    windy_days=('windy_day','sum')
).reset_index()
monthly.to_csv(out/'monthly_weather.csv',index=False)
pivot = monthly.pivot(index='month',columns='city',values='rain_mm')
ax = pivot.plot(figsize=(10,5),marker='o',
                title='Monthly precipitation in 2025')
ax.set_ylabel('Precipitation (mm)')
ax.set_xlabel('Month')
ax.figure.tight_layout()
ax.figure.savefig(out/'monthly_rain.png',dpi=180)
plt.close(ax.figure)
print(monthly.to_string(index=False))
