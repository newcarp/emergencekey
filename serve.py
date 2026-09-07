#!/usr/bin/env python3
"""Serve EmergenceKey over HTTPS (self-signed).
HTTP cert-install port is mainly for iPhone/iPad profile download.

Copy .env.example → .env and set HOST (and optional EXTRA_SANS).
"""
from __future__ import annotations

import http.server
import ipaddress
import os
import ssl
import subprocess
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT_DIR = ROOT / ".certs"
CERT = CERT_DIR / "cert.pem"
KEY = CERT_DIR / "key.pem"
SANS_STAMP = CERT_DIR / "sans.txt"


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def host_san(host: str) -> str:
    return f"IP:{host}" if is_ip(host) else f"DNS:{host}"


def build_sans(host: str, extra: str) -> list[str]:
    sans = [host_san(host), "IP:127.0.0.1", "DNS:localhost"]
    for part in extra.split(","):
        item = part.strip()
        if not item:
            continue
        if ":" not in item:
            item = host_san(item)
        if item not in sans:
            sans.append(item)
    return sans


def ensure_cert(sans: list[str]) -> None:
    stamp = ",".join(sans)
    if CERT.exists() and KEY.exists() and SANS_STAMP.exists():
        if SANS_STAMP.read_text(encoding="utf-8").strip() == stamp:
            return
    CERT_DIR.mkdir(exist_ok=True)
    subprocess.check_call(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-sha256",
            "-days", "365", "-nodes",
            "-keyout", str(KEY), "-out", str(CERT),
            "-subj", "/CN=EmergenceKey",
            "-addext", "subjectAltName=" + stamp,
        ]
    )
    SANS_STAMP.write_text(stamp + "\n", encoding="utf-8")


class AppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("[https] " + (fmt % args))

    def translate_path(self, path):
        p = super().translate_path(path)
        parts = Path(p).parts
        if ".certs" in parts or Path(p).name in {"key.pem", "serve.py", ".env"}:
            return str(ROOT / ".__nope__")
        return p


def make_install_handler(host: str, https_port: int):
    class InstallHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print("[http]  " + (fmt % args))

        def do_GET(self):
            if self.path.split("?", 1)[0] in {"/emergencekey.cer", "/emergencekey.crt", "/cert.pem"}:
                data = CERT.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/x-x509-ca-cert")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            html = f"""<!DOCTYPE html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EmergenceKey cert</title>
<body style="font:16px sans-serif;background:#0b0d10;color:#e8edf5;padding:24px;line-height:1.45">
<h1 style="color:#3dffa8">Then open HTTPS</h1>
<p>iPhone / iPad: tap <a href="/emergencekey.cer" style="color:#6cb6ff">emergencekey.cer</a> → Settings → Profile Downloaded → Install.
Then Settings → General → About → <b>Certificate Trust Settings</b> → enable EmergenceKey.</p>
<p>Android / desktop: skip the cert and open HTTPS below; continue past the warning. The .cer is optional if you want it trusted.</p>
<p>After that open:</p>
<p><a href="https://{host}:{https_port}/" style="color:#3dffa8">https://{host}:{https_port}/</a></p>
</body>"""
            data = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return InstallHandler


def main() -> None:
    env = load_env(ROOT / ".env")
    host = env.get("HOST", "127.0.0.1").strip() or "127.0.0.1"
    https_port = int(env.get("HTTPS_PORT", "8000"))
    http_port = int(env.get("HTTP_PORT", "8080"))
    extra = env.get("EXTRA_SANS", "")
    sans = build_sans(host, extra)

    os.chdir(ROOT)
    ensure_cert(sans)
    httpd = http.server.ThreadingHTTPServer(
        ("0.0.0.0", http_port), make_install_handler(host, https_port)
    )
    httpsd = http.server.ThreadingHTTPServer(("0.0.0.0", https_port), AppHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(str(CERT), str(KEY))
    httpsd.socket = ctx.wrap_socket(httpsd.socket, server_side=True)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"HTTPS  https://{host}:{https_port}/")
    print(f"cert   http://{host}:{http_port}/emergencekey.cer")
    if not (ROOT / ".env").is_file():
        print("tip    copy .env.example → .env and set HOST to your LAN IP")
    httpsd.serve_forever()


if __name__ == "__main__":
    main()
