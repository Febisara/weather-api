@echo off
cd /d "%~dp0"
set "PGHOST=localhost"
set "PGPORT=5432"
set "PGDATABASE=weather_portfolio"
set "PGUSER=portfolio_user"
set "PGPASSFILE=%APPDATA%\postgresql\pgpass.conf"
if not exist logs mkdir logs
".venv\Scripts\python.exe" pipeline.py --recent >> logs\scheduled.log 2>&1
exit /b %errorlevel%
