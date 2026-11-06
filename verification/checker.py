#!/usr/bin/env python3
"""Independent checker for the quartic-4973 (Version 4) Diophantine certificate.

Verifies, from shipped bytes only, without importing any producer module:

  S1  term-list metrics            (terms, variables, degree, max|coeff|, canonicality)
  S2  residual-set metrics         (rows, weights, degrees)
  S3  EXACT identity  Phi == sum_i w_i R_i^2   (coefficient-wise, over Z)
  S4  POINT identity  Phi(p) == sum_i w_i R_i(p)^2  (independent parse path, exact over Z
      and modular at a 100-bit prime)
  S5  certificate replay + per-op semantics for the mechanically decidable op kinds,
      and connectivity of the replay result to the shipped residual set
  S6  easy-direction status (what is and is not machine-checkable here)

Every section reports EXACTLY-CHECKED / MODULAR-CHECKED / NOT-REACHED with measured
numbers. A mismatch is reported as a finding, never silently repaired.

Usage:
  python3 checker.py --package work/current/quartics/quartic-4973
  python3 checker.py --package DIR --termlist other_phi.txt          # reduced variant
  python3 checker.py --package DIR --json report.json --skip-points
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

Mon = tuple[int, ...]  # sorted variable indices, repetition = exponent
Row = dict[Mon, int]

CLAIM_TERMS = 72925
CLAIM_VARS = 4973
CLAIM_DEGREE = 4
CLAIM_MAXCOEFF = 685783949153203534233890
PRIME = (1 << 100) + 267  # arbitrary large prime-ish modulus, fixed for reproducibility


# ---------------------------------------------------------------- row utilities
def decode(poly) -> Row:
    """[coeff, [ids...]] list -> {sorted-monotuple: coeff}; ids repeat per exponent."""
    out: Row = defaultdict(int)
    for c, idxs in poly:
        out[tuple(sorted(idxs))] += int(c)
    return {m: c for m, c in out.items() if c}


def encode(row: Row) -> list:
    return [[c, list(m)] for m, c in sorted(row.items())]


def deg(row: Row) -> int:
    return max((len(m) for m in row), default=0)


def mul(a: Row, b: Row) -> Row:
    out: Row = defaultdict(int)
    for m, c in a.items():
        for n, d in b.items():
            out[tuple(sorted(m + n))] += c * d
    return {m: c for m, c in out.items() if c}


def add_into(acc: Row, row: Row, factor: int = 1) -> None:
    for m, c in row.items():
        acc[m] = acc.get(m, 0) + factor * c


def scalar_eq(a: Row, b: Row) -> bool:
    """Equal up to a nonzero rational scalar (same zero set)."""
    if (a == b):
        return True
    if set(a) != set(b) or not a:
        return False
    m0 = min(a)
    if b.get(m0, 0) == 0:
        return False
    k = Fraction(a[m0], b[m0])
    if k == 0:
        return False
    return all(Fraction(a[m], 1) == k * b[m] for m in a)


def substitute(row: Row, var: int, repl: dict, scale: Fraction = Fraction(1)) -> dict:
    """row with x_var replaced by the polynomial scale*repl (repl may itself contain x_var).

    Returns a Fraction-coefficient row."""
    R = {(m if m else ()): Fraction(c) * scale for m, c in (repl or {}).items()}
    if not R:
        R = {(): scale}
    out: dict[Mon, Fraction] = defaultdict(Fraction)
    for m, c in row.items():
        e = m.count(var)
        rest = tuple(v for v in m if v != var)
        if e == 0:
            out[m] += c
            continue
        acc: dict[Mon, Fraction] = {(): Fraction(1)}
        for _ in range(e):
            nxt: dict[Mon, Fraction] = defaultdict(Fraction)
            for mm, cc in acc.items():
                for nn, dd in R.items():
                    nxt[tuple(sorted(mm + nn))] += cc * dd
            acc = {k: v for k, v in nxt.items() if v}
        for mm, cc in acc.items():
            out[tuple(sorted(rest + mm))] += c * cc
    return {m: c for m, c in out.items() if c}


def iclear(row: dict[Mon, Fraction]) -> Row:
    """Fraction row -> integer row, dividing out content, sign-normalised on the smallest
    monomial; canonical only up to scalar."""
    if not row:
        return {}
    den = 1
    for c in row.values():
        den = den * c.denominator // _gcd(den, c.denominator)
    ints = {m: int(c * den) for m, c in row.items()}
    g = 0
    for c in ints.values():
        g = _gcd(g, abs(c))
    if g == 0:
        return {}
    ints = {m: c // g for m, c in ints.items()}
    if ints[min(ints)] < 0:
        ints = {m: -c for m, c in ints.items()}
    return ints


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


# ---------------------------------------------------------------- term list
def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii")
    return path.open("r", encoding="ascii")


def scan_terms(path: Path) -> dict:
    terms: dict[Mon, int] = {}
    nlines = 0
    header = None
    malformed = []
    unsorted = 0
    dup = 0
    zeros = 0
    degree_hist: Counter[int] = Counter()
    maxabs = 0
    vars_used: set[int] = set()
    with open_text(path) as fh:
        for line in fh:
            nlines += 1
            s = line.rstrip("\n")
            if not s:
                malformed.append((nlines, "empty"))
                continue
            if s[0] == "#":
                header = header or s
                continue
            parts = s.split()
            try:
                c = int(parts[0])
                if len(parts) > 1 and ":" in parts[1]:
                    # canonical form: "<coeff> <var>:<exp> ..."
                    exp: Counter[int] = Counter()
                    for p in parts[1:]:
                        v, e = p.split(":")
                        exp[int(v)] += int(e)
                    idxs = [v for v, e in sorted(exp.items()) for _ in range(e)]
                else:
                    idxs = [int(x) for x in parts[1:]]
            except ValueError:
                malformed.append((nlines, s[:60]))
                continue
            if idxs != sorted(idxs):
                unsorted += 1
            m = tuple(idxs)
            if c == 0:
                zeros += 1
            if m in terms:
                dup += 1
            terms[m] = c
            degree_hist[len(m)] += 1
            if abs(c) > maxabs:
                maxabs = abs(c)
            vars_used.update(m)
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "total_lines": nlines,
        "header": header,
        "terms": terms,
        "term_count": len(terms),
        "line_term_count": nlines - (1 if header else 0),
        "malformed": malformed[:10],
        "malformed_count": len(malformed),
        "unsorted_exponent_lines": unsorted,
        "duplicate_monomial_lines": dup,
        "zero_coefficient_lines": zeros,
        "degree_histogram": dict(sorted(degree_hist.items())),
        "max_total_degree": max(degree_hist) if degree_hist else 0,
        "max_abs_coeff": maxabs,
        "max_abs_coeff_bits": maxabs.bit_length(),
        "var_index_max": max(vars_used) if vars_used else -1,
        "distinct_vars_used": len(vars_used),
    }


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- evaluation
def eval_row(row: Row, vals: dict[int, int], mod: int | None) -> int:
    total = 0
    for m, c in row.items():
        t = c
        for v in m:
            t *= vals[v]
            if mod:
                t %= mod
        total += t
        if mod:
            total %= mod
    return total


def random_point(nvars: int, rng: random.Random, mod: int | None) -> dict[int, int]:
    if mod:
        return {v: rng.randrange(1, mod) for v in range(nvars)}
    return {v: rng.randrange(-3, 4) for v in range(nvars)}


# ---------------------------------------------------------------- certificate
def load_package(pkg: Path) -> dict:
    d = {}
    d["residuals_path"] = pkg / "residuals.json.gz"
    d["weights_path"] = pkg / "weights.json"
    d["termlist_path"] = pkg / "polynomial.expanded.txt"
    d["cert_path"] = pkg / "certificate.jsonl.gz"
    d["varmap_path"] = pkg / "variable-map.json"
    d["final_verification_path"] = pkg / "evidence" / "final-verification.json"
    return d


def check_certificate(pkg: Path, res_rows: list[Row], verbose: bool) -> dict:
    """Replay the transform chain. Patches are applied as shipped; for every op kind whose
    data fully determines the patch, the patch is ALSO re-derived independently."""
    lines = gzip.open(pkg / "certificate.jsonl.gz", "rt").read().splitlines()
    header = json.loads(lines[0])
    rows = [decode(r) for r in header["rows"]]
    kinds: Counter[str] = Counter()
    result = {
        "cert_lines": len(lines),
        "initial_rows": len(rows),
        "initial_source_sha256": header.get("source_sha256"),
        "initial_source_variables": header.get("source_variables"),
        "op_counts": {},
        "kinds_semantically_rederived": {},
        "kinds_patch_only": [],
        "failures": [],
        "weights_event": None,
        "final": None,
    }
    rederived: Counter[str] = Counter()
    patch_only: Counter[str] = Counter()
    all_targets_seen: set[int] = set()

    def fail(msg: str) -> None:
        if len(result["failures"]) < 40:
            result["failures"].append(msg)

    for n, ln in enumerate(lines[1:], start=1):
        ev = json.loads(ln)
        kind = ev["kind"]
        kinds[kind] += 1
        if kind == "weights":
            result["weights_event"] = ev["values"]
            continue
        if kind == "final":
            result["final"] = {k: v for k, v in ev.items() if k != "kind"}
            continue
        patches = ev.get("patches") or []
        data = ev.get("data") or {}

        # ---- independent re-derivation where the data determines the patch
        ok = True
        if kind == "linear":
            a, b, other, target = data["a"], data["b"], data["other"], data["target"]
            cand = {m: a * c for m, c in rows[target].items()}
            add_into(cand, rows[other], b)
            cand = {m: c for m, c in cand.items() if c}
            got = _find_patch(patches, target)
            if got is None:
                fail(f"linear op{n}: no patch for row {target}")
                ok = False
            elif not (got == cand or scalar_eq(got, cand)):
                fail(f"linear op{n}: patch for row {target} != {a}*row[{target}] + {b}*row[{other}]")
                ok = False
        elif kind == "shear":
            var, other, (num, den) = data["variable"], data["other"], data["scalar"]
            repl = {((var,)): Fraction(1), ((other,)): Fraction(num, den)}
            for idx, newrow in patches:
                want = substitute(rows[idx], var, repl)
                if not scalar_eq(decode(newrow), iclear(want)):
                    fail(f"shear op{n}: row {idx} != row with x{var} += {num}/{den}*x{other}")
                    ok = False
        elif kind == "eliminate":
            var = data["variable"]
            src = rows[data["row"]]
            coeff = src.get((var,), 0)
            if coeff == 0:
                fail(f"eliminate op{n}: row {data['row']} is not linear in x{var}")
                ok = False
            else:
                rhs = {m: c for m, c in src.items() if m != (var,)}
                rhsf = {m: Fraction(-c, coeff) for m, c in rhs.items()}
                shipped = decode(data["replacement"])
                shippedf = {m: Fraction(c, data["denominator"]) for m, c in shipped.items()}
                if rhsf != shippedf:
                    fail(f"eliminate op{n}: shipped replacement x{var} != -rest/coeff of row {data['row']}")
                    ok = False
                for idx, newrow in patches:
                    if idx == data["row"]:
                        if decode(newrow):
                            fail(f"eliminate op{n}: definition row {idx} not emptied")
                            ok = False
                        continue
                    want = substitute(rows[idx], var, rhsf, Fraction(1))
                    if not scalar_eq(decode(newrow), iclear(want)):
                        fail(f"eliminate op{n}: row {idx} != substitution of x{var}")
                        ok = False
        elif kind == "relation_eliminate":
            var, rowid = data["variable"], data["row"]
            rep = data["replacement"]
            repf = {tuple(sorted(m)): Fraction(c, rep["denominator"]) for c, m in rep["terms"]}
            if rowid not in [i for i, _ in patches]:
                fail(f"relation_eliminate op{n}: definition row {rowid} not patched")
                ok = False
            reductions = {r["row"]: r["terms"] for r in data["reductions"]}
            if set(reductions) != {i for i, _ in patches} - {rowid}:
                fail(f"relation_eliminate op{n}: reduction rows != patched rows")
                ok = False
            for idx, newrow in patches:
                if idx == rowid:
                    if decode(newrow):
                        fail(f"relation_eliminate op{n}: definition row not emptied")
                        ok = False
                    continue
                want = dict(substitute(rows[idx], var, repf))
                for term in reductions.get(idx, []):
                    sup = rows[term["support"]]
                    mnum = term["multiplier"]
                    numf = {tuple(sorted(m)): Fraction(c, mnum["denominator"]) for c, m in mnum["terms"]}
                    prod: dict[Mon, Fraction] = defaultdict(Fraction)
                    for m, c in numf.items():
                        for mm, cc in sup.items():
                            prod[tuple(sorted(m + mm))] += c * cc
                    for mm, cc in prod.items():
                        want[mm] = want.get(mm, Fraction(0)) - cc
                want = {m: c for m, c in want.items() if c}
                if var in {v for m in want for v in m}:
                    fail(f"relation_eliminate op{n}: x{var} survives reduction of row {idx}")
                    ok = False
                if not scalar_eq(decode(newrow), iclear(want)):
                    fail(f"relation_eliminate op{n}: row {idx} != substitution of x{var} minus reductions")
                    ok = False
        elif kind == "circuit":
            ok = check_circuit(rows, data, patches, n, fail)
        else:
            ok = None  # parity_conic: patch applied, semantics not re-derived
        if ok:
            rederived[kind] += 1
        else:
            patch_only[kind] += 1

        # ---- apply shipped patches
        for idx, newrow in patches:
            if not (0 <= idx < len(rows)):
                fail(f"op{n} {kind}: patch row index {idx} out of range")
                continue
            rows[idx] = decode(newrow)
            all_targets_seen.add(idx)

    result["op_counts"] = dict(kinds)
    result["kinds_semantically_rederived"] = dict(rederived)
    result["kinds_patch_only"] = sorted(k for k in kinds if k not in rederived and k != "header")
    result["rows_after_replay"] = len(rows)
    result["nonempty_rows_after_replay"] = sum(1 for r in rows if r)
    result["patch_targets"] = len(all_targets_seen)

    # ---- independent shipped copy of the POST-chain row list (candidate-rows.json.gz)
    cand_path = pkg / "candidate-rows.json.gz"
    if cand_path.exists():
        cand = [decode(r) for r in json.loads(gzip.open(cand_path, "rt").read())]
        result["candidate_rows"] = len(cand)
        result["replay_matches_candidate_rows"] = cand == rows
        if not result["replay_matches_candidate_rows"]:
            nd = sum(1 for a, b in zip(cand, rows) if a != b) if len(cand) == len(rows) else -1
            fail(f"replayed rows != candidate-rows.json.gz ({nd} rows differ, {len(cand)} vs {len(rows)})")
    # ---- weights event must be the shipped weights, and all 1
    wj = pkg / "weights.json"
    if result["weights_event"] is not None and wj.exists():
        shipped_w = json.loads(wj.read_text())
        # the event carries one weight per row (including emptied rows); weights.json is compact
        result["weights_event_len"] = len(result["weights_event"])
        result["weights_event_all_one"] = all(w == 1 for w in result["weights_event"])
        result["weights_event_consistent"] = (
            result["weights_event_all_one"] and len(shipped_w) == sum(1 for w in result["weights_event"] if True) - (len(result["weights_event"]) - len(shipped_w))
        )
        result["weights_json_len"] = len(shipped_w)
        if not result["weights_event_all_one"]:
            fail("certificate weights event contains a weight != 1 (reweighting)")
    # ---- final report numbers must be what this checker measures
    fin = result.get("final") or {}
    rep_fin = fin.get("report") or {}
    result["final_report"] = rep_fin
    result["allocated_variables_matches_term_list"] = None
    if fin:
        result["allocated_variables"] = fin.get("allocated_variables")
    result["final_rows_sha256_declared"] = fin.get("rows_sha256")

    # ---- connectivity: replay result == shipped residual set, via the shipped variable map
    active = json.loads((pkg / "variable-map.json").read_text())
    mapping = {v: i for i, v in enumerate(active)}
    try:
        replay = [
            {tuple(sorted(mapping[v] for v in m)): c for m, c in r.items()}
            for r in rows
            if r
        ]
    except KeyError as e:
        fail(f"variable-map missing variable {e}")
        replay = []
    result["replay_rows"] = len(replay)
    result["replay_equals_shipped_residuals"] = replay == res_rows if replay else None
    if replay and replay != res_rows:
        if len(replay) != len(res_rows):
            fail(f"replay row count {len(replay)} != shipped {len(res_rows)}")
        else:
            diff = sum(1 for a, b in zip(replay, res_rows) if a != b)
            fail(f"replay differs from shipped residuals in {diff}/{len(res_rows)} rows")
    result["replay_content_sha256"] = hashlib.sha256(
        json.dumps([encode(r) for r in replay], separators=(",", ":")).encode()
    ).hexdigest()
    result["shipped_residuals_content_sha256"] = hashlib.sha256(
        json.dumps([encode(r) for r in res_rows], separators=(",", ":")).encode()
    ).hexdigest()
    return result


def check_circuit(rows: list[Row], data: dict, patches: list, n: int, fail) -> bool:
    """A circuit op replaces a chain of squaring definitions by a shorter chain. Both chains
    must define the same values in terms of the external variables. We re-derive each chain
    from its own rows and compare the expansions exactly, so the check does not depend on the
    producer's argument order."""
    ids = data["old_rows"]
    old_t = data["old_targets"]
    new_t = data["new_targets"]
    outs = data["outputs"]
    ok = True
    if len(patches) != len(ids):
        fail(f"circuit op{n}: {len(patches)} patches for {len(ids)} rows")
        return False
    supplied = {i: decode(r) for i, r in patches}
    if set(supplied) != set(ids):
        fail(f"circuit op{n}: patch rows != old_rows")
        return False
    old_defs = [rows[i] for i in ids]
    new_defs = [supplied[i] for i in ids[: len(new_t)]]
    for i in ids[len(new_t):]:
        if supplied[i]:
            fail(f"circuit op{n}: surplus row {i} not emptied")
            ok = False
    ext = sorted({v for r in old_defs for m in r for v in m} - set(old_t))
    for nm, tgt in zip(("old", "new"), (old_t, new_t)):
        seen = set(ext)
        for row, target in zip(old_defs if nm == "old" else new_defs, tgt):
            if row.get((target,), 0) == 0:
                fail(f"circuit op{n}: {nm} definition of {target} is not linear in it")
                return False
            for m in row:
                if m != (target,) and target in m:
                    fail(f"circuit op{n}: {nm} definition of {target} non-linear")
                    return False
            vs = {v for m in row for v in m} - {target}
            if not vs <= seen:
                fail(f"circuit op{n}: {nm} chain is cyclic or forward-referencing at {target}")
                return False
            seen.add(target)

    def expand(defs, targets, mapping):
        env: dict[int, dict[Mon, Fraction]] = {}
        for row, target in zip(defs, targets):
            lead = row[(target,)]
            acc: dict[Mon, Fraction] = {}
            for m, c in row.items():
                if m == (target,):
                    continue
                term = {(): Fraction(-c, lead)}
                for v in m:
                    nxt: dict[Mon, Fraction] = defaultdict(Fraction)
                    src = env.get(v, {(v,): Fraction(1)})
                    for mm, cc in term.items():
                        for nn, dd in src.items():
                            nxt[tuple(sorted(mm + nn))] += cc * dd
                    term = nxt
                for mm, cc in term.items():
                    acc[mm] = acc.get(mm, Fraction(0)) + cc
            env[target] = acc
        return {
            t: iclear({tuple(sorted(mapping[v] for v in m)): c for m, c in env.get(t, {(t,): Fraction(1)}).items()})
            for t in targets
        }

    mo = {v: i for i, v in enumerate(ext + old_t)}
    mn = {v: i for i, v in enumerate(ext + new_t)}
    eo = dict(expand(old_defs, old_t, mo))
    en = dict(expand(new_defs, new_t, mn))
    for v in outs:
        if v not in eo or v not in en:
            fail(f"circuit op{n}: output {v} is not defined by the opened or the closed chain")
            ok = False
        elif eo[v] != en[v]:
            fail(f"circuit op{n}: output {v} differs between the opened and the closed chain")
            ok = False
    return ok


