# -*- coding: utf-8 -*-
"""Command-line interface: doctor / bench / propose / probe / compose / optimize / recursive / train / serve / export."""
from __future__ import annotations

import argparse
import json

from .config import load_config
from .optimizer.ppc import PPC
from .optimizer.recursive import recursive_optimize, flat_optimize
from .training.trainer import SkillTrainer


def cmd_doctor(cfg):
    ppc = PPC(cfg)
    r = ppc.run(0.9)
    print("[doctor] success_rate=%.3f recall=%.3f violations=%d gain=%.3f" % (
        r["success_rate"], r["component_recall"], r["guardrail_violations"], r["contrastive_gain"]))
    print("[doctor] selected=%s" % ", ".join(r["selected"]))
    print("[doctor] OK")


def cmd_bench(cfg):
    ppc = PPC(cfg)
    skills = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    results = {}
    print("[bench] skill  success  recall  violations  gain")
    for s in skills:
        r = ppc.run(s)
        results[s] = r
        print("[bench] %.2f    %.3f   %.3f    %d          %.3f" % (
            s, r["success_rate"], r["component_recall"], r["guardrail_violations"], r["contrastive_gain"]))
    # two-level recursion at two skill anchors
    for s in (0.5, 1.0):
        rec = recursive_optimize(ppc, s)
        flat = flat_optimize(ppc, s)
        g = rec["success_rate"] - flat["success_rate"]
        print("[bench] recursion@%.2f: recursive=%.3f flat=%.3f gain=%.3f meta=%s" % (
            s, rec["success_rate"], flat["success_rate"], g, ",".join(rec["meta_selected"])))


def cmd_propose(cfg, args):
    from .propose.proposer import Proposer
    p = Proposer(cfg["optimizer"]["seed"])
    for cids in p.propose(args.n, size=args.size):
        print(" ".join(cids))


def cmd_probe(cfg, args):
    ppc = PPC(cfg)
    from .world.reward import success_rate
    from .propose.proposer import Proposer
    candidates = Proposer(cfg["optimizer"]["seed"]).propose(args.n, size=args.size)
    batch = ppc.oracle.make_batch(args.tasks)
    probed = ppc.prober.probe(candidates, batch)
    for i, (cids, traces) in enumerate(probed):
        print("[probe] cand%02d sr=%.3f | %s" % (i, success_rate(traces), " ".join(cids)))


def cmd_compose(cfg, args):
    from .compose.composer import Composer
    from .compose.contrastive import lift_stats
    from .world.universe import component_ids
    ppc = PPC(cfg)
    batch = ppc.oracle.make_batch(cfg["probe"]["n_tasks"])
    from .propose.proposer import Proposer
    candidates = Proposer(cfg["optimizer"]["seed"]).propose(6, size=6)
    probed = ppc.prober.probe(candidates, batch)
    all_traces = [tr for _, traces in probed for tr in traces]
    lifts = lift_stats(all_traces, component_ids())
    selected = Composer(args.skill).select(lifts, cfg["compose"]["top_k"])
    print("[compose] selected=%s" % ", ".join(selected))


def cmd_optimize(cfg, args):
    ppc = PPC(cfg)
    r = ppc.run(args.skill)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_recursive(cfg, args):
    ppc = PPC(cfg)
    rec = recursive_optimize(ppc, args.skill)
    flat = flat_optimize(ppc, args.skill)
    print("[recursive] recursive_sr=%.3f flat_sr=%.3f gain=%.3f" % (
        rec["success_rate"], flat["success_rate"], rec["success_rate"] - flat["success_rate"]))
    print("[recursive] meta_selected=%s" % ", ".join(rec["meta_selected"]))


def cmd_train(cfg, args):
    t = SkillTrainer(0.5, cfg["training"]["lr"])
    for i in range(args.epochs):
        t.train_step()
        print("[train] step %02d skill=%.4f" % (i + 1, t.skill))


def cmd_export(cfg, args):
    ppc = PPC(cfg)
    r = ppc.run(0.9)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print("[export] wrote %s" % args.out)


def cmd_serve(cfg, args):
    from .serving.app import serve
    serve(host=cfg["serving"]["host"], port=args.port or cfg["serving"]["port"], cfg=cfg)


def build_parser():
    ap = argparse.ArgumentParser(prog="reharness", description="recursive agent harness optimization")
    ap.add_argument("--recipe", default=None, help="yaml recipe to merge over defaults")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("doctor")
    sub.add_parser("bench")

    p = sub.add_parser("propose"); p.add_argument("--n", type=int, default=6); p.add_argument("--size", type=int, default=6)
    p = sub.add_parser("probe"); p.add_argument("--n", type=int, default=6); p.add_argument("--size", type=int, default=6); p.add_argument("--tasks", type=int, default=12)
    p = sub.add_parser("compose"); p.add_argument("--skill", type=float, default=0.8)
    p = sub.add_parser("optimize"); p.add_argument("--skill", type=float, default=0.9)
    p = sub.add_parser("recursive"); p.add_argument("--skill", type=float, default=0.9)
    p = sub.add_parser("train"); p.add_argument("--epochs", type=int, default=12)
    p = sub.add_parser("export"); p.add_argument("--out", default="reharness_result.json")
    p = sub.add_parser("serve"); p.add_argument("--port", type=int, default=None)
    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    cfg = load_config(args.recipe)
    if args.cmd is None:
        ap.print_help()
        return
    dispatch = {
        "doctor": lambda: cmd_doctor(cfg),
        "bench": lambda: cmd_bench(cfg),
        "propose": lambda: cmd_propose(cfg, args),
        "probe": lambda: cmd_probe(cfg, args),
        "compose": lambda: cmd_compose(cfg, args),
        "optimize": lambda: cmd_optimize(cfg, args),
        "recursive": lambda: cmd_recursive(cfg, args),
        "train": lambda: cmd_train(cfg, args),
        "export": lambda: cmd_export(cfg, args),
        "serve": lambda: cmd_serve(cfg, args),
    }
    dispatch[args.cmd]()


if __name__ == "__main__":
    main()
