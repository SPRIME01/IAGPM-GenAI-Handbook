import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from fastapi.testclient import TestClient


class MockVLLMHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length).decode("utf-8")
        try:
            j = json.loads(body or "{}")
        except Exception:
            j = {}

        # Simple echo response with expected fields
        resp = {
            "content": f"echo: {j.get('prompt', '')}",
            "model": j.get("model", "mock-model"),
            "usage": {"prompt_tokens": 1},
        }
        data = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run_mock_server(server):
    server.serve_forever()


def test_proxy_forwards_to_mock_vllm(monkeypatch, tmp_path):
    # Start mock vLLM
    server = HTTPServer(("localhost", 0), MockVLLMHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=run_mock_server, args=(server,), daemon=True)
    thread.start()

    try:
        # Point adapter to the mock server
        monkeypatch.setenv("PAC_UPSTREAM_URL", f"http://localhost:{port}")

        # Ensure the app imports from the correct src path
        repo_root = Path(__file__).resolve().parents[3]
        src_dir = str(repo_root / "services" / "policy-gateway" / "src")
        import sys

        sys.path.insert(0, src_dir)
        import app as gateway_app  # type: ignore

        client = TestClient(gateway_app.app)

        resp = client.post(
            "/proxy/completion", json={"prompt": "hello", "model": "mock-model"}
        )
        assert resp.status_code == 200
        j = resp.json()
        assert "echo: hello" in j.get("content", "")
        assert j.get("model") == "mock-model"
    finally:
        server.shutdown()
        server.server_close()