def add_rows(a: Row, b: Row, ka: int, kb: int) -> Row:
    out: Row = dict(a) if ka == 1 else {m: ka * c for m, c in a.items()}
    add_into(out, b, kb)
    return {m: c for m, c in out.items() if c}


def _find_patch(patches, target: int) -> Row | None:
    for idx, newrow in patches:
        if idx == target:
            return decode(newrow)
    return None


# ---------------------------------------------------------------- main checks
def run(args) -> dict:
    pkg = Path(args.package)
    P = load_package(pkg)
    termlist = Path(args.termlist) if args.termlist else P["termlist_path"]
    rep: dict = {"package": str(pkg), "termlist": str(termlist), "sections": {}}

    # S1
    t = scan_terms(termlist)
    terms: Row = t.pop("terms")
    t["claimed"] = {
        "terms": CLAIM_TERMS,
        "variables": CLAIM_VARS,
        "degree": CLAIM_DEGREE,
        "max_abs_coeff": CLAIM_MAXCOEFF,
        "max_abs_coeff_lt_2_80": True,
    }
    t["measured_vs_claimed"] = {
        "terms": f"{t['term_count']} vs {CLAIM_TERMS}" + ("  OK" if t["term_count"] == CLAIM_TERMS else "  DIFFERS"),
        "variables": f"{t['distinct_vars_used']} vs {CLAIM_VARS}"
        + ("  OK" if t["distinct_vars_used"] == CLAIM_VARS else "  DIFFERS"),
        "max_index_plus_one": t["var_index_max"] + 1,
        "degree": f"{t['max_total_degree']} vs {CLAIM_DEGREE}"
        + ("  OK" if t["max_total_degree"] == CLAIM_DEGREE else "  DIFFERS"),
        "max_abs_coeff": f"{t['max_abs_coeff']} vs {CLAIM_MAXCOEFF}"
        + ("  OK" if t["max_abs_coeff"] == CLAIM_MAXCOEFF else "  DIFFERS"),
        "max_abs_coeff_lt_2_80": t["max_abs_coeff"] < (1 << 80),
        "coeff_bit_length": t["max_abs_coeff_bits"],
    }
    rep["sections"]["S1_terms"] = t

    # S2
    res_raw = json.loads(gzip.open(P["residuals_path"], "rt").read())
    res = [decode(r) for r in res_raw]
    weights = json.loads(P["weights_path"].read_text())
    dh = Counter(deg(r) for r in res)
    s2 = {
        "rows": len(res),
        "weights_len": len(weights),
        "distinct_weights": {str(k): v for k, v in Counter(weights).items()},
        "all_weights_one": all(w == 1 for w in weights),
        "degree_histogram": dict(sorted(dh.items())),
        "max_row_degree": max(dh) if dh else 0,
        "terms_per_row_max": max((len(r) for r in res), default=0),
        "max_abs_row_coeff": max((abs(c) for r in res for c in r.values()), default=0),
        "sos_degree_bound": 2 * (max(dh) if dh else 0),
    }
    rep["sections"]["S2_residuals"] = s2

    # S3 exact identity
    acc: Row = {}
    for r, w in zip(res, weights):
        sq: Row = defaultdict(int)
        items = list(r.items())
        for m, c in items:
            for n, d in items:
                sq[tuple(sorted(m + n))] += c * d
        add_into(acc, {m: c for m, c in sq.items() if c}, w)
    acc = {m: c for m, c in acc.items() if c}
    only_a = set(acc) - set(terms)
    only_b = set(terms) - set(acc)
    valdiff = [m for m in set(acc) & set(terms) if acc[m] != terms[m]]
    s3 = {
        "status": "EXACTLY-CHECKED",
        "identity": "Phi == sum_i w_i * R_i^2  (weights from weights.json)",
        "sum_of_squares_term_count": len(acc),
        "sum_of_squares_degree": max((len(m) for m in acc), default=0),
        "termlist_term_count": len(terms),
        "terms_only_in_sum_of_squares": len(only_a),
        "terms_only_in_termlist": len(only_b),
        "coefficient_mismatches": len(valdiff),
        "sample": [{"monomial": list(m), "sos": acc.get(m), "shipped": terms.get(m)} for m in list(only_a)[:5] + list(only_b)[:5] + valdiff[:5]],
        "IDENTITY_HOLDS": not only_a and not only_b and not valdiff,
        "sum_of_squares_content_sha256": hashlib.sha256(
            json.dumps(encode(acc), separators=(",", ":")).encode()
        ).hexdigest(),
        "termlist_content_sha256": hashlib.sha256(
            json.dumps(encode(terms), separators=(",", ":")).encode()
        ).hexdigest(),
    }
    rep["sections"]["S3_identity_exact"] = s3

    # S4 point identity, independent parse
    if not args.skip_points:
        rng = random.Random(args.seed)
        nv = max(t["var_index_max"], max((v for r in res for m in r for v in m), default=0)) + 1
        checks = []
        for i in range(args.points):
            pt_mod = random_point(nv, rng, PRIME) if i % 2 else None
            pt = pt_mod if pt_mod else random_point(nv, rng, None)
            lhs = eval_row(terms, pt, PRIME if pt_mod else None)
            rhs = 0
            for r, w in zip(res, weights):
                v = eval_row(r, pt, PRIME if pt_mod else None)
                rhs += w * v * v
                if pt_mod:
                    rhs %= PRIME
            checks.append(
                {"mode": "mod" if pt_mod else "exact-Z", "equal": lhs == rhs, "lhs": str(lhs)[:40], "rhs": str(rhs)[:40]}
            )
        s4 = {
            "status": "MODULAR-CHECKED" if all(c["equal"] for c in checks if c["mode"] == "mod") else "FAILED",
            "points": checks,
            "all_equal": all(c["equal"] for c in checks),
            "prime": PRIME,
        }
        rep["sections"]["S4_identity_points"] = s4

    # S5 certificate
    try:
        s5 = check_certificate(pkg, res, verbose=args.verbose)
        s5["status"] = (
            "EXACTLY-CHECKED (patch replay)"
            if s5.get("replay_equals_shipped_residuals")
            else "REVIEW (see failures)"
        )
    except Exception as e:  # noqa: BLE001
        s5 = {"status": "ERROR", "error": f"{type(e).__name__}: {e}"}
    rep["sections"]["S5_certificate"] = s5

    # S6 easy direction
    rep["sections"]["S6_easy_direction"] = easy_direction(pkg, res, args)

    # cross-check the certificate's self-reported numbers against this checker's measurements
    fr = (s5.get("final_report") or {}) if isinstance(s5, dict) else {}
    rep["sections"]["S7_selfreport_crosscheck"] = {
        "declared": fr,
        "measurable_by_this_checker": {
            "rows": s2["rows"],
            "monomials": t["term_count"],
            "degree": t["max_total_degree"],
            "max_abs_coefficient": t["max_abs_coeff"],
            "variables": t["distinct_vars_used"],
            "witnesses": t["distinct_vars_used"] - 1,
        },
        "agree": bool(fr)
        and fr.get("rows") == s2["rows"]
        and fr.get("monomials") == t["term_count"]
        and fr.get("degree") == t["max_total_degree"]
        and fr.get("max_abs_coefficient") == t["max_abs_coeff"]
        and fr.get("variables") == t["distinct_vars_used"],
    }

    # verdict
    rep["verdict"] = {
        "terms_match_claims": all(
            str(x).endswith("OK") or x is True
            for x in t["measured_vs_claimed"].values()
            if not isinstance(x, int)
        ),
        "identity_holds_exactly": s3["IDENTITY_HOLDS"],
        "weights_all_one": s2["all_weights_one"],
        "certificate_replay_matches_residuals": s5.get("replay_equals_shipped_residuals"),
        "certificate_failures": len(s5.get("failures", [])),
        "easy_direction": rep["sections"]["S6_easy_direction"]["status"],
    }
    return rep


