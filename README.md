# 🛡️ ZentyQuetry™ Sovereign Desktop Edition

> **Offline & Air-Gapped NIST Post-Quantum Cryptography (PQC) & CBOM Management Engine**  
> Bagian dari **CTARTech Enterprise Cybersecurity Ecosystem**  
> Web Portal: [zentyquetry.ctar.tech](https://zentyquetry.ctar.tech) · Repo Induk: [camanit/ZentyQuetry](https://github.com/camanit/ZentyQuetry)

---

## 📖 Ringkasan

**ZentyQuetry™ Sovereign Desktop Edition** dirancang khusus untuk lingkungan berkeamanan tinggi, terisolasi (*air-gapped*), data center perbankan, instansi pertahanan, dan infrastruktur kritis yang mewajibkan audit **Cryptographic Bill of Materials (CBOM)** serta simulasi migrasi **Post-Quantum Cryptography (NIST FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA)** tanpa mengekspos data ke jaringan internet.

Setiap instalasi desktop terikat secara kriptografis (*hardware node-locking*) dengan mesin fisik Anda: **1 Perangkat Fisik = 1 Lisensi Kriptografis**.

---

## ⚡ Quick Start (Cara Menjalankan)

### 🪟 Windows (Metode 1-Click)
1. Cukup double-click file **`start-zentyquetry.bat`**.
2. Skrip akan memverifikasi lingkungan Python dan otomatis meluncurkan server lokal di:
   ```
   http://127.0.0.1:9527/
   ```
3. Browser default Anda akan otomatis terbuka ke dasbor ZentyQuetry.
4. Untuk menghentikan aplikasi, jalankan **`stop-zentyquetry.bat`** atau tekan `Ctrl + C` pada jendela terminal.

### 🐧 Linux / 🍎 macOS
Buka terminal di direktori ini dan jalankan:
```bash
chmod +x start-zentyquetry.sh
./start-zentyquetry.sh
```
Atau langsung:
```bash
python3 desktop_runner.py
```

---

## 🆓 Mode Lisensi: Community (Gratis) vs Enterprise

### 1. Community Mode (Free / Bawaan Langsung)
Saat pertama kali diunduh dan dijalankan **tanpa file lisensi**:
- ✅ **100% GRATIS** tanpa batas waktu kedaluwarsa.
- ✅ **CBOM Scanner**: Pindai aset kriptografi lokal, dependensi, dan sertifikat TLS.
- ✅ **PQC Migration Simulator**: Simulasi penggantian algoritma klasik (RSA, ECC) ke PQC (ML-KEM, ML-DSA).
- ✅ **Eksekusi 100% Lokal (Air-gapped)**: Tanpa koneksi internet atau telemetri eksternal.
- *Saat layar aktivasi muncul, cukup klik tombol **"Lanjutkan sebagai Community (Free)"** untuk langsung masuk.*

### 2. Enterprise & Government Tier
Untuk membuka kapabilitas penuh enterprise:
- 🚀 **SentinelOps Real-time Daemon** & continuous background asset monitor.
- 🚀 **Multi-Tenant Federation & Custom Policy Engine**.
- 🚀 **Konektor DataBank AI Central (`gplay.ctar.tech`)**.
- 🚀 **Integrasi SOC Feed (`ZentyInfoSec`) & Health Scoring (`ZentyTeamScore`)**.
- 🚀 **Ekspor Audit CBOM Format CycloneDX 1.6 / SPDX 3.0 & Executive PDF**.

---

## 🔑 Cara Aktivasi Lisensi Enterprise

Setiap instalasi ZentyQuetry Desktop menghasilkan **Hardware Node ID unik**:
Format: `ZQ-NODE-XXXX-XXXX-XXXX-XXXX`

1. Jalankan aplikasi, perhatikan **Node ID** yang tertera pada jendela aktivasi atau terminal.
2. Salin Node ID tersebut dan kirimkan ke tim otorisasi lisensi CTARTech atau administrator internal perusahaan Anda.
3. Anda akan menerima file **`license.lic`** bertanda tangan kriptografis Ed25519.
4. Ada 2 cara aktivasi:
   - **Metode A (GUI):** Buka `http://127.0.0.1:9527`, paste isi teks JSON `license.lic` ke kolom aktivasi, lalu klik **"Aktifkan Lisensi"**.
   - **Metode B (File):** Salin file `license.lic` langsung ke folder aplikasi ini dan restart aplikasi.
5. Mesin akan langsung terverifikasi secara matematis menggunakan kunci publik `public_key.pem`.

---

## 🛡️ Spesifikasi Keamanan & Integritas Kriptografis

| Komponen | Spesifikasi |
|---|---|
| **Protokol Tanda Tangan** | Ed25519 Asymmetric Sovereign Cryptography |
| **Kunci Publik** | `public_key.pem` (Tersemat pada distribusi) |
| **Fallback Verifier** | HMAC-SHA256 Machine Seed Lock |
| **Hardware Binding** | Hostname + CPU Processor + Machine Architecture + MAC SHA-256 |
| **Standar PQC** | NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) |
| **Kepatuhan Privasi** | Zero External Leak, No Cloud Analytics, Air-Gap Ready |

---

## 📂 Struktur Berkas Distribusi

```
ZentyQuetry-Dist/
├── desktop_runner.py       # Engine HTTP server lokal & validator lisensi node-lock
├── public_key.pem          # Kunci publik resmi CTARTech untuk verifikasi Ed25519
├── start-zentyquetry.bat   # Launcher 1-click Windows
├── stop-zentyquetry.bat    # Pemati server Windows port 9527
├── start-zentyquetry.sh    # Launcher Linux / macOS
├── index.html              # Antarmuka web console ZentyQuetry
├── app.js                  # Logika aplikasi CBOM & PQC Engine
├── styles.css              # Styling antarmuka enterprise
└── README.md               # Dokumentasi ini
```

---

## 🤝 Dukungan & Hubungi Kami

- **Portal Resmi:** [https://zentyquetry.ctar.tech](https://zentyquetry.ctar.tech)
- **Repositori Distribusi:** [https://github.com/camanit/ZentyQuetry-Dist](https://github.com/camanit/ZentyQuetry-Dist)
- **CTARTech Central Security:** [https://ctar.tech](https://ctar.tech)
- **Ekosistem Terhubung:** `ZentyTeamsCore`, `ZentyInfoSec`, `ZentyElastis`, `GPlay AI DataBank`

© 2026 **CTARTech**. All rights reserved. Sovereign Cryptographic Protection Systems.