@echo off
title Hentikan ZentyQuetry Desktop
color 0C
cls

echo ===================================================================
echo   Menghentikan ZentyQuetry Desktop Server (Port 9527)
echo ===================================================================
echo.

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":9527" ^| findstr "LISTENING"') do (
    echo [*] Menghentikan proses PID: %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] Server ZentyQuetry Desktop dihentikan.
timeout /t 2 /nobreak >nul
exit /b 0