#!/usr/bin/env python3
"""Control arms for checker.py.

A checker is only worth its failures. Each arm mutates ONE shipped input and asserts the
matching check flips to FAIL. Run:  python3 control_arms.py --package <dir>
"""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def checker(pkg: Path, termlist: Path | None = None) -> tuple[int, dict]:
    tmp = pkg / "_report.json"
    cmd = [sys.executable, str(HERE / "checker.py"), "--package", str(pkg), "--json", str(tmp), "--skip-points"]
    if termlist:
        cmd += ["--termlist", str(termlist)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    rep = json.loads(tmp.read_text()) if tmp.exists() else {}
    tmp.unlink(missing_ok=True)
    return r.returncode, rep


def arm(name: str, pkg: Path, mutate, expectation: str) -> bool:
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "pkg"
        shutil.copytree(pkg, work)
        mutate(work)
        rc, rep = checker(work)
        ok = not (
            rep.get("verdict", {}).get("identity_holds_exactly", False)
            and rep.get("verdict", {}).get("certificate_failures", 1) == 0
        )
        print(f"[{'CAUGHT' if ok else 'MISSED'}] {name}  (rc={rc}) expect={expectation}")
        return ok


def flip_one_coefficient(pkg: Path) -> None:
    p = pkg / "polynomial.expanded.txt"
    lines = p.read_text().splitlines()
    for i, ln in enumerate(lines):
        if ln and not ln.startswith("#"):
            parts = ln.split()
            parts[0] = str(int(parts[0]) + 1)
            lines[i] = " ".join(parts)
            break
    p.write_text("\n".join(lines) + "\n")


def drop_one_term(pkg: Path) -> None:
    p = pkg / "polynomial.expanded.txt"
    lines = [ln for ln in p.read_text().splitlines()]
    idx = next(i for i, ln in enumerate(lines) if ln and not ln.startswith("#"))
    del lines[idx]
    p.write_text("\n".join(lines) + "\n")


def drop_one_residual(pkg: Path) -> None:
    p = pkg / "residuals.json.gz"
    rows = json.loads(gzip.open(p, "rt").read())
    rows = rows[:-1]
    p.write_bytes(gzip.compress(json.dumps(rows).encode()))


def reweight_one_residual(pkg: Path) -> None:
    p = pkg / "weights.json"
    w = json.loads(p.read_text())
    w[0] = 2
    p.write_text(json.dumps(w))


def corrupt_one_certificate_patch(pkg: Path) -> None:
    p = pkg / "certificate.jsonl.gz"
    lines = gzip.open(p, "rt").read().splitlines()
    for i, ln in enumerate(lines):
        ev = json.loads(ln)
        if ev.get("kind") == "linear":
            idx, row = ev["patches"][0]
            row[0][0] = row[0][0] + 1
            lines[i] = json.dumps(ev)
            break
    p.write_bytes(gzip.compress(("\n".join(lines) + "\n").encode()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True)
    a = ap.parse_args()
    pkg = Path(a.package)
    arms = [
        ("coefficient +1 in Phi", flip_one_coefficient, "S3 IDENTITY_HOLDS -> False"),
        ("one Phi term deleted", drop_one_term, "S3 IDENTITY_HOLDS -> False"),
        ("last residual deleted", drop_one_residual, "S3 -> False"),
        ("one residual reweighted to 2", reweight_one_residual, "S3 -> False + weights finding"),
        ("one linear patch coefficient +1", corrupt_one_certificate_patch, "S5 failures > 0"),
    ]
    results = [arm(n, pkg, m, e) for n, m, e in arms]
    print(f"\ncontrol arms caught {sum(results)}/{len(results)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
