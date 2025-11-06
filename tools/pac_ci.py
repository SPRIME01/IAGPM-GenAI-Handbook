#!/usr/bin/env python3
import argparse, json, yaml, sys


def load_cfg(path):
    if path.endswith(".yaml") or path.endswith(".yml"):
        return yaml.safe_load(open(path))
    return json.load(open(path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--eval", required=True)
    ap.add_argument("--fairness", required=True)
    ap.add_argument("--safety", required=True)
    ap.add_argument("--drift", required=True)
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    q = json.load(open(args.eval))["pass_at_5"]
    f = json.load(open(args.fairness))["subgroup_delta"]
    s = json.load(open(args.safety))["harmful_rate"]
    d = json.load(open(args.drift))["psi"]

    qt = cfg["thresholds"]["quality"]["pass_at_5"]["target"]
    ft = cfg["thresholds"]["fairness"]["subgroup_delta"]["target_max"]
    st = cfg["thresholds"]["safety"]["harmful_rate"]["target_max"]

    violations = []
    if q < qt:
        violations.append(f"quality.pass_at_5 {q} < target {qt}")
    if f > ft:
        violations.append(f"fairness.subgroup_delta {f} > max {ft}")
    if s > st:
        violations.append(f"safety.harmful_rate {s} > max {st}")

    print(json.dumps({"violations": violations}, indent=2))
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
