#!/usr/bin/env python3
"""
CTARTech-ZentyQuetry(tm) Desktop License Authority (Developer HQ)
Sovereign Master License Generator & Ed25519 Airgap Signer.
Listens on http://127.0.0.1:9528 matching CTARTech Sovereign Standards.

Format lisensi identik dengan CTARTech-ZentyElastis:
  - Ed25519 signing (cryptography library)
  - signature_b64 base64
  - Unix timestamp issued_at / expires_at
  - Output file .lic

Usage:
    python license_generator.py
    -- atau --
    generate-license.bat
"""

import os, sys, json, base64, time, hashlib, platform, uuid, hmac
import http.server, socketserver, urllib.parse, threading, webbrowser
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

PORT     = 9528
HOST     = "127.0.0.1"
BASE_DIR = Path(__file__).resolve().parent
KEYS_DIR = BASE_DIR / "tools" / "license-issuer" / "keys"
PRIVATE_KEY_PATH  = KEYS_DIR / "private_key.pem"
PUBLIC_KEY_PATH   = KEYS_DIR / "public_key.pem"
WORKSPACE_PUBKEY  = BASE_DIR / "public_key.pem"
WORKSPACE_LIC     = BASE_DIR / "license.lic"
HISTORY_FILE      = BASE_DIR / ".license_history.json"

# ── Ed25519 Key Management ─────────────────────────────────────────────────────
def ensure_keypair():
    """Generate or load Ed25519 keypair. Returns private key object (or None if no crypto)."""
    if not HAS_CRYPTO:
        return None

    KEYS_DIR.mkdir(parents=True, exist_ok=True)

    if not PRIVATE_KEY_PATH.exists():
        priv_key = ed25519.Ed25519PrivateKey.generate()
        pem_priv = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        PRIVATE_KEY_PATH.write_bytes(pem_priv)

        pub_key  = priv_key.public_key()
        pem_pub  = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        PUBLIC_KEY_PATH.write_bytes(pem_pub)
        WORKSPACE_PUBKEY.write_bytes(pem_pub)
        print(f"  [NEW] Ed25519 keypair generated -> {KEYS_DIR}")
        return priv_key

    priv_key = serialization.load_pem_private_key(
        PRIVATE_KEY_PATH.read_bytes(), password=None
    )
    if not WORKSPACE_PUBKEY.exists() and PUBLIC_KEY_PATH.exists():
        WORKSPACE_PUBKEY.write_bytes(PUBLIC_KEY_PATH.read_bytes())

    return priv_key


def get_public_key_b64() -> str:
    if HAS_CRYPTO and PUBLIC_KEY_PATH.exists():
        raw = PUBLIC_KEY_PATH.read_bytes()
        lines = [l for l in raw.decode().split('\n') if l and not l.startswith('---')]
        return ''.join(lines)
    return "N/A (install: pip install cryptography)"


def sign_payload(payload: dict) -> str:
    """Sign canonical JSON with Ed25519. Falls back to HMAC-SHA256."""
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')

    if HAS_CRYPTO:
        priv_key = ensure_keypair()
        if priv_key:
            sig = priv_key.sign(canonical)
            return base64.b64encode(sig).decode('utf-8')

    # HMAC-SHA256 fallback
    machine_seed = f"ZENTY-SOVEREIGN-CA-2026-{platform.node()}-{uuid.getnode()}"
    key = hashlib.sha256(machine_seed.encode()).digest()
    sig = hmac.new(key, canonical, hashlib.sha256).digest()
    return base64.b64encode(sig).decode('utf-8')


def get_machine_node_id() -> str:
    raw    = f"{platform.node()}-{platform.processor()}-{platform.machine()}-{uuid.getnode()}"
    digest = hashlib.sha256(raw.encode()).hexdigest().upper()
    return f"ZQ-NODE-{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:16]}"


def get_key_status() -> str:
    if HAS_CRYPTO and PRIVATE_KEY_PATH.exists():
        return "Ed25519 Sovereign Key Active"
    if HAS_CRYPTO:
        return "Ed25519 Key (will generate on first use)"
    return "HMAC-SHA256 Fallback (pip install cryptography for Ed25519)"


