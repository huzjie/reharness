# -*- coding: utf-8 -*-
"""HTTP client example (stdlib urllib)."""
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

import json
import urllib.request


def post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


if __name__ == "__main__":
    # Start the server first: python -m reharness serve --port 8790
    try:
        health = json.loads(urllib.request.urlopen("http://127.0.0.1:8790/health", timeout=5).read())
        print("health:", health)
        out = post("http://127.0.0.1:8790/v1/optimize", {"skill": 0.9})
        r = out["result"]
        print("success=%.3f recall=%.3f" % (r["success_rate"], r["component_recall"]))
    except Exception as e:
        print("server not reachable (start it with: python -m reharness serve):", e)