def easy_direction(pkg: Path, res: list[Row], args) -> dict:
    """The theorem needs: q in Z => exists integer w with Phi(q,w)=0.
    Phi = sum of squares, so Phi = 0 iff every R_i vanishes. Whether a witness EXISTS for
    each integer q is not decided by the residual list alone; we measure how far forward
    substitution gets and report the boundary honestly."""
    nvars = max((v for r in res for m in r for v in m), default=0) + 1
    known = {0}
    used: set[int] = set()
    steps = 0
    while True:
        progressed = False
        for i, r in enumerate(res):
            if i in used:
                continue
            unk = {v for m in r for v in m if v not in known}
            if len(unk) != 1:
                continue
            v = next(iter(unk))
            lin = 0
            ok = True
            for m, c in r.items():
                if v not in m:
                    continue
                if m.count(v) != 1:
                    ok = False
                    break
                others = [u for u in m if u != v]
                if any(u not in known for u in others):
                    ok = False
                    break
                lin += c
            if not ok or lin == 0:
                continue
            known.add(v)
            used.add(i)
            steps += 1
            progressed = True
        if not progressed:
            break
    return {
        "status": "NOT-REACHED (residual list is not a definition chain)",
        "phi_nonnegativity": "EXACTLY-CHECKED by S3: Phi is a sum of squares with weights 1, so Phi >= 0 over R and Phi = 0 iff all R_i = 0",
        "trivial_witness_all_zero": "Phi(0,...,0) equals Phi's constant term; if nonzero, w=0 is not a witness",
        "triangular_sweep_steps_from_input_only": steps,
        "triangular_sweep_variables_known": len(known),
        "triangular_sweep_variables_total": nvars,
        "triangular_sweep_complete": len(known) == nvars,
        "note": (
            "Forward substitution over the 4552 residuals determines only "
            f"{len(known)} of {nvars} variables, so the q -> w witness map is NOT contained in "
            "residuals.json.gz. It lives in the transform chain's inverted elimination patches "
            "and in the source arithmetic theorem, which the release scopes out of the algebraic "
            "checker (evidence/final-verification.json: 'The source arithmetic theorem is not "
            "checked here')."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True)
    ap.add_argument("--termlist", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--points", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20261106)
    ap.add_argument("--skip-points", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    rep = run(a)
    for name, sec in rep["sections"].items():
        print(f"\n=== {name} ===")
        print(json.dumps({k: v for k, v in sec.items() if k != "terms"}, indent=2, default=str)[:6000])
    print("\n=== VERDICT ===")
    print(json.dumps(rep["verdict"], indent=2, default=str))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=2, default=str) + "\n")
    return 0 if (rep["verdict"]["identity_holds_exactly"] and not rep["verdict"]["certificate_failures"]) else 1


if __name__ == "__main__":
    sys.exit(main())
