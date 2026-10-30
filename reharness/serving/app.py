# -*- coding: utf-8 -*-
"""Run the stdlib HTTP server (blocking)."""
from __future__ import annotations

from http.server import ThreadingHTTPServer

from .handlers import Handler
from ..optimizer.ppc import PPC


def serve(host: str = "127.0.0.1", port: int = 8790, cfg: dict | None = None):
    Handler.ppc = PPC(cfg)
    srv = ThreadingHTTPServer((host, port), Handler)
    print("[serve] reharness listening on http://%s:%d" % (host, port), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
