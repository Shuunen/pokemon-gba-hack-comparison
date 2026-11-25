"""Serveur de dev avec live reload.
- sert le dossier dist/ sur http://localhost:8085/
- injecte un petit script dans les pages HTML qui recharge l'onglet quand un fichier de dist/ change
- reconstruit dist/index.html (build_site.py) quand data/hacks.db, site_template.html, data/shots.json
  ou build_site.py changent
Lancer:  python3 serve.py [port]
"""
import json
import os
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "dist")
DATA = os.path.join(ROOT, "data")
WATCH_SRC = ["data/hacks.db", "site_template.html", "data/shots.json", "build_site.py"]
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8085

SNIPPET = b"""<script>
(()=>{let v=null;const tick=async()=>{try{const r=await fetch('/__version',{cache:'no-store'});const j=await r.json();
if(v!==null&&j.v!==v){location.reload();return}v=j.v}catch(e){}setTimeout(tick,700)};tick()})();
</script>"""

state = {"v": 0.0}


def site_mtime():
    m = 0.0
    for base, _, files in os.walk(SITE):
        for f in files:
            m = max(m, os.path.getmtime(os.path.join(base, f)))
    return m


def src_mtime():
    return max((os.path.getmtime(os.path.join(ROOT, f)) for f in WATCH_SRC if os.path.exists(os.path.join(ROOT, f))), default=0)


def watcher():
    last_src = src_mtime()
    reload_id = 0   # n'augmente que pour les modifications externes (édition de la base, du template…)
    while True:
        time.sleep(0.4)
        try:
            cur = src_mtime()
            if cur != last_src:
                time.sleep(0.3)  # laisse finir l'écriture
                last_src = src_mtime()
                r = subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, capture_output=True, text=True)
                print("[rebuild]", "ok" if r.returncode == 0 else "ERREUR\n" + r.stderr[-400:], flush=True)
                reload_id += 1
            state["v"] = reload_id
        except Exception as e:  # ne jamais tuer le watcher
            print("[watcher]", e, flush=True)


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/__version":
            body = json.dumps({"v": state["v"]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path in ("/", "/index.html"):
            with open(os.path.join(SITE, "index.html"), "rb") as f:
                html = f.read()
            html = html.replace(b"</body>", SNIPPET + b"</body>", 1)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return
        super().do_GET()

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    threading.Thread(target=watcher, daemon=True).start()
    print(f"http://localhost:{PORT}/  (live reload actif)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
