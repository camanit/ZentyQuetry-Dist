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

:: 1. Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak terdeteksi di sistem PATH!
    echo         Silakan install Python 3.9+ dari https://www.python.org/
    echo.
    pause
    exit /b 1
)

:: 2. Cek cryptography library
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo [*] Menginstal dependensi cryptography untuk verifikasi Ed25519...
    pip install cryptography >nul 2>&1
    if errorlevel 1 (
        echo [WARN] Gagal install cryptography otomatis. Menggunakan HMAC-SHA256 fallback.
    ) else (
        echo [OK]   Pustaka cryptography siap.
    )
) else (
    echo [OK]   Pustaka cryptography siap (Sovereign Ed25519 aktif).
)

echo.
echo [*] Memulai server ZentyQuetry Desktop di http://127.0.0.1:9527...
echo [*] Tekan Ctrl+C di jendela ini jika ingin menghentikan server.
echo.

python desktop_runner.py

pause