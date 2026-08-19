#!/usr/bin/env python3
"""Phase 1: Minimal local server for ADTC Offline Coding Assistant.

Starts llama-server as a child process, serves app/ as static files,
and proxies chat requests with streaming SSE support.
"""

import argparse
import http.server
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
APP_DIR = WORKSPACE / "app"
DEFAULT_MODEL = WORKSPACE / "models" / "microsoft_Phi-4-mini-instruct-Q4_K_M.gguf"
LLAMA_SERVER = WORKSPACE / "bin" / "llama-server"
LLAMA_PORT = 8080

llama_proc = None


def llama_status():
    """Check if llama-server is reachable."""
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{LLAMA_PORT}/health")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read())
            return data.get("status", "unknown"), True
    except Exception:
        return "unreachable", False


class ADTCHandler(http.server.BaseHTTPRequestHandler):
    """Minimal HTTP handler for Phase 1."""

    def log_message(self, fmt, *args):
        # Concise logging
        sys.stderr.write(f"[serve] {args[0]}\n")

    def _json_response(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code, msg):
        self._json_response(code, {"error": msg})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"

        # API: status
        if path == "/api/status":
            status_text, running = llama_status()
            self._json_response(200, {
                "llama_server": running,
                "llama_status": status_text,
                "model": str(DEFAULT_MODEL.name),
                "model_path": str(DEFAULT_MODEL),
                "port": LLAMA_PORT,
            })
            return

        # Static files from app/
        if path == "/":
            path = "/index.html"

        # Security: reject path traversal
        if ".." in path:
            self._error(403, "path traversal rejected")
            return

        # Only allow files under app/
        file_path = APP_DIR / path.lstrip("/")
        if not file_path.resolve().is_relative_to(APP_DIR.resolve()):
            self._error(403, "access denied")
            return

        if not file_path.is_file():
            self._error(404, f"not found: {path}")
            return

        content_type = "text/html"
        if path.endswith(".js"):
            content_type = "application/javascript"
        elif path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".json"):
            content_type = "application/json"

        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = self.path.split("?")[0]

        if path != "/api/chat":
            self._error(404, "unknown endpoint")
            return

        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0 or content_len > 1024 * 1024:
            self._error(400, "invalid content length")
            return

        body = self.rfile.read(content_len)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._error(400, "invalid JSON")
            return

        messages = payload.get("messages")
        if not messages or not isinstance(messages, list):
            self._error(400, "messages array required")
            return

        # Validate no path traversal / injection in messages
        for msg in messages:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                self._error(400, "each message must have role and content")
                return

        stream = payload.get("stream", True)

        # Build request to llama-server
        llama_payload = json.dumps({
            "model": "local",
            "messages": messages,
            "stream": stream,
            "temperature": payload.get("temperature", 0.7),
            "max_tokens": payload.get("max_tokens", 512),
        }).encode()

        try:
            req = urllib.request.Request(
                f"http://127.0.0.1:{LLAMA_PORT}/v1/chat/completions",
                data=llama_payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            if stream:
                resp = urllib.request.urlopen(req, timeout=300)
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
            else:
                resp = urllib.request.urlopen(req, timeout=300)
                data = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode(errors="replace")
            self._json_response(e.code, {
                "error": f"llama-server error: {e.code}",
                "detail": err_body[:500],
            })
        except urllib.error.URLError as e:
            self._json_response(502, {
                "error": "llama-server unreachable",
                "detail": str(e.reason),
            })
        except Exception as e:
            self._json_response(500, {
                "error": "internal error",
                "detail": str(e),
            })


def start_llama_server(model_path, port=LLAMA_PORT, n_ctx=2048):
    """Start llama-server as a child process."""
    global llama_proc

    cmd = [
        str(LLAMA_SERVER),
        "--model", str(model_path),
        "--host", "127.0.0.1",
        "--port", str(port),
        "--ctx-size", str(n_ctx),
    ]

    print(f"[serve] Starting llama-server: {' '.join(cmd)}")
    try:
        llama_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print(f"[serve] ERROR: llama-server not found at {LLAMA_SERVER}")
        sys.exit(1)
    except PermissionError:
        print(f"[serve] ERROR: no permission to execute {LLAMA_SERVER}")
        sys.exit(1)

    # Wait for server to become ready (up to 120s for model loading)
    print("[serve] Waiting for llama-server to load model...")
    for i in range(240):
        if llama_proc.poll() is not None:
            stderr = llama_proc.stderr.read().decode(errors="replace")
            print(f"[serve] ERROR: llama-server exited with code {llama_proc.returncode}")
            print(f"[serve] stderr: {stderr[:2000]}")
            sys.exit(1)

        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/health")
            with urllib.request.urlopen(req, timeout=1) as resp:
                data = json.loads(resp.read())
                if data.get("status") in ("ok", "no slot available"):
                    print(f"[serve] llama-server ready ({i * 0.5:.1f}s)")
                    return
        except Exception:
            pass
        time.sleep(0.5)

    print("[serve] ERROR: llama-server did not become ready in 120s")
    llama_proc.kill()
    sys.exit(1)


def shutdown_llama_server():
    """Gracefully stop llama-server."""
    global llama_proc
    if llama_proc and llama_proc.poll() is None:
        print("[serve] Stopping llama-server...")
        llama_proc.terminate()
        try:
            llama_proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            llama_proc.kill()
            llama_proc.wait(timeout=5)
        print("[serve] llama-server stopped.")


def main():
    parser = argparse.ArgumentParser(description="ADTC Offline Coding Assistant - Phase 1 Server")
    parser.add_argument("--model", type=str, default=str(DEFAULT_MODEL),
                        help="Path to GGUF model file")
    parser.add_argument("--port", type=int, default=3000,
                        help="Port for the web server (default: 3000)")
    parser.add_argument("--n-ctx", type=int, default=2048,
                        help="Context size for llama-server (default: 2048)")
    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.is_file():
        print(f"[serve] ERROR: model not found: {model_path}")
        sys.exit(1)

    if not LLAMA_SERVER.is_file():
        print(f"[serve] ERROR: llama-server not found: {LLAMA_SERVER}")
        sys.exit(1)

    # Ensure app/ directory exists with at least index.html
    if not (APP_DIR / "index.html").is_file():
        print(f"[serve] WARNING: {APP_DIR}/index.html not found")

    start_llama_server(model_path, port=LLAMA_PORT, n_ctx=args.n_ctx)

    # Set up signal handlers for graceful shutdown
    def handle_signal(signum, frame):
        print(f"\n[serve] Received signal {signum}, shutting down...")
        shutdown_llama_server()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    server = http.server.HTTPServer(("0.0.0.0", args.port), ADTCHandler)
    print(f"[serve] Serving app/ on http://localhost:{args.port}")
    print(f"[serve] API: GET /api/status, POST /api/chat")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_llama_server()
        server.server_close()
        print("[serve] Server stopped.")


if __name__ == "__main__":
    main()
