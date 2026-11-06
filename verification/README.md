# dzq-artifact — machine-readable substrate + independent checker for quartic-4973

Lane B1 of board `z-diophantine-in-q`. Goal: make the Version-4 construction verifiable **outside
anyone's Lean and outside the producer's own checker**.

Result in one line: Φ = Σ R_i² was re-derived and matches the shipped 72,925-term polynomial
**coefficient-exactly**; all four headline counts measure as claimed; 550 of the 551 certificate
transforms were re-derived from their own parameters with **0 failures**; the q ↦ w easy direction
is **NOT-REACHED** — it is the source arithmetic theorem, which the release scopes out.

## Re-run everything

```bash
cd ~/bigo-campaign/dzq-artifact

# 1. acquire (needs gh auth; downloads into dl/, gitignored)
gh release download research-handoff-2026-11-06-r3 -R elliotglazer/diophantine-z-q \
   -p 'z-in-q-version4-current-handoff.zip' -O dl/r3-current.zip
shasum -a 256 dl/r3-current.zip   # expect ecbbfc6b18a23ae3cdee64287a18bf863996bc8bff98486b40b2f0842a6ebcc9
mkdir -p work && unzip -q -o dl/r3-current.zip -d work 'current/quartics/quartic-4973/*'

# 2. check (stdlib only, ~2 s)
python3 checker.py --package work/current/quartics/quartic-4973 --json work/report.json

# 3. prove the checker can fail
python3 control_arms.py --package work/current/quartics/quartic-4973

# 4. rebuild the canonical artifact
python3 make_canonical.py work/current/quartics/quartic-4973/polynomial.expanded.txt \
        artifacts/phi-4973.canonical.txt.gz

# 5. re-check any variant term list against the same residual set
python3 checker.py --package work/current/quartics/quartic-4973 \
        --termlist artifacts/phi-4973.canonical.txt.gz
```

`checker.py` exit code is 0 only when the identity holds exactly, the claims measure as claimed,
and the certificate replay produces no failures.

## Files

| file | what it is |
|---|---|
| `INVENTORY.md` | what the release ships, in what form, with hashes; two declared GAPs |
| `CHECKER_REPORT.md` | measured-vs-claimed ledger, per-section verdicts, control arms |
| `checker.py` | the independent checker (sections S1–S7; no producer imports) |
| `control_arms.py` | mutation arms proving the checker fails when it should |
| `make_canonical.py` | shipped term list → deterministic canonical term list |
| `inventory.py` | ZIP + package inventory with sha256 (`work/inventory_v4.json`) |
| `terms_scan.py` | standalone term-list measurement |
| `artifacts/phi-4973.canonical.txt.gz` | the artifact: 72,925 terms, sorted, 334,290 B |
| `dl/`, `work/` | downloads and extracted package — **gitignored**, re-acquire with the commands above |

## The artifact format

```
# canonical Phi term list: '<coeff> <var>:<exp> ...' sorted by sparse monomial key; variable 0 is the rational input
1900333570565983
4 0:2
-2 0:2 57:1
```

Sorted by the sparse `(var, exp)` key, sparse exponents (3× smaller than the shipped
repeated-index form), `gzip mtime=0` so the bytes are reproducible. sha256 (plain)
`7296204974548c1feb83315fd2ca2e91410acfe6e56fd070e9ae1b2361113580`, (gz)
`d9a5126709ef9a4c7ece84c26fa83fa4855ed64d46ab063b77ac18fdf675f075`. The shipped
`polynomial.expanded.txt` is deliberately gitignored-by-`work/`; it is one download away, and its
hash is pinned in `INVENTORY.md` and inside `CHECKER_REPORT.md`.

## Not done here (scope)

- The arithmetic theorem (why a witness exists for every integer q) — `dzq-anatomy` and the
  paper's arithmetic argument own that; this lane records that the artifact cannot decide it.
- The `parity_conic` transform's bespoke justification rule (1 of 551 ops) — its patch is applied
  and its consequences are covered by S3, but its derivation is not re-checked.
- Lean, and the `full-handoff` ZIP's history payloads (see GAPs in `INVENTORY.md`).
- Regenerating the polynomial from `source/`: the release's `reproducibility/run.py` is Linux-only
  by construction (`need(sys.platform.startswith('linux'),'Linux process controls required')`), so
  it refuses to run on this macOS host. Verification here is between the two representations the
  release already ships, which is the algebraic content the reproducer would reproduce.
