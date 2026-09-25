#!/usr/bin/env bash
echo "==================================================================="
echo "  ZentyQuetry(TM) Sovereign Desktop Edition (Offline / Air-Gapped)"
echo "  NIST Post-Quantum Cryptography (PQC) & CBOM Management Engine"
echo "==================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 tidak ditemukan. Silakan pasang python3."
    exit 1
fi

python3 desktop_runner.py