#!/usr/bin/env python3
"""Produce the canonical term list for a Phi term file shipped in the release form.

Input form (as shipped in polynomial.expanded.txt):
    # comment header
    <coeff> <var-index repeated once per exponent> ...
e.g.  -2 0 0 57   means  -2 * x0^2 * x57      (variable 0 is the rational input)

Output form (canonical, deterministic):
    <coeff> <var>:<exp> ...     terms sorted by the sparse monomial key
e.g.  -2 0:2 57:1
Sparse exponents keep the file 3x smaller than the repeated-index form; the sort key is the
full exponent vector compared lexicographically by (variable, exponent) pairs, so the order is
stable across runs and machines.

  python3 make_canonical.py IN.txt OUT.txt.gz
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from collections import Counter
from pathlib import Path

CANON_HEADER = (
    "# canonical Phi term list: '<coeff> <var>:<exp> ...' sorted by sparse monomial key;"
    " variable 0 is the rational input"
)


def parse(path: Path) -> dict[tuple[tuple[int, int], ...], int]:
    terms: dict[tuple[tuple[int, int], ...], int] = {}
    with path.open("r", encoding="ascii") as fh:
        for n, line in enumerate(fh, 1):
            s = line.rstrip("\n")
            if not s or s[0] == "#":
                continue
            parts = s.split()
            c = int(parts[0])
            exps = Counter(int(x) for x in parts[1:])
            key = tuple(sorted(exps.items()))
            if key in terms:
                raise SystemExit(f"{path}:{n}: duplicate monomial {key}")
            if c == 0:
                raise SystemExit(f"{path}:{n}: zero coefficient")
            terms[key] = c
    return terms


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    terms = parse(src)
    body = "\n".join(
        " ".join([str(c)] + [f"{v}:{e}" for v, e in key]) for key, c in sorted(terms.items())
    )
    payload = (CANON_HEADER + "\n" + body + "\n").encode("ascii")
    with gzip.GzipFile(dst, "wb", mtime=0) as fh:  # mtime=0 -> reproducible bytes
        fh.write(payload)
    print(
        f"terms={len(terms)} bytes_plain={len(payload)} bytes_gz={dst.stat().st_size} "
        f"sha256_plain={hashlib.sha256(payload).hexdigest()} "
        f"sha256_gz={hashlib.sha256(dst.read_bytes()).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
