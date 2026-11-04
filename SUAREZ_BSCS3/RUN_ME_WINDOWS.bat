@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 (
  py -m pip install -r requirements.txt
  if errorlevel 1 pause & exit /b 1
  py main.py
) else (
  python main.py
)
pause
