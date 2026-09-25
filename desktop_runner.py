#!/usr/bin/env python3
"""
ZentyQuetry Sovereign Desktop Edition Launcher (Offline & Air-Gapped)
====================================================================
Serves the ZentyQuetry console locally. Enforces:
  - Hardware node fingerprint (ZQ-NODE-XXXX) tied to this machine
  - license.lic validation before full app access
  - Community mode if no license present
  - Ed25519 / HMAC-SHA256 signature verification

Usage:
    python desktop_runner.py [--port 9527] [--browser]
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import hmac
import hashlib
import platform
import uuid
import base64
import time
import threading
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs

PORT     = 9527
HOST     = "127.0.0.1"
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent
LIC_FILE = BASE_DIR / "license.lic"

# ── Hardware Node Fingerprint ──────────────────────────────────────────────────
def get_node_id() -> str:
    raw = f"{platform.node()}-{platform.processor()}-{platform.machine()}-{uuid.getnode()}"
    digest = hashlib.sha256(raw.encode()).hexdigest().upper()
    return f"ZQ-NODE-{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:16]}"

NODE_ID = get_node_id()

# ── License Verification ───────────────────────────────────────────────────────
def _hmac_verify(payload: dict, sig_b64: str) -> bool:
    """Verify HMAC-SHA256 fallback signature."""
    try:
        seed = f"ZENTY-SOVEREIGN-CA-2026-{platform.node()}-{uuid.getnode()}"
        key  = hashlib.sha256(seed.encode()).digest()
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
        expected  = hmac.new(key, canonical, hashlib.sha256).digest()
        return base64.b64encode(expected).decode() == sig_b64
    except Exception:
        return False

def _ed25519_verify(payload: dict, sig_b64: str) -> bool:
    """Verify Ed25519 signature using public_key.pem in workspace root."""
    pub_path = BASE_DIR / "public_key.pem"
    if not pub_path.exists():
        return False
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        pub_pem  = pub_path.read_bytes()
        pub_key  = serialization.load_pem_public_key(pub_pem)
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
        sig_bytes = base64.b64decode(sig_b64)
        pub_key.verify(sig_bytes, canonical)
        return True
    except Exception:
        return False

def validate_license(lic_path: Path = LIC_FILE) -> dict:
    """
    Validate license.lic. Returns:
      { valid, plan, features, node_locked, allowed_node, message, expires_at }
    """
    # No file → Community
    if not lic_path.exists():
        return {
            "valid": True, "plan": "COMMUNITY", "mode": "COMMUNITY",
            "features": ["cbom_scanner", "pqc_migration"],
            "node_locked": False, "allowed_node": "ANY",
            "message": "No license.lic found. Running in Community (Free) mode.",
            "expires_at": None, "perpetual": True,
        }

    try:
        doc = json.loads(lic_path.read_text('utf-8'))
    except Exception as e:
        return {"valid": False, "plan": "INVALID", "mode": "ERROR",
                "message": f"license.lic is not valid JSON: {e}"}

    payload   = doc.get("payload", {})
    sig_b64   = doc.get("signature_b64", "")
    algorithm = doc.get("algorithm", "HMAC-SHA256")

    # 1. Signature check
    if algorithm == "Ed25519":
        sig_ok = _ed25519_verify(payload, sig_b64)
        if not sig_ok:
            # Fallback to HMAC (for dev/demo licenses)
            sig_ok = _hmac_verify(payload, sig_b64)
    else:
        sig_ok = _hmac_verify(payload, sig_b64)

    if not sig_ok:
        return {
            "valid": False, "plan": "INVALID", "mode": "SIGNATURE_FAIL",
            "message": "License signature verification FAILED. File may be tampered.",
            "node_locked": False, "allowed_node": "NONE",
        }

    # 2. Expiry check
    expires_at = payload.get("expires_at")
    perpetual  = payload.get("perpetual", False)
    now_ts     = int(time.time())
    if expires_at and not perpetual and int(expires_at) < now_ts:
        return {
            "valid": False, "plan": "EXPIRED", "mode": "EXPIRED",
            "message": f"License expired on {datetime.utcfromtimestamp(int(expires_at)).strftime('%Y-%m-%d')}. "
                       f"Downgraded to Community mode.",
            "node_locked": False, "allowed_node": "ANY",
        }

    # 3. Node lock check
    allowed_node = payload.get("allowed_node", "ZQ-NODE-ANY")
    node_locked  = allowed_node != "ZQ-NODE-ANY" and allowed_node != "ANY"

    if node_locked and allowed_node != NODE_ID:
        return {
            "valid": False, "plan": "NODE_MISMATCH", "mode": "NODE_LOCKED",
            "message": f"License node-locked to: {allowed_node}\nThis machine: {NODE_ID}\nContact your license administrator.",
            "node_locked": True,
            "allowed_node": allowed_node,
            "this_node": NODE_ID,
        }

    return {
        "valid": True,
        "plan": payload.get("tier", "Enterprise"),
        "mode": "ACTIVE",
        "features": payload.get("features", []),
        "max_assets": payload.get("max_assets", 500),
        "max_agents": payload.get("max_agents", 10),
        "node_locked": node_locked,
        "allowed_node": allowed_node,
        "expires_at": expires_at,
        "perpetual": perpetual,
        "client_id": payload.get("client_id", ""),
        "org_name": payload.get("org_name", ""),
        "authority": doc.get("authority", ""),
        "message": f"License ACTIVE · Plan: {payload.get('tier', 'Enterprise')} · Node: {'Locked' if node_locked else 'Any'}",
    }

# Global license state (loaded once at startup)
LICENSE = validate_license()

# ── Activation Screen HTML ─────────────────────────────────────────────────────
ACTIVATION_HTML = """\
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>ZentyQuetry — Aktivasi Lisensi Desktop</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Inter',sans-serif;background:#060912;color:#e2e8f0;
      min-height:100vh;display:flex;align-items:center;justify-content:center;
      background:radial-gradient(ellipse 70% 60% at 50% 30%,rgba(168,85,247,.12) 0%,transparent 70%)}}
    .box{{max-width:520px;width:95%;background:#0f1629;border:1px solid rgba(168,85,247,.3);
      border-radius:16px;padding:2.2rem;box-shadow:0 24px 64px rgba(0,0,0,.7)}}
    .logo{{width:52px;height:52px;background:linear-gradient(135deg,#a855f7,#6366f1);
      border-radius:12px;display:flex;align-items:center;justify-content:center;
      font-size:1.5rem;font-weight:800;color:#fff;margin:0 auto 1.2rem;
      box-shadow:0 0 24px rgba(168,85,247,.5)}}
    h1{{font-size:1.2rem;font-weight:700;text-align:center;margin-bottom:.4rem}}
    .sub{{font-size:.78rem;color:#94a3b8;text-align:center;margin-bottom:1.8rem}}
    .node-box{{background:rgba(0,0,0,.4);border:1px dashed rgba(6,182,212,.3);
      border-radius:9px;padding:.9rem 1rem;margin-bottom:1.4rem}}
    .node-lbl{{font-size:.68rem;text-transform:uppercase;color:#64748b;letter-spacing:.06em}}
    .node-id{{font-family:'JetBrains Mono',monospace;font-size:1rem;
      color:#06b6d4;font-weight:600;letter-spacing:.05em;margin:.2rem 0}}
    .node-hint{{font-size:.7rem;color:#64748b}}
    .status-{mode_class}{{padding:.7rem 1rem;border-radius:8px;margin-bottom:1.2rem;
      font-size:.82rem;line-height:1.6;
      background:rgba({status_bg});border:1px solid rgba({status_bdr})}}
    textarea{{width:100%;padding:.7rem .85rem;background:rgba(0,0,0,.4);
      border:1px solid rgba(99,102,241,.2);border-radius:8px;color:#e2e8f0;
      font-family:'JetBrains Mono',monospace;font-size:.78rem;
      min-height:140px;resize:vertical;outline:none;margin-bottom:.9rem}}
    textarea:focus{{border-color:#a855f7;box-shadow:0 0 0 3px rgba(168,85,247,.12)}}
    .btn{{width:100%;padding:.78rem;background:linear-gradient(135deg,#a855f7,#6366f1);
      border:none;border-radius:9px;color:#fff;font-size:.9rem;font-weight:700;
      cursor:pointer;letter-spacing:.03em;box-shadow:0 4px 18px rgba(168,85,247,.4)}}
    .btn:hover{{opacity:.9}}
    .btn-sec{{width:100%;padding:.62rem;background:transparent;
      border:1px solid rgba(99,102,241,.3);border-radius:8px;color:#94a3b8;
      font-size:.8rem;cursor:pointer;margin-top:.6rem}}
    .btn-sec:hover{{border-color:#06b6d4;color:#06b6d4}}
    #msg{{margin-top:.8rem;font-size:.8rem;text-align:center;min-height:1.2rem}}
    .ok{{color:#10b981}} .err{{color:#f43f5e}} .warn{{color:#f59e0b}}
    .community-note{{font-size:.74rem;color:#64748b;text-align:center;margin-top:1.2rem;
      padding:.7rem;border:1px dashed rgba(99,102,241,.2);border-radius:8px}}
    code{{background:rgba(99,102,241,.15);padding:1px 5px;border-radius:4px;
      font-family:'JetBrains Mono',monospace;font-size:.85em}}
  </style>
</head>
<body>
<div class="box">
  <div class="logo">Z</div>
  <h1>ZentyQuetry&#8482; Desktop Edition</h1>
  <p class="sub">NIST Post-Quantum Cryptography &amp; CBOM Management Engine<br>
  Aktivasi Lisensi Diperlukan untuk Akses Penuh</p>

  <div class="node-box">
    <div class="node-lbl">Node ID Perangkat Ini</div>
    <div class="node-id" id="node-id">{node_id}</div>
    <div class="node-hint">Salin ID ini dan kirim ke administrator lisensi untuk mendapatkan file .lic</div>
  </div>

  <div class="status-{mode_class}" style="background:rgba({status_bg});border:1px solid rgba({status_bdr})">
    {status_msg}
  </div>

  <div>
    <label style="font-size:.74rem;color:#94a3b8;display:block;margin-bottom:.35rem">
      Paste isi file <code>license.lic</code> di bawah, atau simpan file .lic di folder aplikasi dan restart:
    </label>
    <textarea id="lic-input" placeholder='{{"version":"1.0","algorithm":"Ed25519","payload":{{...}},"signature_b64":"..."}}'></textarea>
    <button class="btn" onclick="activateLicense()">&#128274; Aktifkan Lisensi</button>
    <button class="btn-sec" onclick="continueAsComm()">Lanjutkan sebagai Community (Free)</button>
    <div id="msg"></div>
  </div>

  <div class="community-note">
    &#128274; <strong>Community Mode:</strong> CBOM Scanner &amp; PQC Migration tersedia gratis.<br>
    Untuk fitur Enterprise (SentinelOps, Multi-Tenant, API Access), hubungi
    <strong>ctar.tech</strong> atau kunjungi
    <a href="https://github.com/camanit/ZentyQuetry-Dist" target="_blank"
       style="color:#a855f7;">ZentyQuetry-Dist</a>.
  </div>
</div>

<script>
async function activateLicense() {{
  const raw = document.getElementById('lic-input').value.trim();
  const msg = document.getElementById('msg');
  if (!raw) {{ msg.className='err'; msg.textContent='Paste isi license.lic terlebih dahulu.'; return; }}

  let doc;
  try {{ doc = JSON.parse(raw); }} catch(e) {{
    msg.className='err'; msg.textContent='Format JSON tidak valid: ' + e.message; return;
  }}

  msg.className=''; msg.textContent='Memverifikasi tanda tangan...';

  const r = await fetch('/activate-license', {{
    method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{ license_json: doc }})
  }});
  const d = await r.json();

  if (d.status === 'ACTIVATED') {{
    msg.className='ok';
    msg.textContent = '✅ Lisensi berhasil diaktifkan! Plan: ' + d.plan + ' · Mengarahkan...';
    setTimeout(() => {{ location.href = '/'; }}, 1800);
  }} else {{
    msg.className='err';
    msg.textContent = '❌ ' + (d.message || 'Aktivasi gagal.');
  }}
}}

function continueAsComm() {{
  fetch('/activate-license', {{
    method:'POST', headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{ community_mode: true }})
  }}).finally(() => {{ location.href = '/'; }});
}}

// Copy node ID on click
document.getElementById('node-id').addEventListener('click', () => {{
  navigator.clipboard.writeText(document.getElementById('node-id').textContent)
    .then(() => {{ document.getElementById('node-id').textContent += ' ✓'; }});
}});
</script>
</body>
</html>
"""

# ── Custom HTTP Handler ────────────────────────────────────────────────────────
class ZQDesktopHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        # Suppress SimpleHTTPRequestHandler noise
        pass

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html, status=200):
        body = html.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        global LICENSE
        path = urlparse(self.path).path

        # Node ID endpoint (for app.js bootstrapDesktopLicense)
        if path == '/api/node-id':
            self._json({'node_id': NODE_ID, 'platform': platform.system(),
                        'hostname': platform.node()})
            return

        # License status endpoint
        if path == '/api/license-status':
            self._json(LICENSE)
            return

        # If license is invalid (not community mode) and user hasn't bypassed,
        # redirect to activation screen
        if path == '/' or path == '/index.html':
            if not LICENSE.get('valid') and LICENSE.get('mode') not in ('COMMUNITY',):
                self._render_activation()
                return

        # Serve static files normally
        return super().do_GET()

    def do_POST(self):
        global LICENSE
        path = urlparse(self.path).path

        if path == '/activate-license':
            length = int(self.headers.get('Content-Length', 0))
            try:
                body = json.loads(self.rfile.read(length))
            except Exception:
                self._json({'status': 'ERROR', 'message': 'Invalid JSON'}, 400)
                return

            # Community bypass
            if body.get('community_mode'):
                LICENSE = {
                    'valid': True, 'plan': 'COMMUNITY', 'mode': 'COMMUNITY',
                    'features': ['cbom_scanner', 'pqc_migration'],
                    'node_locked': False, 'message': 'Running in Community mode.'
                }
                self._json({'status': 'ACTIVATED', 'plan': 'COMMUNITY'})
                return

            # Real license activation
            lic_doc = body.get('license_json')
            if not lic_doc:
                self._json({'status': 'ERROR', 'message': 'license_json missing'}, 400)
                return

            # Save to license.lic
            try:
                LIC_FILE.write_text(json.dumps(lic_doc, indent=2, ensure_ascii=False), 'utf-8')
            except Exception as e:
                self._json({'status': 'ERROR', 'message': f'Could not write license.lic: {e}'}, 500)
                return

            # Re-validate
            result = validate_license()
            if result.get('valid'):
                LICENSE = result
                self._json({'status': 'ACTIVATED', **result})
            else:
                # Remove invalid file
                try: LIC_FILE.unlink()
                except: pass
                self._json({'status': 'INVALID', **result}, 403)
            return

        # Fallback
        self.send_response(404)
        self.end_headers()

    def _render_activation(self):
        lic = LICENSE
        mode = lic.get('mode', 'INVALID')

        # Color coding
        if mode == 'EXPIRED':
            bg, bdr, cls = '245,158,11,0.1', '245,158,11,0.3', 'warn'
        elif mode == 'NODE_LOCKED':
            bg, bdr, cls = '244,63,94,0.1', '244,63,94,0.3', 'err'
        elif mode == 'SIGNATURE_FAIL':
            bg, bdr, cls = '244,63,94,0.1', '244,63,94,0.3', 'err'
        else:
            bg, bdr, cls = '168,85,247,0.08', '168,85,247,0.2', 'warn'

        msg_html = lic.get('message', 'Lisensi tidak valid.').replace('\n', '<br>')
        html = ACTIVATION_HTML.format(
            node_id=NODE_ID,
            mode_class=cls,
            status_bg=bg,
            status_bdr=bdr,
            status_msg=f'<strong>{mode}:</strong> {msg_html}'
        )
        self._html(html)


# ── Entry Point ────────────────────────────────────────────────────────────────
def run_desktop():
    base_dir = str(BASE_DIR)
    os.chdir(base_dir)

    print("=" * 70)
    print("  ZENTYQUETRY SOVEREIGN DESKTOP EDITION  (OFFLINE & AIR-GAPPED)")
    print("  NIST Post-Quantum Cryptography & CBOM Management Engine")
    print("=" * 70)
    print(f"  [*] Server          : http://{HOST}:{PORT}")
    print(f"  [*] Hardware Node   : {NODE_ID}")
    print(f"  [*] License Status  : {LICENSE['mode']} — {LICENSE.get('plan','N/A')}")
    if LICENSE.get('mode') == 'ACTIVE':
        print(f"  [*] Plan Features   : {', '.join(LICENSE.get('features', []))}")
        print(f"  [*] Node Lock       : {'YES — ' + LICENSE.get('allowed_node','') if LICENSE.get('node_locked') else 'NO (any device)'}")
    print("=" * 70 + "\n")

    if not LICENSE.get('valid'):
        print(f"  [!] License issue: {LICENSE.get('message', '')}")
        print(f"  [!] Opening activation screen at http://{HOST}:{PORT}")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), ZQDesktopHandler) as httpd:
        print(f"[+] Serving on http://{HOST}:{PORT}  (Ctrl+C to quit)\n")
        try:
            webbrowser.open(f"http://{HOST}:{PORT}")
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] ZentyQuetry Desktop shutting down.")
            httpd.server_close()
            sys.exit(0)


if __name__ == "__main__":
    run_desktop()
