"""Stream-parse the shipped polynomial.expanded.txt term list; report measurements only."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LINE_RE = re.compile(r"^(-?\d+)((?: \d+)*)$")


def scan(path: Path) -> dict:
    nlines = 0
    header = None
    terms = 0
    bad = []
    max_var = -1
    min_var = None
    max_deg = 0
    deg_hist: dict[int, int] = {}
    max_abs_coeff = 0
    max_abs_coeff_line = None
    zero_coeff = 0
    dup_monomials = 0
    seen: dict[tuple[int, ...], int] = {}
    sum_abs = 0
    coeff_hist: dict[int, int] = {}
    const_term = None
    var_use: dict[int, int] = {}

    with path.open("r", encoding="ascii") as fh:
        for raw in fh:
            nlines += 1
            s = raw.rstrip("\n")
            if not s:
                bad.append((nlines, "empty"))
                continue
            if s.startswith("#"):
                if header is None:
                    header = s
                continue
            m = LINE_RE.match(s)
            if not m:
                bad.append((nlines, s[:80]))
                continue
            coeff = int(m.group(1))
            idxs = tuple(int(x) for x in m.group(2).split()) if m.group(2) else ()
            terms += 1
            # repeated indices == exponents; they must be sorted ascending (canonical form)
            if idxs:
                if list(idxs) != sorted(idxs):
                    bad.append((nlines, "unsorted-exponents"))
                lo, hi = idxs[0], idxs[-1]
                min_var = lo if min_var is None else min(min_var, lo)
                max_var = max(max_var, hi)
                for v in set(idxs):
                    var_use[v] = var_use.get(v, 0) + 1
            else:
                const_term = coeff
            d = len(idxs)
            max_deg = max(max_deg, d)
            deg_hist[d] = deg_hist.get(d, 0) + 1
            if coeff == 0:
                zero_coeff += 1
            coeff_hist[d] = coeff_hist.get(d, 0) + 1
            a = abs(coeff)
            sum_abs += a
            if a > max_abs_coeff:
                max_abs_coeff, max_abs_coeff_line = a, nlines
            if idxs in seen:
                dup_monomials += 1
            else:
                seen[idxs] = coeff

    return {
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size_bytes": path.stat().st_size,
        "total_lines": nlines,
        "header": header,
        "terms": terms,
        "malformed_lines": bad[:20],
        "malformed_count": len(bad),
        "var_index_min": min_var,
        "var_index_max": max_var,
        "distinct_vars_used": len(var_use),
        "implied_variable_count": (max_var + 1) if max_var >= 0 else 0,
        "max_total_degree": max_deg,
        "degree_histogram": {str(k): v for k, v in sorted(deg_hist.items())},
        "max_abs_coeff": max_abs_coeff,
        "max_abs_coeff_lineno": max_abs_coeff_line,
        "max_abs_coeff_bits": max_abs_coeff.bit_length(),
        "two_pow_80": 2**80,
        "max_abs_coeff_lt_2_80": max_abs_coeff < 2**80,
        "sum_abs_coeff": sum_abs,
        "zero_coefficients": zero_coeff,
        "duplicate_monomials": dup_monomials,
        "constant_term": const_term,
        "unused_var_indices": [v for v in range(0, (max_var + 1)) if v not in var_use],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out")
    a = ap.parse_args()
    r = scan(Path(a.path))
    txt = json.dumps(r, indent=2)
    if a.out:
        Path(a.out).write_text(txt + "\n")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
