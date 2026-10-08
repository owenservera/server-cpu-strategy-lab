@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js 20 or newer is required. Install Node.js and run this file again.
  pause
  exit /b 1
)
echo Starting CORE/SIGNAL at http://127.0.0.1:4173/
start "CORE SIGNAL Web Browser" "http://127.0.0.1:4173/"
node server.mjs
pause