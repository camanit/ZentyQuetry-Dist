# ZentyQuetry™ Enterprise PQC Platform
**Post-Quantum Cryptography (PQC), CBOM Deep Discovery & Cryptographic Agility Migration Platform**

[![Status](https://img.shields.io/badge/Release-V.1.0%20ENTERPRISE-10b981?style=flat&logo=shield)](https://github.com/camanit/ZentyQuetry)
[![PQC Standards](https://img.shields.io/badge/NIST-FIPS%20203%20%7C%20204%20%7C%20205-purple?style=flat)](https://csrc.nist.gov/publications/detail/fips/203/final)
[![FIPS Kepatuhan](https://img.shields.io/badge/Compliance-FIPS%20140--3%20Hybrid-06b6d4?style=flat)]()
[![Hardware Lock](https://img.shields.io/badge/Air--Gap-Hardware%20Node%20Binding-f59e0b?style=flat)]()

ZentyQuetry™ adalah platform enterprise terpadu untuk memantau, memetakan, menganalisis, dan memigrasikan inventaris kriptografi organisasi guna menghadapi ancaman komputasi kuantum (*Store-Now-Decrypt-Later / SNDL* & Q-Day). Platform ini mendukung penerapan hybrid standar NIST (FIPS 203 ML-KEM-768, FIPS 204 ML-DSA-65, FIPS 205 SLH-DSA) dengan nol downtime melalui arsitektur multi-cloud maupun luring (*100% Sovereign Air-Gap*).

---

## 🏛️ 15 Modul Operasional Enterprise

| No | Modul Platform | Kategori | Deskripsi Fungsional |
|:---|:---|:---:|:---|
| 1 | **Overview & Posture Health** | Core | Dasbor eksekutif postur kriptografi real-time, skor kesiapan PQC, dan rasio aset rentan. |
| 2 | **CBOM & Discovery Engine** | Core | Inventarisasi CBOM otomatis, pemindaian Shadow Crypto, keystore usang, dan deduplikasi deterministik SHA-256. |
| 3 | **PQC Code Playbooks** | Core | Generator refactoring kode hibrida otomatis untuk Java, Go, Python, Node.js, dan Rust. |
| 4 | **Crypto Agility Benchmark** | ⭐ PRO | Pengujian stress-test latensi dan enkapsulasi algoritma NIST FIPS 203 vs RSA/ECC. |
| 5 | **Quantum CA & PKI Bridge** | 👑 ENT | Penerbitan sertifikat digital X.509 hybrid kuantum (ML-KEM/ML-DSA) terintegrasi ACME. |
| 6 | **ZentyTunnel (PQC VPN)** | 👑 ENT | Terowongan Zero-Trust Network Access (ZTNA) berbasis WireGuard dan IPsec quantum-safe. |
| 7 | **CI/CD Shift-Left Gatekeeper** | ⭐ PRO | Pipeline blocker otomatis untuk mendeteksi hardcoded legacy cipher suites pada merge request git. |
| 8 | **Zero-Code PQC Reverse Proxy** | ⭐ PRO | Sidecar ingress proxy (Envoy & Nginx) terminasi TLS kuantum tanpa modifikasi backend. |
| 9 | **Recurring Cron & Cert Drift** | ⭐ PRO | Pemantauan kontinyu masa kedaluwarsa sertifikat (&lt;30 hari) dan alert peringatan downgrade cipher. |
| 10 | **AI Mosca Threat Modeling** | Core | Evaluasi risiko SNDL matematis Teorema Mosca ($Y + X > Z$) dan proyeksi timeline Q-Day. |
| 11 | **Global Regulatory Compliance** | ⭐ PRO | Pemetaan kepatuhan audit regulasi global: FIPS 140-3, BSI TR-02102, CNSA 2.0, UU PDP & OJK. |
| 12 | **Merkle Audit & Ecosystem** | 👑 ENT | Jejak audit kriptografi tamper-proof berbasis rantai Merkle terhubung ke ekosistem Zenty. |
| 13 | **Executive Reports & Analytics** | ⭐ PRO | Generator laporan audit formal untuk CISO, regulator, dan auditor eksternal (PDF & JSON). |
| 14 | **SentinelOps Autonomous Daemon** | 👑 ENT | Agen orkestrasi pemindaian background dan remediasi hibrida (Dry-run, Canary, Instant Rollback). |
| 15 | **Subscription & Sovereign Licensing** | Core | Manajemen kuota tenant, hardware node binding, dan verifikasi lisensi offline air-gapped. |

---

## 📊 Matriks Perbandingan Paket Lisensi

| Fitur & Kapabilitas Teknis | 🌱 Community (Free) | ⭐ Professional (Pro) | 👑 Enterprise Sovereign (Tertinggi) |
|:---|:---:|:---:|:---:|
| **Tujuan Penggunaan** | Riset & Eksplorasi Dasar | DevSecOps & Tim Engineering | Bank, BUMN, Militer & Sovereign Air-Gap |
| **Model Distribusi** | Web Cloud / Desktop Demo | Workstation & Pipeline CI/CD | **100% Offline Air-Gap Hardware Locked** |
| **Kapasitas Aset & Node** | Maks. 25 Aset (1 Node) | Hingga 500 Aset (16 Nodes) | **Unlimited Local Assets & Multi-Node Cluster** |
| **CBOM Discovery & Deduplikasi** | ✅ Standar | ✅ Penuh (Shadow Crypto & Modes) | ✅ Penuh (Deduplikasi Deterministik SHA-256) |
| **PQC Code Playbooks Refactoring** | ✅ Snippet Contoh | ✅ Full Refactoring Engine | ✅ Full Multi-Language Hybrid Engine |
| **AI Mosca Risk (SNDL Exposure)** | ✅ Mode Standar | ✅ Telemetri & Horizon Dinamis | ✅ Prediktif Threat Modeling Lanjutan |
| **Crypto Agility Benchmark** | 🔒 Terkunci | ✅ **Terbuka Penuh** | ✅ **Terbuka Penuh** |
| **CI/CD Shift-Left Gatekeeper** | 🔒 Terkunci | ✅ **Terbuka Penuh** | ✅ **Terbuka Penuh** |
| **Zero-Code PQC Reverse Proxy** | 🔒 Terkunci | ✅ **Terbuka Penuh** | ✅ **Terbuka Penuh** |
| **Recurring Cron & Drift Detection** | 🔒 Terkunci | ✅ **Terbuka Penuh (&lt;30 Hari)** | ✅ **Terbuka Penuh (&lt;30 Hari)** |
| **Global Compliance & Reports Export** | 🔒 Terkunci | ✅ **Terbuka Penuh** | ✅ **Terbuka Penuh** |
| **Quantum CA & PKI Bridge** | 🔒 Terkunci | 🔒 Terkunci *(Butuh Enterprise)* | 🛡️ **Eksklusif Enterprise (FIPS 203/204)** |
| **ZentyTunnel PQC VPN** | 🔒 Terkunci | 🔒 Terkunci *(Butuh Enterprise)* | 🛡️ **Eksklusif Enterprise (Zero-Trust)** |
| **Merkle Audit & Ecosystem Ledger** | 🔒 Terkunci | 🔒 Terkunci *(Butuh Enterprise)* | 🛡️ **Eksklusif Enterprise (Tamper-Proof)** |
| **SentinelOps Multi-Core Remediation** | 🔒 Terkunci | 🔒 Terkunci *(Butuh Enterprise)* | 🛡️ **Eksklusif Enterprise (Canary & Rollback)** |

---

## 🔄 Panduan Upgrade Versi Aplikasi (Zero-Downtime)

Saat rilis versi baru diterbitkan (misalnya dari `v0.1.0` ke `v1.0.0`), Anda dapat memperbarui aplikasi tanpa khawatir kehilangan konfigurasi maupun lisensi aktif:

### Metode 1: Distribusi Biner Mandiri (`ZentyQuetry.exe`)
1. Unduh arsip rilis terbaru `ZentyQuetry-v1.0.0-windows-x64.zip` dari [GitHub Releases](https://github.com/camanit/ZentyQuetry-Dist/releases).
2. Tutup aplikasi yang sedang berjalan (`stop-zentyquetry.bat` atau tutup jendela aplikasi).
3. Ekstrak dan timpa berkas `ZentyQuetry.exe`, `desktop.html`, `desktop_app.js`, dan `styles.css` ke direktori instalasi Anda.
4. **PENTING**: Berkas `license.lic` yang sudah ada **TIDAK PERLU DIUBAH ATAU DIHAPUS**.
5. Jalankan kembali `ZentyQuetry.exe`. Sistem akan langsung berjalan pada versi baru dengan paket lisensi tetap aktif secara otomatis!

### Metode 2: Pembaruan Lingkungan Git Source
```bash
git pull origin main
# Untuk menjalankan desktop mode:
python desktop_runner.py
# Atau jalankan script batch:
start-zentyquetry.bat
```

---

## 🔑 Panduan Penerbitan & Aktivasi Lisensi Luring (Air-Gap)

ZentyQuetry menggunakan kriptografi asimetris **Ed25519** untuk menandatangani berkas lisensi digital secara luring. Lisensi ini mengunci hak akses ke perangkat keras fisik (*Hardware Node-Locking*) guna mencegah duplikasi ilegal pada data center tertutup (*air-gapped*).

### Langkah 1: Periksa Hardware Node ID Mesin Target
1. Jalankan aplikasi desktop ZentyQuetry.
2. Buka tab **Subscription & License** (atau lihat di status bar atas).
3. Salin kode Node ID perangkat Anda, contoh:
   ```text
   ZQ-NODE-5161-202A-F79C-05C7
   ```

### Langkah 2: Terbitkan Berkas Lisensi (`license.lic`)
1. Buka portal **License Authority** pengembang:
   * Jalankan `generate-license.bat` atau perintah:
     ```bash
     python license_generator.py
     ```
   * Buka browser pada alamat: `http://127.0.0.1:9528`
2. Masukkan **Nama Organisasi** dan **Email PIC**.
3. Pilih **Tier Lisensi**:
   * Pilih **`⭐ Professional`** untuk workstation developer / CI/CD pipeline.
   * Pilih **`👑 Enterprise Sovereign`** untuk implementasi penuh air-gap tanpa batas.
4. Pada kotak **Hardware Node ID**, tempelkan Node ID yang disalin pada Langkah 1 (atau klik tombol *Gunakan Node Ini*).
5. Klik **`TANDA TANGANI & TERBITKAN FILE (.LIC)`**.
6. Generator akan otomatis membuat dan menandatangani berkas `license.lic`.

### Langkah 3: Penempatan Berkas & Verifikasi Instan
1. Pastikan berkas `license.lic` berada di direktori root aplikasi ZentyQuetry.
2. Buka atau muat ulang (*refresh*) aplikasi desktop ZentyQuetry.
3. Node server secara otomatis memvalidasi tanda tangan kriptografi Ed25519 dan mengaktifkan seluruh modul berlisensi **tanpa perlu koneksi internet**.

---

## 💻 Menjalankan Aplikasi di Berbagai Lingkungan

### 1. Menjalankan Desktop App Mandiri (Windows)
Double-click `ZentyQuetry.exe` atau jalankan via terminal:
```cmd
start-zentyquetry.bat
```
Aplikasi akan membuka jendela *Chromium App Mode* mandiri pada port lokal `http://127.0.0.1:9527`.

### 2. Menjalankan SentinelOps Daemon untuk Scan Lokal
```bash
python sentinelops.py scan --mode=EDGE_DAEMON --target=localhost:443
```

### 3. Menjalankan Suite Pengujian (Unit Tests)
```bash
python -m unittest discover tests
```

---

## 🛡️ Standar Kepatuhan & Regulasi yang Didukung
* **NIST FIPS 203**: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM-768 / ML-KEM-1024).
* **NIST FIPS 204**: Module-Lattice-Based Digital Signature Standard (ML-DSA-65).
* **NIST FIPS 205**: Stateless Hash-Based Digital Signature Standard (SLH-DSA).
* **NIST FIPS 140-3**: Cryptographic Security Requirements for Cryptographic Modules.
* **BSI TR-02102 & CNSA 2.0**: Panduan transisi agilitas kriptografi kuantum pemerintah Jerman dan Amerika Serikat.
* **Regulasi Nasional (Indonesia)**: Kepatuhan pelindungan data kriptografis sesuai amanat UU No. 27 Tahun 2022 (UU PDP) dan Surat Edaran Keamanan Siber OJK.

---

&copy; 2026 ZentyQuetry™. Bagian dari ekosistem riset keamanan siber kuantum ctar.tech.
Hak Cipta Dilindungi Undang-Undang.
