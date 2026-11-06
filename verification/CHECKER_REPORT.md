# CHECKER REPORT — quartic-4973 (Version 4)

Independent checker: `checker.py` (stdlib only, ~700 lines, imports no producer module).
Provenance note: the *mathematics* is re-implemented here, but the *interpretation* of each
transform event's `data` fields was decoded from the shipped `verify_certificate.py` (the release's
own published spec for its certificate format) — matching a specified serialization is not the
same as trusting the producer's verdict, and every number below is recomputed from bytes.
Inputs: the shipped bytes listed in `INVENTORY.md`. Reproduce with `python3 checker.py
--package work/current/quartics/quartic-4973 --json out.json`; control arms with
`python3 control_arms.py --package …`.

Verdict vocabulary: **EXACTLY-CHECKED** = coefficient-wise/bit-exact over Z on the shipped bytes;
**MODULAR-CHECKED** = exact at sampled points over Z and at a 100-bit modulus;
**NOT-REACHED** = needs the source arithmetic theorem, which the release itself scopes out.

## Ledger: measured vs claimed

| claim (release notes, `quartic_4973.tex` line 51, `final-verification.json`) | measured | |
|---|---|---|
| 72,925 nonzero monomials | 72,925 (72,925 term lines, 0 duplicates, 0 zero coefficients, 0 malformed) | **OK** |
| 4,973 total variables | 4,973 distinct variables; max index 4,972; **every** index 0…4,972 used | **OK** |
| degree 4 | max total degree 4 (histogram: 1 const, 513 linear, 6,364 quadratic, 12,789 cubic, 53,258 quartic) | **OK** |
| max abs coefficient 685,783,949,153,203,534,233,890, below 2^80 | exactly that value, bit length **80** (so ≥ 2^79), 2^80 = 1,208,925,819,614,629,174,706,176 → strictly below | **OK** |
| 4,552 residuals / 4,972 witnesses | 4,552 rows; 4,973 − 1 input = 4,972 witnesses | **OK** |
| weights all 1 | 4,552 shipped weights all `1`; certificate's 4,879-row weights event all `1` | **OK** |
| summed residual degree ≤ 2 | 10 rows linear, 4,542 rows quadratic; max 17 terms in a row; max \|row coeff\| 828,120,733,440 (40 bits) | **OK** |
| Φ = Σ R_i² | see S3 | **EXACTLY-CHECKED** |

Φ's own derived figures (not separately claimed in the release): constant term 19,003,335,705,659,83 → `1900333570565983`; Σ\|coeff\| = 1,196,383,549,147,270,363,936,472.

## S1/S2 — terms and residuals — EXACTLY-CHECKED

`polynomial.expanded.txt` sha256 `094f6a7ed17e7cc8d5d17a2f809127bbaffd0fe343cb2a32d18ac97e61279876`
(1,622,053 B, 72,926 lines = 1 header + 72,925 terms), matching the hash declared in
`evidence/final-verification.json` (`expanded_sha256`) — the shipped list has not been touched
since the producer recorded it. `certificate.jsonl.gz` sha256
`81ca768459a13b76dbdf4bfe81e94fbab9ab99f14a5731f6b1a1b03e28c1df2b` also matches the declared
`certificate_sha256`.

## S3 — the collapse identity — **EXACTLY-CHECKED, holds**

Expanded Σ_i w_i·(Σ_m c_im x^m)² independently into a coefficient dictionary and compared it to
the shipped term list, coefficient by coefficient over Z:

- Σ R_i² gives 72,925 monomials, degree 4; shipped list has 72,925 monomials, degree 4
- terms only in Σ R_i²: **0**; terms only in the shipped list: **0**; coefficient mismatches: **0**
- canonical-content sha256 is identical on both sides: `7a29c524bf81f44476b5acb514eeda7c3808b89ee6dcf835e3a2cc9ce496292a`

So Φ **is** exactly the sum of squares of the 4,552 shipped residuals. Consequently Φ ≥ 0 over R
and Φ = 0 ⟺ every R_i = 0. **No reweighting smuggles anything**: every weight is 1, so the
identity is literally Φ = Σ R_i².

## S4 — identity at random points — MODULAR-CHECKED

Two independent evaluation paths (the term list as written, and the residual list squared),
6 random points: 3 over Z with no modulus (values ~10^25, exact integer equality) and 3 at the
prime 1,267,650,600,228,229,401,496,703,205,643 (100 bits). All 6 **agree**.

## S5 — the 551-transform certificate — **EXACTLY-CHECKED for 550 of 551 ops, 0 failures**

The certificate is fully self-describing: line 0 is the `initial` state (4,879 candidate rows
inline + gates + reuse rules), then 551 ops each carrying `data` (parameters) **and** `patches`
(the affected rows' new content), then `weights` and `final`.

This checker **re-derives each patch from `data` plus the pre-op row state**, not merely applies
it. Op kinds re-derived exactly: `linear` 266/266 (`row_target ← a·row_target + b·row_other`),
`eliminate` 121/121 (the shipped rational `replacement` equals `−rest/coeff` of the definition row
exactly, and every affected row equals the substitution), `relation_eliminate` 148/148
(substitution of the declared variable **minus** the declared multiplier×support-row reductions),
`shear` 2/2 (`x_v ← x_v + (num/den)·x_other`), `circuit` 13/13 (both the opened and the closed
squaring chain are expanded to polynomials in the external variables and must define the same
values at every declared output).

**Not semantically re-derived (1 op): `parity_conic`** — its justification is a bespoke
rational-map rule embedded in the producer's checker (`verify_certificate.py` exec's an own
checker for it). Its patch is still applied and its output still flows into every check above, so
a wrong patch would surface in S3; only the step's own justification is unverified. `weights` and
`final` are records, not transforms.

