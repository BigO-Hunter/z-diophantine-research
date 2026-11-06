# INVENTORY — quartic-4973-version-4 (and handoff r3)

Acquired 2026-11-06 from `github.com/elliotglazer/diophantine-z-q` with `gh release download`
(authenticated as `darkhipo`). Every downloaded asset was checked against the release's own
`SHA256SUMS`; both ZIP checksums matched.

## What was acquired

| asset | bytes | sha256 | status |
|---|---|---|---|
| `z-in-q-version4-current-handoff.zip` (release `quartic-4973-version-4`) | 31,895,055 | `b5a4ed9e0b4e58ad53c0410f3976259b696892a4883557aab5ab05e567b00086` | checksum OK |
| `z-in-q-version4-current-handoff.zip` (release `research-handoff-2026-11-06-r3`) | 34,908,844 | `ecbbfc6b18a23ae3cdee64287a18bf863996bc8bff98486b40b2f0842a6ebcc9` | checksum OK |
| `quartic_4973.tex` | 719,455 | `2cb539bdd7039eef9a8fe489ee3b153bfa2d0e74c26006b8da3c617aa815c32b` | checksum OK |
| `SHA256SUMS` (v4) / `SHA256SUMS` (r3) | 367 / 201 | — | both bind the two ZIPs + tex |
| `BUILD_RECEIPT.json` (v4, r3) | 1,900 | — | package identity record |
| `handoff-plan.json` (v4, r3) | 539,537 / 553,933 | — | payload/plan manifest |

**GAP**: `z-in-q-version4-full-handoff.zip` (371,756,101 B v4 / 374,769,889 B r3) was **not**
downloaded. It is documented as the current-only archive **plus** the unchanged November 4
revision-2 baseline and selected history. The current-only archive contains the complete quartic
package, the manuscript snapshot, `current/lean/` and `current/docs/`, so nothing the checker uses
is missing; the full archive adds history only.

**GAP**: `quartic_4973.pdf` (1,164,209 B) not downloaded — the `.tex` source is authoritative and
the release ships both.

**GAP**: the producer's own reproducer (`reproducibility/run.py`) was **not** run. It is
deliberately Linux-only and refuses to start elsewhere:
`reproducibility/run.py:74  need(sys.platform.startswith('linux'),'Linux process controls
required')`, plus `/proc/meminfo` and `prctl(PR_SET_PDEATHSIG)` in `child_setup()`. This host is
macOS, so the generator cannot execute here. Consequence: this lane verifies the two independent
representations the release ships (the 72,925-term list and Σ R_i²) against each other, and does
not regenerate either from `source/`.

## ZIP contents (v4 current-only)

1,385 files, 81,861,645 B uncompressed, under `current/` and `history/`:

| area | files | what it is |
|---|---|---|
| `current/quartics/` | 537 | three quartic packages: `quartic-4973/`, `quartic-9625/`, `quartic-12504/` (earlier versions kept for comparison) |
| `current/docs/` | 382 | manuscript sources and notes |
| `current/handoff/` | 170 | handoff records |
| `history/version4/` | 93 | intermediate build history |
| `current/lean/` | 60 | Lean-side files (not used by this lane) |
| `current/construction/` | 28 | the JS/Python compiler that emits the ordinary-integer polynomial (largest files: `ordinary-integer-definition.json` 23.2 MB, `precision-natural-polynomial.json` 17.9 MB) |
| top-level | — | `START_HERE.md`, `CURRENT_STATE.json`, `COVERAGE.md`, `RESEARCH_NOTES.md`, `MANIFEST.json`, `SHA256SUMS` |

## What FORM the polynomial ships in

**A plain ASCII sparse term list — not Sage, not Magma, not a bare generator script.**
`current/quartics/quartic-4973/polynomial.expanded.txt` (1,622,053 B, sha256 `094f6a7e…`):

```
# coefficient followed by repeated variable indices; input is variable 0
1900333570565983            <- constant term
4 0 0                       <- 4*x0^2
-2 0 0 57                   <- -2*x0^2*x57
```

One line per monomial: the coefficient, then each variable index repeated once per exponent, in
ascending order. Variable 0 is the rational input. This is a fully machine-readable artifact as
shipped — no generator needs to be run — and the list is **not** sorted by monomial (it is in
generator order), which is why this lane produces a canonical re-encoding.

The generator also ships, so the release is reproducible in both directions:

| file | role |
|---|---|
| `residuals.json.gz` | the 4,552 residual polynomials `R_i` (`[[coeff,[indices…]],…]` per row) |
| `weights.json` | 4,552 weights, all `1` |
| `certificate.jsonl.gz` | the 554-line transform certificate (551 ops + `weights` + `final`) |
| `candidate-rows.json.gz` | 4,879 candidate rows (the chain's starting set) |
| `variable-map.json` | 4,973-entry ordered map: allocated variable → active column |
| `verify_certificate.py` | the producer's own checker (74 KB, stdlib only) |
| `evidence/final-verification.json` | the producer's PASS record and declared counts |
| `reproducibility/` | pipeline, base tools, and a `cleanup/` package that regenerates this quartic |
| `source/` | the pinned source system (4,513 rows, 4,935 vars) + compiler + 22 contract/proof files |

The construction is **quartic = (Σ over residual rows) of squared quadratics**: the certificate
starts from 4,879 candidate rows, applies 551 transforms, empties 327 rows, and the surviving
4,552 rows are `R_i`; Φ = Σ R_i² expands to the 72,925-term list.

## r3 vs v4

`research-handoff-2026-11-06-r3` re-ships the same quartic. Measured by sha256 over the extracted
bytes, `polynomial.expanded.txt`, `residuals.json.gz` and `certificate.jsonl.gz` are
**identical** in both archives, so every number in `CHECKER_REPORT.md` applies to both releases.
r3 adds collaborator notes under `current/research/` and an updated run manifest; it does not
change the polynomial, the residual set, or the certificate.
