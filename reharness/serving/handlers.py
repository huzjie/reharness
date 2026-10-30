# -*- coding: utf-8 -*-
"""HTTP request handler (stdlib http.server)."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from .models import info, ok
from ..optimizer.ppc import PPC
from ..optimizer.recursive import recursive_optimize, flat_optimize


class Handler(BaseHTTPRequestHandler):
    ppc = None

    def log_message(self, *args):
        pass

    def _send(self, code: int, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if n <= 0:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, ok())
        if self.path == "/v1/info":
            return self._send(200, info())
        self._send(404, {"error": "not found"})

    def do_POST(self):
        body = self._read_json()
        ppc = Handler.ppc or PPC()
        Handler.ppc = ppc
        if self.path == "/v1/optimize":
            r = ppc.run(
                skill=float(body.get("skill", 0.9)),
                top_k=body.get("top_k"),
                scoring=body.get("scoring", "lift"),
                probe_size=int(body.get("probe_size", 8)),
                n_candidates=body.get("n_candidates"),
                n_tasks=body.get("n_tasks"),
            )
            return self._send(200, ok(result=r))
        if self.path == "/v1/recursive":
            rec = recursive_optimize(ppc, float(body.get("skill", 0.9)))
            flat = flat_optimize(ppc, float(body.get("skill", 0.9)))
            return self._send(200, ok(
                recursive=rec["success_rate"], flat=flat["success_rate"],
                gain=rec["success_rate"] - flat["success_rate"],
                meta_selected=rec["meta_selected"]))
        self._send(404, {"error": "not found"})