Chain connectivity, all measured:

- 554 lines = `initial` + 551 transforms + `weights` + `final` ✔ (matches the producer's
  `operations` tally: 266+148+121+13+2+1 = 551)
- applying the patches in order to the 4,879 initial rows reproduces the shipped
  `candidate-rows.json.gz` **exactly** (4,879 rows, 327 emptied)
- compacting those rows through `variable-map.json` reproduces the shipped `residuals.json.gz`
  **exactly** (4,552 rows); replay content sha256 `45c5287d3e727980a2c34dea2798939f33e822934892c59136388a0c7e179939`
- the `final` record's declared report (4,552 rows / 72,925 monomials / degree 4 / max coefficient
  / 4,973 variables / 4,972 witnesses) equals this checker's own measurements
- peak allocation 5,365 variables → 4,973 active columns after compaction (392 allocated
  coordinates vanish)

**Boundary of this S5 claim, stated precisely:** each op is verified *locally* (its patch is
exactly what its declared operation produces from the pre-op rows), and the repaired chain is shown
to terminate in the shipped residual set. The *global* statement the release makes — that the
composition is an exact projection-preserving equivalence onto the input coordinate, in both
directions — is implied by these op kinds all being invertible rational substitutions, but this
checker does not mechanize that composition argument. Local correctness of 550 steps plus exact
row-level connectivity is what is measured here.

## S6 — the easy direction (q ∈ Z ⇒ ∃ rational w with Φ(q,w)=0) — **NOT-REACHED**

What is established here: Φ ≥ 0 and Φ = 0 ⟺ all 4,552 residuals vanish (EXACTLY-CHECKED, S3),
and every elimination in the chain is a **genuine definition** (verified exact), so the chain is
invertible by forward substitution and a solution of the 4,513-row source system lifts to a
solution of the 4,552-row reduced system.

What is **not** established by the shipped algebraic artifact, measured rather than assumed:

- The residual list alone is not a definition chain: a forward-substitution sweep from the input
  variable determines only **34 of 4,973** variables before stalling. The q ↦ w map is **not**
  contained in `residuals.json.gz`.
- The all-zero assignment is not a witness (Φ's constant term is 1,900,333,570,565,983 ≠ 0).
- Existence of a witness for each integer q is the **source arithmetic theorem**: the release
  states this explicitly in `evidence/final-verification.json` ("The source arithmetic theorem is
  not checked here") and supports it separately in `evidence/arithmetic-source-review.md`.
  Nothing in this lane's artifact can decide it.

**Checked and NOT a finding, though it looked like one:** 27 of the 121 eliminations carry a
non-unit denominator (e.g. 127,449; 2,688,000) and both shears use fractional scalars
(−1/2, −2/3), so the lift is **rational**, not integral. The manuscript's claim is "rational zero
projection exactly Z" (line 51), i.e. rational witnesses are exactly what is claimed — the
fractional denominators are consistent with the stated theorem, not a defect. Recorded because a
reader expecting integer witnesses would misread it.

## Control arms — the checker is known to fail

`control_arms.py` mutates one shipped input at a time in a throwaway copy; each arm must flip the
verdict: coefficient +1 in Φ → caught; one Φ term deleted → caught; last residual deleted →
caught; one residual reweighted to 2 → caught; one `linear` patch coefficient +1 → caught.
**5/5 caught.** A variant term list can be re-checked with `--termlist FILE` (accepts both the
shipped repeated-index form and this lane's canonical `var:exp` form, gz or plain; the canonical
artifact below was re-verified through it and S3 holds).

## Artifact

`artifacts/phi-4973.canonical.txt.gz` — the same polynomial, deterministically ordered, from
`make_canonical.py`:

- 72,925 terms, one per line, `<coeff> <var>:<exp> …`, sorted by sparse monomial key
- plain 1,836,663 B / gzipped **334,290 B** (reproducible: `gzip mtime=0`)
- sha256 plain `7296204974548c1feb83315fd2ca2e91410acfe6e56fd070e9ae1b2361113580`
- sha256 gz `d9a5126709ef9a4c7ece84c26fa83fa4855ed64d46ab063b77ac18fdf675f075`
- regeneration: `python3 make_canonical.py work/current/quartics/quartic-4973/polynomial.expanded.txt artifacts/phi-4973.canonical.txt.gz`

Feeding this artifact back through `checker.py --termlist` reproduces the S1 metrics and S3
identity (0 mismatches), which is the proof that the re-encoding is faithful.

## Nothing smelled wrong, with two observations

1. The producer's declared `expanded_sha256` and `certificate_sha256` both match the shipped bytes,
   and the declared counts match this checker's independent measurements — the self-report is not
   merely self-consistent, it is correct.
2. The `final` record is stamped `"status": "CANDIDATE: independent verification pending"` inside
   the certificate while `evidence/final-verification.json` says `"status": "PASS"`. That is a
   scoping nuance, not a contradiction: the PASS covers the algebraic checks, and both documents
   say the arithmetic theorem is out of scope.
