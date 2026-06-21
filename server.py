#!/usr/bin/env python3
"""
Mini-servidor local do Bet Coffe.

Faz duas coisas:
  1) Serve os arquivos HTML desta pasta  (http://localhost:8000/)
  2) Proxy da API-Football para evitar bloqueio de CORS:
        GET /api/<rota>  ->  https://v3.football.api-sports.io/<rota>
     injetando o header x-apisports-key.

Uso:
    python server.py            # porta 8000
    python server.py 8080       # outra porta

Depois abra no navegador:
    http://localhost:8000/            (painel)
    http://localhost:8000/analise.html

A chave da API-Football é resolvida nesta ordem:
    1) header  x-apisports-key  enviado pela página (salvo no localStorage), ou
    2) variável de ambiente  APISPORTS_KEY, ou
    3) arquivo  apikey.txt  nesta pasta (uma linha com a chave).

Sem dependências externas — só a biblioteca padrão do Python 3.
"""
import os
import sys
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit

UPSTREAM = "https://v3.football.api-sports.io"
HERE = os.path.dirname(os.path.abspath(__file__))


def load_key_from_file():
    try:
        with open(os.path.join(HERE, "apikey.txt"), "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    # ---------- CORS em todas as respostas ----------
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "x-apisports-key, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    def end_headers(self):
        self._cors()
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.proxy()
        return super().do_GET()

    # ---------- helpers ----------
    def _send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def resolve_key(self):
        k = self.headers.get("x-apisports-key")
        if k and k.strip():
            return k.strip()
        k = os.environ.get("APISPORTS_KEY", "")
        if k.strip():
            return k.strip()
        return load_key_from_file()

    # ---------- proxy da API-Football ----------
    def proxy(self):
        key = self.resolve_key()
        if not key:
            return self._send_json(400, {"errors": {
                "key": "Chave da API ausente. Informe na pagina, ou use APISPORTS_KEY / apikey.txt."
            }})

        rest = self.path[len("/api/"):]          # ex.: teams?search=Palmeiras
        parts = urlsplit(rest)
        url = UPSTREAM + "/" + parts.path
        if parts.query:
            url += "?" + parts.query

        req = Request(url, headers={"x-apisports-key": key, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=20) as r:
                data = r.read()
                self.send_response(r.getcode())
                self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except HTTPError as e:                    # repassa erro da API (401, 429, etc.)
            data = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", e.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except URLError as e:
            self._send_json(502, {"errors": {"upstream": "Falha ao contatar a API-Football: %s" % e.reason}})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Porta invalida: %r" % sys.argv[1])
            sys.exit(1)

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("=" * 52)
    print(" Bet Coffe  ->  http://localhost:%d/" % port)
    print("   painel:   http://localhost:%d/index.html" % port)
    print("   analise:  http://localhost:%d/analise.html" % port)
    print("   proxy:    /api/...  ->  %s/..." % UPSTREAM)
    print("   (Ctrl+C para parar)")
    print("=" * 52)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nparando...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