# ── License Issuer ─────────────────────────────────────────────────────────────
def issue_license(org: str, product: str, tier: str, days: int,
                  max_nodes: int, max_assets: int, features: list,
                  node_id: str, email: str, edition: str = "DESKTOP") -> dict:

    now  = int(time.time())
    exp  = (now + days * 86400) if days > 0 else None
    slug = org.upper().replace(" ", "_").replace(".", "").replace(",", "")[:16]
    client_id = f"CTAR-{product[:8].upper()}-{slug}-{now % 100000}"

    payload = {
        "issuer"    : f"CTARTech-{product} Sovereign Authority",
        "client_id" : client_id,
        "org_name"  : org,
        "email"     : email,
        "product"   : product,
        "edition"   : (edition or "DESKTOP").upper(),  # DESKTOP | WEB | HYBRID
        "tier"      : tier,
        "max_nodes" : max_nodes,
        "max_assets": max_assets,
        "allowed_node": node_id or "ZQ-NODE-ANY",
        "features"  : features,
        "issued_at" : now,
        "expires_at": exp,
        "perpetual" : days == 0,
        "status"    : "ACTIVE",
    }

    sig_b64 = sign_payload(payload)

    doc = {
        "version"      : "1.0",
        "algorithm"    : "Ed25519" if HAS_CRYPTO else "HMAC-SHA256",
        "payload"      : payload,
        "signature_b64": sig_b64,
        "authority"    : f"CTARTech-{product} Sovereign License Authority",
        "generated_at" : datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

    # Save as license.lic in workspace root (overwrite active license)
    WORKSPACE_LIC.write_text(json.dumps(doc, indent=2, ensure_ascii=False), 'utf-8')

    # History
    try:
        hist = json.loads(HISTORY_FILE.read_text('utf-8')) if HISTORY_FILE.exists() else []
        hist.insert(0, {
            "client_id": client_id, "org": org, "product": product,
            "tier": tier, "node": node_id or "ANY",
            "expires": datetime.utcfromtimestamp(exp).strftime('%Y-%m-%d') if exp else "PERPETUAL",
            "issued_at": datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M UTC'),
        })
        HISTORY_FILE.write_text(json.dumps(hist[:100], indent=2), 'utf-8')
    except Exception:
        pass

    return doc


# ── HTML UI ────────────────────────────────────────────────────────────────────
HTML_PAGE = """\
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CTARTech-ZentyQuetry License Authority</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    :root{
      --bg:#060912;--bg2:#0a0f1e;--bg3:#0f1629;--bg4:#141b30;
      --bdr:rgba(99,102,241,0.18);
      --pur:#a855f7;--cyn:#06b6d4;--grn:#10b981;--amb:#f59e0b;--ros:#f43f5e;
      --tx1:#e2e8f0;--tx2:#94a3b8;--tx3:#64748b;
      --mono:'JetBrains Mono',monospace;
    }
    body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx1);min-height:100vh}
    body::before{content:'';position:fixed;inset:0;pointer-events:none;
      background:radial-gradient(ellipse 60% 40% at 15% 10%,rgba(168,85,247,.08) 0%,transparent 60%),
                 radial-gradient(ellipse 50% 35% at 85% 90%,rgba(6,182,212,.05) 0%,transparent 60%)}
    .wrap{position:relative;z-index:1;max-width:1140px;margin:0 auto;padding:0 1.5rem 3rem}
    /* header */
    .hd{display:flex;align-items:center;justify-content:space-between;padding:1.1rem 2rem;
      background:rgba(15,22,41,.88);border-bottom:1px solid var(--bdr);
      backdrop-filter:blur(12px);position:sticky;top:0;z-index:100}
    .hd-brand{display:flex;align-items:center;gap:.9rem}
    .hd-logo{width:42px;height:42px;border-radius:10px;
      background:linear-gradient(135deg,#a855f7,#6366f1);
      display:flex;align-items:center;justify-content:center;
      font-size:1.2rem;font-weight:800;color:#fff;
      box-shadow:0 0 18px rgba(168,85,247,.45)}
    .hd-t{font-size:.97rem;font-weight:700}
    .hd-s{font-size:.7rem;color:var(--tx2);margin-top:1px}
    .badge{display:flex;align-items:center;gap:.45rem;
      background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.3);
      padding:4px 11px;border-radius:20px;font-size:.71rem;font-weight:600;color:var(--grn)}
    .badge::before{content:"\\25CF";font-size:.5rem;animation:pulse 2s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
    /* grid */
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:1.4rem;margin-top:1.8rem}
    @media(max-width:760px){.grid{grid-template-columns:1fr}}
    /* cards */
    .card{background:var(--bg4);border:1px solid var(--bdr);border-radius:13px;padding:1.4rem}
    .ct{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;
      color:var(--tx2);margin-bottom:1.2rem;display:flex;align-items:center;gap:.45rem}
    .ct svg{width:13px;height:13px}
    /* form */
    .fg{margin-bottom:.85rem}
    label{display:block;font-size:.74rem;font-weight:500;color:var(--tx2);margin-bottom:.28rem}
    input,select{width:100%;padding:.52rem .78rem;
      background:rgba(0,0,0,.38);border:1px solid rgba(99,102,241,.2);
      border-radius:7px;color:var(--tx1);font-family:inherit;font-size:.83rem;
      transition:border-color .2s;outline:none}
    input:focus,select:focus{border-color:var(--pur);box-shadow:0 0 0 3px rgba(168,85,247,.12)}
    select option{background:var(--bg2)}
    small{font-size:.68rem;color:var(--tx3);display:block;margin-top:.22rem}
    .g2{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}
    /* features */
    .feats{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}
    .fi{display:flex;align-items:center;gap:.4rem;
      background:rgba(0,0,0,.25);border:1px solid rgba(99,102,241,.14);
      padding:.42rem .6rem;border-radius:7px;cursor:pointer;transition:border-color .2s}
    .fi:hover{border-color:var(--pur)}
    .fi input[type=checkbox]{width:auto;accent-color:var(--pur)}
    .fi span{font-size:.76rem}
    /* machine box */
    .mb{background:rgba(0,0,0,.32);border:1px dashed rgba(6,182,212,.25);
      border-radius:8px;padding:.62rem .88rem;margin-bottom:.85rem}
    .mb-id{font-family:var(--mono);font-size:.84rem;color:var(--cyn);font-weight:600;letter-spacing:.05em}
    .mb-lbl{font-size:.66rem;text-transform:uppercase;color:var(--tx3);letter-spacing:.06em;margin-bottom:.18rem}
    /* buttons */
    .btn-gen{width:100%;padding:.78rem;
      background:linear-gradient(135deg,#a855f7,#6366f1);
      border:none;border-radius:9px;color:#fff;font-size:.86rem;font-weight:700;
      cursor:pointer;margin-top:.9rem;
      display:flex;align-items:center;justify-content:center;gap:.55rem;
      transition:transform .15s,box-shadow .15s;
      box-shadow:0 4px 20px rgba(168,85,247,.35)}
    .btn-gen:hover{transform:translateY(-1px);box-shadow:0 6px 26px rgba(168,85,247,.5)}
    .btn-sec{padding:.44rem .85rem;border-radius:7px;background:transparent;
      border:1px solid rgba(99,102,241,.28);color:var(--tx2);
      font-size:.76rem;font-weight:500;cursor:pointer;transition:all .2s}
    .btn-sec:hover{border-color:var(--cyn);color:var(--cyn)}
    .btn-dl{padding:.52rem .95rem;border-radius:7px;
      background:linear-gradient(135deg,rgba(16,185,129,.2),rgba(6,182,212,.1));
      border:1px solid var(--grn);color:var(--grn);
      font-size:.78rem;font-weight:600;cursor:pointer;transition:all .2s;
      display:inline-flex;align-items:center;gap:.38rem}
    .btn-dl:disabled{opacity:.35;cursor:not-allowed}
    .btn-dl:not(:disabled):hover{background:rgba(16,185,129,.28)}
    .btn-cp{padding:.52rem .85rem;border-radius:7px;background:transparent;
      border:1px solid rgba(6,182,212,.28);color:var(--cyn);
      font-size:.76rem;font-weight:500;cursor:pointer;transition:all .2s;
      display:inline-flex;align-items:center;gap:.35rem}
    .btn-cp:disabled{opacity:.35;cursor:not-allowed}
    /* preview */
    .prev{background:rgba(0,0,0,.52);border:1px dashed rgba(168,85,247,.22);
      border-radius:9px;padding:.9rem;min-height:240px;max-height:350px;
      overflow-y:auto;margin-bottom:.9rem;position:relative}
    .prev pre{font-family:var(--mono);font-size:.73rem;color:#a5f3fc;
      line-height:1.7;white-space:pre-wrap;word-break:break-all}
    .ph{color:var(--tx3);font-size:.78rem;position:absolute;top:50%;left:50%;
      transform:translate(-50%,-50%);text-align:center;line-height:1.9}
    .arow{display:flex;gap:.52rem;flex-wrap:wrap;margin-bottom:.9rem}
    /* info + sk */
    .ibox{background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);
      border-radius:8px;padding:.75rem .9rem;font-size:.74rem;color:var(--tx2);line-height:1.8}
    .ibox strong{color:var(--grn)}
    .sk{margin-top:.9rem;padding:.6rem .88rem;
      background:rgba(168,85,247,.06);border:1px solid rgba(168,85,247,.2);border-radius:8px}
    .sk-lbl{font-size:.66rem;text-transform:uppercase;color:var(--tx3);letter-spacing:.06em;margin-bottom:.25rem}
    .sk-val{font-family:var(--mono);font-size:.72rem;color:var(--pur)}
    /* toast */
    #toast{position:fixed;bottom:20px;right:20px;z-index:9999;
      background:rgba(10,14,26,.97);border-radius:10px;padding:11px 15px;
      max-width:320px;font-size:.8rem;line-height:1.5;
      box-shadow:0 8px 28px rgba(0,0,0,.6);display:none}
    #toast.show{display:block;animation:up .3s ease}
    @keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    @keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    ::-webkit-scrollbar{width:5px}::-webkit-scrollbar-thumb{background:rgba(99,102,241,.3);border-radius:3px}
    .mono{font-family:var(--mono);font-size:.8rem}
    code{background:rgba(99,102,241,.15);padding:1px 5px;border-radius:4px;
         font-family:var(--mono);font-size:.85em}
  </style>
</head>
<body>

<header class="hd">
  <div class="hd-brand">
    <div class="hd-logo">Z</div>
    <div>
      <div class="hd-t">CTARTech-ZentyQuetry&#8482; License Authority</div>
      <div class="hd-s">Desktop Master Generator &amp; Ed25519 Airgap Signer (Developer HQ)</div>
    </div>
  </div>
  <div class="badge" id="key-badge">Loading&#8230;</div>
</header>

<div class="wrap">
  <div class="grid">

    <!-- LEFT: FORM -->
    <div class="card">
      <div class="ct">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
        Konfigurasi Sertifikat Lisensi Klien
      </div>

      <div class="mb">
        <div class="mb-lbl">Node ID Mesin Ini (auto-detect)</div>
        <div class="mb-id" id="this-node">Loading&#8230;</div>
        <small style="margin-top:.3rem">Klik tombol untuk mengunci lisensi ke mesin ini.</small>
        <div style="margin-top:.45rem">
          <button class="btn-sec" onclick="useThisNode()">&#128204; Gunakan Node Ini</button>
        </div>
      </div>

      <div class="fg">
        <label>Nama Organisasi / Perusahaan Klien</label>
        <input type="text" id="f-org" placeholder="PT Bank Mandiri (Persero) Tbk">
      </div>
      <div class="fg">
        <label>Email PIC / Administrator</label>
        <input type="email" id="f-email" placeholder="admin@perusahaan.co.id">
      </div>
      <div class="fg">
        <label>Produk / Aplikasi</label>
        <select id="f-product">
          <option value="ZentyQuetry">ZentyQuetry &#8212; PQC &amp; CBOM Engine</option>
          <option value="ZentyElastic">ZentyElastic &#8212; Elastic Search &amp; Log Analytics</option>
          <option value="ZentyCore">ZentyCore &#8212; SSO &amp; IAM Platform</option>
          <option value="ZentyInfoSec">ZentyInfoSec &#8212; SOC / SIEM</option>
          <option value="ZentyTeamScore">ZentyTeamScore &#8212; KPI &amp; Migration Tracker</option>
          <option value="ZentyVault">ZentyVault &#8212; Secure Secrets Manager</option>
        </select>
        <div class="fg">
          <label>Target Platform / Edisi Lisensi</label>
          <select id="f-edition">
            <option value="DESKTOP" selected>💻 Desktop Sovereign Node (Offline Air-Gap)</option>
            <option value="WEB">🌐 Web Enterprise Cloud (Multi-Tenant SaaS)</option>
            <option value="HYBRID">🛡️ Universal Hybrid (Web SaaS + Desktop Nodes)</option>
          </select>
        </div>
      </div>
      <div class="g2">
        <div class="fg">
          <label>Tier Lisensi</label>
          <select id="f-tier">
            <option value="Community">&#127358; Community (Free)</option>
            <option value="Professional">&#11088; Professional</option>
            <option value="Enterprise" selected>&#127970; Enterprise Airgap</option>
            <option value="Enterprise Sovereign">&#128081; Enterprise Sovereign</option>
          </select>
        </div>
        <div class="fg">
          <label>Masa Berlaku (Hari, 0=perpetual)</label>
          <input type="number" id="f-days" value="365" min="0">
        </div>
      </div>
      <div class="fg">
        <label>Hardware Node ID (kosong = ANY node)</label>
        <input type="text" id="f-node" class="mono" placeholder="ZQ-NODE-XXXX-XXXX-XXXX-XXXX">
        <small>Kosongkan untuk web/cloud. Untuk desktop, paste ZQ-NODE dari mesin target.</small>
      </div>
      <div class="g2">
        <div class="fg">
          <label>Kapasitas Maksimal Node / Hardware</label>
          <select id="f-nodes">
            <option value="4">4 Nodes (Starter)</option>
            <option value="16">16 Nodes (Professional)</option>
            <option value="32">32 Nodes (Enterprise)</option>
            <option value="64" selected>64 Nodes (Enterprise Cluster)</option>
            <option value="256">256 Nodes (Sovereign)</option>
            <option value="0">Unlimited (Sovereign+)</option>
          </select>
        </div>
        <div class="fg">
          <label>Maks. Protected Assets</label>
          <input type="number" id="f-assets" value="500" min="0">
        </div>
      </div>
      <div class="fg">
        <label>Modul Fitur Berlisensi</label>
        <div class="feats">
          <label class="fi"><input type="checkbox" id="ft-cbom" checked><span>&#9889; CBOM Scanner</span></label>
          <label class="fi"><input type="checkbox" id="ft-pqc" checked><span>&#128272; PQC Migration</span></label>
          <label class="fi"><input type="checkbox" id="ft-sentinel"><span>&#128737; SentinelOps</span></label>
          <label class="fi"><input type="checkbox" id="ft-api"><span>&#128279; API Access</span></label>
          <label class="fi"><input type="checkbox" id="ft-multi"><span>&#127970; Multi-Tenant</span></label>
          <label class="fi"><input type="checkbox" id="ft-audit" checked><span>&#128203; SOC Merkle Audit</span></label>
          <label class="fi"><input type="checkbox" id="ft-pki"><span>&#128273; PKI Bridge</span></label>
          <label class="fi"><input type="checkbox" id="ft-sla" checked><span>&#9201; SLAShield</span></label>
        </div>
      </div>
      <button class="btn-gen" id="btn-gen" onclick="generateLicense()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        TANDA TANGANI &amp; TERBITKAN FILE (.LIC)
      </button>
    </div>

    <!-- RIGHT: PREVIEW -->
    <div class="card">
      <div class="ct">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        Berkas Lisensi Bertanda Tangan
      </div>

      <div class="prev">
        <div class="ph" id="ph">&#128274; Menunggu penerbitan lisensi kriptografi Ed25519&#8230;<br><small>Isi form di kiri lalu klik "Tanda Tangani"</small></div>
        <pre id="prev-code" style="display:none"></pre>
      </div>

      <div class="arow">
        <button class="btn-dl" id="btn-dl" disabled onclick="downloadLIC()">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Download .lic
        </button>
        <button class="btn-cp" id="btn-cp" disabled onclick="copyJSON()">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          Copy JSON
        </button>
        <button class="btn-sec" onclick="resetPrev()">Clear</button>
      </div>

      <div class="ibox">
        <strong>Cara distribusi lisensi:</strong><br>
        1. Generate &#8594; Download file <code>.lic</code> atau copy JSON<br>
        2. Kirim ke klien / pengguna desktop<br>
        3. Untuk desktop: simpan sebagai <code>license.lic</code> di folder aplikasi<br>
        4. Untuk web: upload via tab <strong>Subscription &amp; Licensing</strong>
      </div>

      <div class="sk">
        <div class="sk-lbl">Signing Key Info (This Machine)</div>
        <div class="sk-val" id="sk-val">Loading&#8230;</div>
      </div>
    </div>

  </div>
</div>

<div id="toast"></div>

<script>
let _lic = null;

async function loadMachineInfo() {
  try {
    const d = await fetch('/api/machine').then(r => r.json());
    document.getElementById('this-node').textContent = d.node_id;
    document.getElementById('key-badge').textContent = d.key_status;
    document.getElementById('sk-val').textContent = d.algorithm + ' | ' + d.key_status;
  } catch(e) {
    document.getElementById('this-node').textContent = 'ZQ-NODE-OFFLINE-FALLBACK';
  }
}

function useThisNode() {
  document.getElementById('f-node').value = document.getElementById('this-node').textContent;
  toast('Node ID di-paste ke form!', '#06b6d4');
}

async function generateLicense() {
  const org = document.getElementById('f-org').value.trim();
  if (!org) { toast('Isi nama organisasi!', '#f43f5e'); return; }

  const features = [];
  const map = {
    'ft-cbom':'CBOM_SCANNER','ft-pqc':'PQC_MIGRATION_ENGINE',
    'ft-sentinel':'SENTINELOPS_AGENT','ft-api':'API_ACCESS',
    'ft-multi':'MULTI_TENANT','ft-audit':'SOC_MERKLE_AUDIT',
    'ft-pki':'PKI_BRIDGE','ft-sla':'SLASHIELD_LATENCY_GUARD'
  };
  for (const [id, feat] of Object.entries(map)) {
    if (document.getElementById(id).checked) features.push(feat);
  }

  const btn = document.getElementById('btn-gen');
  btn.disabled = true;
  btn.innerHTML = '<span style="display:inline-block;animation:spin 1s linear infinite">&#9651;</span>&nbsp;Menandatangani dengan Ed25519&#8230;';

  try {
    const body = {
      org, email: document.getElementById('f-email').value.trim(),
      product:  document.getElementById('f-product').value,
      edition:  document.getElementById('f-edition') ? document.getElementById('f-edition').value : 'DESKTOP',
      tier:     document.getElementById('f-tier').value,
      days:     parseInt(document.getElementById('f-days').value) || 365,
      node:     document.getElementById('f-node').value.trim(),
      max_nodes:parseInt(document.getElementById('f-nodes').value) || 64,
      assets:   parseInt(document.getElementById('f-assets').value) || 500,
      features,
    };
    const r   = await fetch('/api/generate', { method:'POST',
      headers:{'Content-Type':'application/json'}, body:JSON.stringify(body) });
    const lic = await r.json();
    if (lic.error) throw new Error(lic.error);
    _lic = lic;

    document.getElementById('ph').style.display = 'none';
    const pre = document.getElementById('prev-code');
    pre.style.display = 'block';
    pre.textContent = JSON.stringify(lic, null, 2);
    document.getElementById('btn-dl').disabled = false;
    document.getElementById('btn-cp').disabled = false;
    toast('Lisensi berhasil diterbitkan dan ditandatangani!', '#10b981');
  } catch(e) {
    toast('Error: ' + e.message, '#f43f5e');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> TANDA TANGANI &amp; TERBITKAN FILE (.LIC)';
  }
}

function downloadLIC() {
  if (!_lic) return;
  const blob = new Blob([JSON.stringify(_lic, null, 2)], {type:'application/json'});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  const org  = (_lic.payload?.org_name || 'license').replace(/[^a-zA-Z0-9]/g,'_').slice(0,30);
  const cid  = _lic.payload?.client_id || 'ZQ-LIC';
  a.href = url; a.download = cid + '_' + org + '.lic';
  a.click(); URL.revokeObjectURL(url);
  toast('File .lic berhasil didownload!', '#10b981');
}

function copyJSON() {
  if (!_lic) return;
  navigator.clipboard.writeText(JSON.stringify(_lic, null, 2))
    .then(() => toast('JSON lisensi berhasil dicopy!', '#06b6d4'))
    .catch(() => toast('Gagal copy', '#f43f5e'));
}

function resetPrev() {
  _lic = null;
  document.getElementById('ph').style.display = '';
  const pre = document.getElementById('prev-code');
  pre.style.display = 'none'; pre.textContent = '';
  document.getElementById('btn-dl').disabled = true;
  document.getElementById('btn-cp').disabled = true;
}

function toast(msg, color) {
  const el = document.getElementById('toast');
  el.style.borderColor = color; el.style.color = color;
  el.textContent = msg; el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 4000);
}

loadMachineInfo();
</script>
</body>
</html>
"""

# ── HTTP Handler ───────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _j(self, data, s=200):
        b = json.dumps(data, indent=2, ensure_ascii=False).encode()
        self.send_response(s)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length', len(b))
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers(); self.wfile.write(b)

    def _h(self, html):
        b = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length', len(b))
        self.end_headers(); self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()

    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p in ('/', '/index.html'):
            self._h(HTML_PAGE)
        elif p == '/api/machine':
            self._j({
                'node_id'   : get_machine_node_id(),
                'algorithm' : 'Ed25519' if HAS_CRYPTO else 'HMAC-SHA256',
                'key_status': get_key_status(),
                'platform'  : platform.system(),
                'hostname'  : platform.node(),
                'crypto_lib': HAS_CRYPTO,
            })
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        if p != '/api/generate':
            self.send_response(404); self.end_headers(); return
        try:
            req = json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
        except Exception:
            self._j({'error':'Invalid JSON'},400); return

        try:
            doc = issue_license(
                org       = req.get('org','Unknown'),
                product   = req.get('product','ZentyQuetry'),
                edition   = req.get('edition','DESKTOP'),
                tier      = req.get('tier','Enterprise'),
                days      = int(req.get('days',365)),
                max_nodes = int(req.get('max_nodes',64)),
                max_assets= int(req.get('assets',500)),
                features  = req.get('features',[]),
                node_id   = req.get('node','').strip(),
                email     = req.get('email',''),
            )
            self._j(doc)
        except Exception as e:
            self._j({'error': str(e)}, 500)


# ── Entry Point ────────────────────────────────────────────────────────────────
def main():
    # Pre-generate keypair on startup
    ensure_keypair()
    node_id = get_machine_node_id()
    algo    = 'Ed25519' if HAS_CRYPTO else 'HMAC-SHA256 (pip install cryptography for Ed25519)'

    print("=" * 70)
    print("  CTARTech-ZentyQuetry(tm) LICENSE AUTHORITY -- DESKTOP GENERATOR")
    print("=" * 70)
    print(f"  URL           : http://{HOST}:{PORT}")
    print(f"  Machine Node  : {node_id}")
    print(f"  Signing Algo  : {algo}")
    print(f"  Private Key   : {PRIVATE_KEY_PATH}")
    print(f"  Public Key    : {WORKSPACE_PUBKEY}")
    print(f"  Output .lic   : {WORKSPACE_LIC}")
    print("=" * 70 + "\n")

    if not HAS_CRYPTO:
        print("  [WARN] 'cryptography' library not found. Using HMAC-SHA256 fallback.")
        print("         For Ed25519 (like ZentyElastis): pip install cryptography\n")

    # Open browser after 0.8s
    threading.Thread(
        target=lambda: (time.sleep(0.8), webbrowser.open(f"http://{HOST}:{PORT}")),
        daemon=True
    ).start()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"[+] Serving at http://{HOST}:{PORT}  (Ctrl+C to quit)\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] License Authority shut down.")


if __name__ == '__main__':
    main()
