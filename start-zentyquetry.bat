@echo off
title ZentyQuetry Desktop Edition (Air-Gapped)
color 0B
cls

cd /d "%~dp0"

echo ===================================================================
echo   ZentyQuetry(TM) Sovereign Desktop Edition (Offline / Air-Gapped)
echo   NIST Post-Quantum Cryptography (PQC) & CBOM Management Engine
echo ===================================================================
echo.

if exist "ZentyQuetry.exe" (
    echo [*] Memulai Standalone Executable ZentyQuetry.exe...
    echo [*] URL Akses: http://127.0.0.1:9527/
    echo [*] Tekan Ctrl+C di jendela ini jika ingin menghentikan server.
    echo.
    ZentyQuetry.exe
    goto end
)

:: Fallback untuk mode source Python
echo [*] ZentyQuetry.exe tidak ditemukan, menjalankan via Python runtime...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi di PATH!
    echo         Silakan unduh ZentyQuetry.exe atau pasang Python 3.9+.
    pause
    exit /b 1
)

python desktop_runner.py

:end
pause