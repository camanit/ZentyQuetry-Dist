# ZentyQuetry
**Post-Quantum Cryptography (PQC) & Cryptographic Agility Migration Platform**

[![Vercel Deployment](https://img.shields.io/badge/Deploy-Vercel-black?style=flat&logo=vercel)](https://vercel.com)
[![Status](https://img.shields.io/badge/Status-V.1.0%20Enterprise-emerald?style=flat)]()
[![PQC Standards](https://img.shields.io/badge/NIST-FIPS%20203%20%7C%20204%20%7C%20205-purple?style=flat)]()

ZentyQuetry adalah platform terpadu untuk memantau, menganalisis, dan memigrasikan aset kriptografi organisasi menghadapi era komputasi kuantum (ancaman *Store-Now-Decrypt-Later / SNDL*). Terintegrasi dengan bank data sentral `gplay.ctar.tech`, mesin pemindai SentinelOps, dan ekosistem Zenty.

---

## 🚀 Fitur Utama
1. **Cryptographic Bill of Materials (CBOM)**:
   * Penemuan otomatis seluruh cipher suite, SSL/TLS endpoints, SSH host keys, dan sertifikat.
   * Mode ganda: **Agentless Remote Scanner** (tanpa instalasi apapun) dan **SentinelOps Edge Daemon** (pemindaian mendalam & rotasi otomatis).
2. **AI-Driven SNDL Risk Assessor**:
   * Evaluasi risiko matematis berbasis Teorema Mosca ($Y + X > Z$) untuk mengidentifikasi data rahasia yang terancam dekripsi di masa depan.
3. **Automated Zero-Downtime Remediation**:
   * Generator sertifikat hibrida (Klasik + PQC seperti ML-KEM-768 & ML-DSA-65).
4. **All-in-One Multi-Tenant Portal**:
   * Form Auth lengkap (Login, Register Tenant Baru, Lupa Sandi).
   * Portal Tenant (Ringkasan Postur, CBOM Explorer, Manajemen Lisensi, Profil).
   * Portal Superadmin (Manajemen Tenant, Paket & Harga, Billing & Invoice, Laporan Analitik Global).
5. **Dukungan Aplikasi Desktop (Air-Gapped Workstation)**:
   * Menjalankan antarmuka native lokal via `desktop_app.py` tanpa koneksi internet dengan verifikasi lisensi fisik Machine ID.

---

## 📂 Struktur Proyek
```text
├── index.html              # Antarmuka Web App & Portal Multi-View (Vercel Ready)
├── styles.css              # Sistem desain cyber-quantum dark mode
├── app.js                  # Logika interaktif, lokalisasi (EN/ID), Mosca simulator
├── desktop_app.py          # Wrapper aplikasi desktop native (Air-Gapped Mode)
├── vercel.json             # Konfigurasi routing & security headers Vercel
├── ROADMAP.md              # Rencana pengembangan V.0.1 - V.1.0
├── DATA_SPEC_GPLAY.md      # Spesifikasi API & skema database gplay.ctar.tech
├── license.lic             # Contoh berkas lisensi digital bertanda tangan
├── tools/
│   └── license_engine.py   # Generator Machine ID hardware & validator lisensi
└── gplay-integration/      # Paket integrasi Laravel untuk Herd/gplay
    ├── database/migrations/
    ├── app/Models/
    ├── app/Http/Controllers/
    ├── routes/
    └── deploy_to_herd.ps1  # Script deploy otomatis ke Herd gplay
```

---

## ⚡ Deployment ke Vercel
Proyek ini siap di-deploy langsung ke Vercel:
1. Hubungkan repositori GitHub: `https://github.com/camanit/ZentyQuetry`.
2. Vercel akan otomatis mendeteksi konfigurasi statis (`index.html`, `styles.css`, `app.js`).
3. Masukkan Environment Variables (`.env`) bila diperlukan.
4. Klik **Deploy**.

---

## 💻 Menjalankan Desktop App Lokal
```bash
# Menjalankan aplikasi desktop native:
python desktop_app.py

# Memeriksa Machine ID perangkat untuk aktivasi lisensi:
python tools/license_engine.py
```

---
&copy; 2026 ZentyQuetry. Bagian dari Ekosistem ctar.tech.
