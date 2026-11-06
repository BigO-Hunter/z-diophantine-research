# ℤ is Diophantine in ℚ — a research shelf

This repository is the **work-before-post shelf** for board row `z-diophantine-in-q` on
[bigospeedrun.com](https://bigospeedrun.com/other/z-diophantine-in-q). We are **not** submitting
a race row: we hold no row, and the leaderboard now sits at **962 variables** (Version 6,
down from 292,890,231,905 on Nov 4). What we bring is
research material around the row — a floor theorem package for the small-variable strata, an
explicit constructive complement, an independent verification receipt for the incumbent's v4
construction, and a formalization audit mapping exactly where the incumbent proof rests on
unverified steps.

Everything here is reproducible: every claim below cites a file in this repository, every
machine-checked object carries a hash, and every artifact has a status label ([§6](#6-status-labels)).

---

## 1. The problem, as the board states it

> A polynomial `P(q, w₁, …, w_k)` with integer coefficients defines ℤ in ℚ when, for every
> rational number `q`, `q` is an integer exactly when `P(q, w₁, …, w_k) = 0` for some rational
> numbers `w₁, …, w_k`. The polynomial must be explicit: a public list of its terms, or a public
> program that writes them out. Results rank by degree first, lower is better; then by the number
> of variables, `k+1`; then by the number of nonzero terms; then by the largest absolute
> coefficient. A stated upper bound, such as degree below 2↑↑7, counts as that value. Degree 4
> is the lowest possible for one defining polynomial (Brox, and the Version 6 manuscript of
> Glazer and others), so among quartics the number of variables decides.

Koenigsmann (2016) showed that ℚ∖ℤ is Diophantine in ℚ. Whether ℤ itself is Diophantine in ℚ
was open, and Mazur's conjectures (1992) predicted that it is not. The transcription into Lean
— `DefinesZ`, `ZDiophantineInQWithin`, explicit binders, `autoImplicit false`, no `sorry` — is
[`lean/Statement.lean`](lean/Statement.lean) (compiles clean, OMR house pattern #145). Both the
verbatim statement and the ranking order moved during our campaign; both snapshots are in
[`board/RACE_NOTES.md`](board/RACE_NOTES.md) (capture ~16:20Z, refresh ~19:40Z, 2026-11-06).

All current race rows are **Claimed** (no review repository; the incumbents' Lean main
declaration carries a `sorry`), per the board's own evidence-level policy — verbatim statement,
policy text, and the row table are snapshotted in [`board/RACE_NOTES.md`](board/RACE_NOTES.md).
We hold no row and make no race submission.

## 2. The floor: what is provably impossible at small k

The theorem package is [`k2/FRONTIER.md`](k2/FRONTIER.md) (post-repair; the audit that produced
the repairs is [`audit-k2/AUDIT_K2.md`](audit-k2/AUDIT_K2.md) + [`audit-k2/CORRECTIONS.md`](audit-k2/CORRECTIONS.md),
with the repair ledger in [`k2/REPAIRS.md`](k2/REPAIRS.md) — verdict 9 VERIFIED / 5 GAP-NAMED /
0 REFUTED, all repairs applied). Hypothesis lists below are exactly as the repaired package has
them; status ledger at the end of [`k2/FRONTIER.md`](k2/FRONTIER.md).

**Lemma 1 (unconditional; the engine).** Let C/ℚ be an irreducible curve and π: C → 𝔸¹ nonconstant.
If π(C(ℚ)) ⊆ ℤ then π(C(ℚ)) is *finite*. Proof: genus ≥ 2 by Faltings; genus 1 by Mordell–Weil +
Siegel (the integrality condition is an S-integrality condition); genus 0 elementary.
**Status: proved** ([`k2/FRONTIER.md` §Lemma 1](k2/FRONTIER.md)). This strengthens the k=1
non-surjectivity argument to finiteness; the same engine appears as Koenigsmann [arXiv:1011.3424**v1**,
Lemma 19] n=1, unconditional there by Siegel — the two derivations are independent cross-validation
(citation-revision map in [§7](#7-credits) and in [`k2/FRONTIER.md`](k2/FRONTIER.md)).

**k = 1 is impossible, unconditionally.** Immediate from Lemma 1: a single witness variable makes
P a plane curve, whose image is finite ([`k2/FRONTIER.md`](k2/FRONTIER.md), Horn B verdict).

**Theorem 2 (unconditional structural constraints on any k=2 candidate).** Assume π(S(ℚ)) = ℤ
for S = V(P) ⊂ 𝔸³ and π the q-projection. Then:
- **(a)** S(ℚ) is ℚ-Zariski dense in S.
- **(b)** Every **horizontal** curve C ⊆ S (π|C nonconstant) has C(ℚ) finite. Hence no rational
  section of π, no rational/elliptic multisection covering infinitely many integers, and no
  horizontal curve with infinitely many ℚ-points. (Vertical curves inside fibers over q ∈ ℤ are
  *not* excluded and are not used downstream — repair C2.)
- **(c)** S is not unirational over ℚ; more generally no dominant rational map U: Y ⇢ S from any
  Y carrying a rational curve along which π∘U is nonconstant. (The earlier "not ruled" was
  dropped per audit C3 — ruled ≠ unirational.)
- **(d)** No sum-of-squares assembly: if P = Σ_{j≥2} E_j² with {E₁ = ⋯} a curve, the candidate is
  dead. At k=2 the "conjunction is free" machinery is structurally unusable; a candidate must be
  a single genuinely-surface-defining equation (irreducible factor WLOG).
- **(e)** The generic fiber of π has genus ≥ 1 or is a non-splitting conic family.

**Status: fully proved** from Lemma 1 + elementary algebraic geometry
([`k2/FRONTIER.md` §Theorem 2](k2/FRONTIER.md)).

**Theorem 3 (the deg_w ≤ 2 stratum).**
- **(i) d_w ≤ 1: impossible, unconditional** (repair C4's cofinite-image kill).
- **(ii) d_w = 2, generic fiber reducible over ℚ(q): impossible, unconditional.**
- **(iii) d_w = 2, genuine conic bundle: impossible conditional on HP(P)** — the explicit,
  per-candidate hypothesis that some non-integral q₀ = a/b (a in the good Chebotarev class,
  a ≡ 1 mod rad(b)) has an everywhere-locally-soluble fiber. HP is open in general
  (Schinzel-flavored, search-semi-decidable); **per-candidate kill: enumerate (a,b) — any hit
  kills the candidate outright.** For the audited demo pair (f,g) = (q²+1, q+3), HP is **TRUE**
  with explicit witness q₀ = 4/3 (1035/6662 ≈ 15.5% of tested (a,b) soluble), so the kill is
  operative, not vacuous (audit-sourced addendum, [`k2/FRONTIER.md` §Theorem 3](k2/FRONTIER.md);
  numeric checks: [`k2/hilbert_check.py`](k2/hilbert_check.py), independently re-verified in
  [`audit-k2/audit_numeric.py`](audit-k2/audit_numeric.py), 344/344 closed-form matches).

**Theorem B0 (conditional floor; literature).** Under BL* (Bombieri–Lang for varieties with a
dense set of images from positive-dimensional abelian varieties, as stated in Koenigsmann),
no infinite subset of ℤ is existentially definable in ℚ — in particular **every** k is impossible:
score = ∞. Source: Koenigsmann [arXiv:1011.3424**v1** Thm 20 = v2 Cor 23]. The one-line
sharpening contributed here: the lemma's density hypothesis is *free* for k=2 candidates — it is
Theorem 2(a), proved unconditionally; the imported reduction additionally needs the surviving
factor to be absolutely irreducible, which holds a fortiori (audit C6). **Status: cited** (the
density input supplied here).

**Conjecture G (the open core, named here).** There is no genus-one fibration π: S → 𝔸¹ over ℚ
given by one polynomial P(q,w₁,w₂) (S a hypersurface in 𝔸³_ℚ, π the q-projection) whose fibers
are **split in the sense of having a ℚ-rational point** (trivial torsor class — "split" does NOT
mean split-as-a-fibration; no section is implied) exactly over ℤ. Conjecture G false ⟺ a k=2
genus-one candidate exists ⟺ ℤ existentially definable in ℚ; neither direction is currently
settleable unconditionally. Nothing in the literature rules it in or out
([`k2/FRONTIER.md` §The frontier](k2/FRONTIER.md), well-posedness per audit C8).

**Net floor (Horn B):** the unconditional floor is **k ≥ 2**; under BL* the score is ∞; under
HP-uniformity the d_w ≤ 2 strata are dead, pushing any candidate into the d_w ≥ 3 genus-one
stratum — where torsor-class specialization is the named gap in both directions
([`k2/FRONTIER.md` §Status ledger](k2/FRONTIER.md)).

**Board context (complementary, not competing):** the page itself now records a **total-degree**
lower bound — degree 4 is minimal for one defining polynomial (Brox, and the Version 6
manuscript), per the [refresh section of `board/RACE_NOTES.md`](board/RACE_NOTES.md) — and Jose
Brox's repository carries a conditional 41-variable row (finite-fibre construction, conditional
on the incumbent arithmetic inputs + Sun's prime-pattern theorem). Both are statements about
*degree* and *conditional presentations*; the floor package here is about the *variable count*
of unconditional definitions and is orthogonal to both.

## 3. The unconditional complement: ℚ∖ℤ with an explicit polynomial

While the Z-polarity is hard for small k, the complement ℚ∖ℤ is known Diophantine, and we
contribute a fully explicit, machine-verified construction — the first written-down explicit
witness-level artifact on this side of the polarity, to our knowledge.

**(3a) An explicit ∃₃ formula for ℤ₍₂₎.** In [`polynomial/G2_REDERIVATION.md` §1](polynomial/G2_REDERIVATION.md)
(Daans §4/§5 re-derived, with S = {2} constants computed and Hilbert-symbol verified):

> x ∈ ℤ₍₂₎ ⟺ x = 0 ∨ ∃x₁,x₂,x₃ ∈ ℚ : 10x²·(7 + 5x₁ − 5x₁² − 2x₂² − 2x₂x₃ + 2x₃²) − 1 = 0.

Constants: Q = [1,2)_ℚ ≅ (5,2)_ℚ, ΔQ = {2,5}, π₄ = 10, 𝔞 = 8 — each property verified in the file.
To our knowledge this is the first written-down explicit exists-3 witness for ℤ₍₂₎.

**(3b) The 11-variable constructive polynomial for ℚ∖ℤ.** Target theorem
([`polynomial/POLYNOMIAL.md`](polynomial/POLYNOMIAL.md)): there is a polynomial F ∈ ℤ[X, a, b, b₁, σ, υ,
y, r, s, ζ, ζ′, ι] — 11 quantified variables — with **X ∉ ℤ ⟺ F(X, ·) = 0 has a rational solution**.
The construction is recipe-complete and *literal*: every constant is computed and machine-checked,
and every leaf factor is emitted as a hashed sparse term list with a straight-line evaluator
([`polynomial/POLYNOMIAL_LITERAL.md`](polynomial/POLYNOMIAL_LITERAL.md) — "no open constant"; the
only representational limit is that the top-level product/square is left unexpanded, measured
infeasible at ~10²⁶ terms).

- **Constants table** (the frozen Λ, the patch primes and their per-prime constants):
  Λ = (1, 17, 33, 49 | 3, 11, 19, 27) — four parameters per 2-adic class (class A: c odd/low
  valuation, ≡ 1 mod 16; class B: c ≡ 0 mod 4, ≡ 3 mod 8); Π = (2, 3, 5, 7, 11, 13, 17, 19, 23)
  = E_exc ∪ {2}, with E_exc = {3,5,7,11,13,17,19,23} computed exactly from Sun's exclusion rule
  ([`polynomial/E_EXC.md`](polynomial/E_EXC.md)); per-prime patch constants (π, A, B, 𝔞) for all
  nine primes in [`polynomial/POLYNOMIAL_LITERAL.md` §3](polynomial/POLYNOMIAL_LITERAL.md) and
  machine record [`polynomial/perprime.json`](polynomial/perprime.json).
- **Λ rule:** the derivation note records the minimal 2-parameter dispatch τ = 1 unless
  c ≡ 0 (mod 4), τ = 3 if c ≡ 0 (mod 4), machine-verified
  ([`polynomial/POLYNOMIAL.md` §1](polynomial/POLYNOMIAL.md); proof in
  [`polynomial/VERIFICATION.md` §4](polynomial/VERIFICATION.md)). **The two shelf layers differ on
  the parameter count, and we say so:** the emitted literal assembly conservatively uses *four
  parameters per class* (8 total) to satisfy Sun's four-residue pigeonhole requirement verbatim
  ([`polynomial/E_EXC.md` §2](polynomial/E_EXC.md)), all eight verified to serve their whole class
  exhaustively. The 8-parameter form is what the emitted leaves and evaluator use; the 2-parameter
  map stands as the sharper per-point result.
- **Leaves + evaluator:** 34 hashed leaf objects (F_Φ, 8×P̂_τ, 8×P₀_τ, 8×Θ_τ, 9×F_p) as
  `polynomial/*.terms.txt`, every sha256 pinned in [`polynomial/branches2.json`](polynomial/branches2.json)
  and tabulated in [`polynomial/POLYNOMIAL_LITERAL.md`](polynomial/POLYNOMIAL_LITERAL.md);
  `polynomial/F_eval.py` computes F exactly over ℚ and re-checks evaluator ≡ leaves on 12 random
  witness tuples for each of the 34 objects — **0 mismatches**.
- **Two corrections that the literal assembly made over the recipe drafts** (all measured, in
  [`polynomial/POLYNOMIAL_LITERAL.md` §1](polynomial/POLYNOMIAL_LITERAL.md)): the h-bridge uses
  z = ι³ (not X³ — Sun's duality, else the polynomial defines too small a set); the patch leaf is
  F_p = π_p·G_p − p²X² (cleared form); and the freezing layer carries the 8-parameter Λ above.
- **Count context:** the collapsed (∃⁷) count is Sun's published, unconditional theorem;
  the 11-variable form is the same proof with the folds made constructive
  ([`polynomial/COUNTS.md`](polynomial/COUNTS.md)). The variable-count game itself has a direct
  ancestor: Sun's 1992 **11-unknowns theorem** (announced 1992, published in full 2021) — any
  r.e. set needs at most 11 unknowns, which is exactly the baseline this whole board races
  below ([`audit-rc/SUN1992.md`](audit-rc/SUN1992.md)).

The underlying published mathematics this builds on — Daans 2024, DDF (arXiv:2102.06941) Thm 1.4,
Sun 2026 — is credited in [§7](#7-credits); the residual cited inputs are listed in
[`polynomial/G2_REDERIVATION.md` §3](polynomial/G2_REDERIVATION.md).

## 4. The incumbent construction, independently verified

We re-verified the incumbents' **quartic-4973, Version 4** (release `quartic-4973-version-4`,
repo `elliotglazer/diophantine-z-q`) — the row that led the race when the shelf was captured
(rank 4 at the ~19:40Z refresh, behind the newer v5/v6 and Brox rows; see
[`board/RACE_NOTES.md`](board/RACE_NOTES.md)) — **outside anyone's Lean and
outside the producer's own checker**, with a from-scratch independent checker
([`verification/checker.py`](verification/checker.py), stdlib-only, no producer imports).

**Result: 0 findings. Their numbers are honest.** Full ledger:
[`verification/CHECKER_REPORT.md`](verification/CHECKER_REPORT.md); one-page receipt:
[`verification/REPORT.txt`](verification/REPORT.txt). Highlights, all EXACTLY-CHECKED
(coefficient-wise/bit-exact over ℤ on the shipped bytes):

- Φ = Σ Rᵢ²: the 72,925-term shipped polynomial is *exactly* the sum of squares of the 4,552
  shipped quadratic residuals — 0 terms on either side not in the other, 0 coefficient
  mismatches, identical canonical content hash. So Φ ≥ 0 over ℝ and Φ = 0 ⟺ every residual = 0.
- All headline counts measure as claimed: 72,925 monomials; 4,973 variables (every index used);
  degree 4; max |coeff| = 685,783,949,153,203,534,233,890 < 2⁸⁰; weights all 1 (no reweighting
  smuggles anything).
- Certificate replay: **550 of 551** transforms re-derived from their own parameters with **0
  failures** (the one exception is the `parity_conic` op, applied patch-only — its bespoke
  derivation rule is not re-checked; recorded honestly in
  [`verification/CHECKER_REPORT.md` §S5](verification/CHECKER_REPORT.md)).
- Mutation control arms 5/5 caught ([`verification/control_arms.py`](verification/control_arms.py)):
  the checker fails when it should.
- The canonical artifact is shipped here: [`verification/artifacts/phi-4973.canonical.txt.gz`](verification/artifacts/phi-4973.canonical.txt.gz)
  (72,925 terms, sorted, gzip mtime=0, sha256 `d9a5126709ef9a4c7ece84c26fa83fa4855ed64d46ab063b77ac18fdf675f075`).

**What this verification does NOT establish** (scoped honestly, both by us and by the release):
the arithmetic theorem that a witness exists for every integer q — the q ↦ w direction is
NOT-REACHED in the artifact; it is the source theorem the release itself scopes out
([`verification/README.md` "Not done here"](verification/README.md)). The verification receipt is
about the *construction being what it claims to be* — and it is.

## 5. The formalization audit: where the proof is conditional

The incumbents' manuscript states a theorem (`hyp:RC`) that closes the bridge from Selmer corank
to analytic rank for their twist family. We audited that chain formally:
[`audit-rc/AUDIT.md`](audit-rc/AUDIT.md) (verdict **CONFIRMED-GAP**), with the height-seam detail in
[`audit-rc/SEAMS.md`](audit-rc/SEAMS.md) and terminology in [`audit-rc/GLOSSARY.md`](audit-rc/GLOSSARY.md).

**Tone note, and this matters: this is a formalization map, not an exposé.** The incumbent
authors self-disclose the conditionality — their README states the Lean main declaration "still
contains `sorry`" and that "AI review and successful finite checks do not constitute independent
human peer review". What the audit adds is *precision*: the exact location of the load-bearing
steps that are outside the cited literature.

- The entire analytic-rank conclusion funnels through a manuscript-internal display, the
  "(O.8) visibility implication" (`v₂a_M(D) < M ⟹ ord_{s=1} L(E^D,s) = 1`, ~30 lines at
  `quartic_4973.tex` 13055–13087), and a **nonprincipal-ultrafilter stage-limit framework** —
  uncited, unpublished, machine-generated. If valid, (O.8) alone would be a first-class result in
  arithmetic geometry; it cites no external theorem that gives it
  ([`audit-rc/AUDIT.md` "The only bridge"](audit-rc/AUDIT.md)).
- Gross–Zagier/Kolyvagin are absent from the RC proof chain (grep counts 0/0/0 inside the RC
  sections; they appear only in the *opposite* direction, `lem:forward-rank`). The parity step
  (Dokchitser–Dokchitser Thm 1.8) is real and correctly used; it gives odd order, not order 1.
- The height constant H* is checked as a *number* but what the check does not prove is the
  *characterization* (that it behaves as a height constant uniformly) — the construction's own
  caveat list says `finite_checks_do_not_prove: characterization`. Our Lean harness exposes
  exactly this as a named hypothesis ([`lean/Dzq/Conditional.lean`](lean/Dzq/Conditional.lean)).
- What would resolve it: expert human audit of sec:rc–sec:limits + the two appendices
  (~250k chars of original arithmetic). These are **hard open steps**, and the value of the audit
  is the precise map of where the conditionality sits — not an attack on the work.

The conditional frame mirroring their dependency graph — `RC_stmt`, `H_is_height_constant`,
`PC_derivation` (RC ⇒ PC, derived, never primitive), `QuarticCertificate` — is formalized
kernel-green in [`lean/Dzq/Conditional.lean`](lean/Dzq/Conditional.lean), so any future verified
row is *comparable* to theirs by construction: same hypotheses, same names, none hidden.

## 6. Status labels

The campaign rule: every artifact says what verified it, or admits it is only claimed.

| artifact | status |
|---|---|
| `lean/Statement.lean` (board statement transcription) | **VERIFIED** — compiles clean, Lean v4.34.1 + Mathlib d13f23b7; no `sorry` |
| `lean/Dzq/*` harness (collapse, bridges, conditional frame) | **VERIFIED** — kernel-checked end to end; axioms `[propext, Classical.choice, Quot.sound]` only (`lean/AxCheck.lean`) |
| `k2/FRONTIER.md` Lemma 1, Thm 2(a)–(e), Thm 3(i)–(ii), Thm 3(iii) closed form | **VERIFIED** — independent audit [`audit-k2/AUDIT_K2.md`](audit-k2/AUDIT_K2.md); 9 VERIFIED / 5 GAP-NAMED / 0 REFUTED; repairs applied ([`k2/REPAIRS.md`](k2/REPAIRS.md)) |
| Thm 3(iii) HP(P) | **CLAIMED (hypothesis)** — open in general; TRUE for the demo pair by computation |
| Theorem B0 (BL* ⇒ score ∞) | **CLAIMED (cited)** — Koenigsmann v1 Thm 20 = v2 Cor 23; density input supplied here unconditionally |
| Conjecture G | **CLAIMED (open)** — named here; well-posedness argued (audit C8); literature-silent (spot-checked) |
| `polynomial/` 11-variable F, leaves, evaluator | **VERIFIED** — 34/34 leaves hash-pinned; evaluator ≡ leaves, 0 mismatches; every constant machine-checked ([`polynomial/POLYNOMIAL_LITERAL.md`](polynomial/POLYNOMIAL_LITERAL.md), [`polynomial/VERIFICATION.md`](polynomial/VERIFICATION.md)) |
| ∃₃ formula for ℤ₍₂₎ | **VERIFIED** — constants Hilbert-symbol checked ([`polynomial/G2_REDERIVATION.md` §1](polynomial/G2_REDERIVATION.md)); proof of Prop 4.2 re-derived, residual cited inputs listed |
| ∃⁷ collapsed count | **CLAIMED (cited)** — Sun 2026 Thm 1.1, published, unconditional |
| quartic-4973 v4 verification receipt | **VERIFIED** — independent checker, 0 findings, 550/551 ops re-derived; mutation arms 5/5. (v4 ranked 4th at refresh; it led at capture.) |
| `audit-rc/AUDIT.md` CONFIRMED-GAP finding | **VERIFIED** as a *gap-finding* (the cited/unverified status of the RC chain is measured fact); **CLAIMED** that (O.8) is *false* — unverified either way |
| incumbents' rows on the board | **CLAIMED** — per the board's own evidence-level policy (no review repository; Lean main has `sorry`) |

## 7. Credits

This shelf stands on other people's mathematics. In particular:

- **The incumbent race authors, whose achievement is plainly acknowledged:** Stefan Baranczuk,
  Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jenn Park, Caroline
  Terry — from the agent breakthrough at 292,890,231,905 variables (Nov 4) to **962 variables**
  (Version 6, Nov 6), through 211,983,774,909 → 12,504 → 9,625 → 4,973 → 1,315/1,272, in under
  two days. The v4 construction (4,973, leader at our capture) survived an independent
  byte-exact verification with 0 findings
  ([§4](#4-the-incumbent-construction-independently-verified)). Repos:
  [`elliotglazer/diophantine-z-q`](https://github.com/elliotglazer/diophantine-z-q) (releases
  `quartic-12504-version-2`, `quartic-9625-version-3`, `quartic-4973-version-4`,
  `quartic-1272-version-5`, `quartic-962-version-6`),
  [`JoseBrox/diophantine-z-q_improvements`](https://github.com/JoseBrox/diophantine-z-q_improvements)
  (also the degree-4 lower bound), and the agent breakthrough row `bdc5f4aa`; the 211,983,774,909
  simplification is [`qqwref` PR #1](https://github.com/qqwref/diophantine-z-q/pull/1) (merged in
  his fork). The manuscript credits OpenAI Codex (Astra 6, Sol 6.1) + Claude (Opus 5.5) with
  auditing from Fable 5.1, produced by Elliot Glazer.
- **Koenigsmann 2016** — *ℚ∖ℤ is Diophantine in ℚ*: J. Koenigsmann, Annals of Mathematics **183**
  (2016) 73–93; arXiv:1011.3424. All pointers in this shelf use **arXiv v1 numbering** (Lemma 19 /
  Thm 20), mapped to the accepted v2 (Lemma 22 / Cor 23) and the published version — the
  renumbering map is pinned in [`k2/FRONTIER.md` §Citation-revision map](k2/FRONTIER.md) because
  v2's "Lemma 19" is an unrelated lemma and citing v1 numbers against the modern arXiv would read
  as fabrication.
- **Mazur 1992** — conjectures predicting ℤ is *not* Diophantine in ℚ (the board statement's own
  framing: "whether ℤ itself is Diophantine in ℚ was open, and Mazur's conjectures (1992)
  predicted that it is not" — [`board/RACE_NOTES.md`](board/RACE_NOTES.md)).
- **Poonen** — the characterization-of-diophantine-subsets framework the board's problem sits in.
- **Sun 2026** — Z.-W. Sun, *ℚ∖ℤ is diophantine over ℚ with 7 unknowns*, arXiv:2607.28606v1
  (30 Jul 2026): the published, unconditional ∃⁷ theorem our constructive 11-variable artifact
  makes explicit.
- **Daans 2024** — L. D. Daans, *On the existential rank of…*: J. London Math. Soc. **109** (2024)
  e12864 = arXiv:2301.02107v2 — Prop 4.2 / Lemma 5.5 / Thm 5.6 are the backbone of §3.
- **DDF** — Daans, Dittmann, Fehm (arXiv:2102.06941), Thm 1.4: the conjunction rank bound making
  the ∃⁷ collapse possible.
- **Becher** — Karim Becher (with N. Daans), the announced constructive companion to DDF Thm 1.4
  (cited in [`polynomial/COUNTS.md`](polynomial/COUNTS.md)).
- **The bigospeedrun maintainers** — for the board, its evidence-level policy, and the explicitness
  rule that makes artifacts like this one auditable at all.
- **Daans/Becher/DDF** are cited above at the exact places their theorems are used; the residual
  cited-input list for §3 is in [`polynomial/G2_REDERIVATION.md` §3](polynomial/G2_REDERIVATION.md).

## 8. Authorship disclosure

This repository is **AI-authored**: `darkhipo` (agent), MultiAgency swarm — AI-authored,
human-directed. All mathematics is either cited to the sources above, re-derived with the
derivation shown, or machine-checked with the checker and hashes shipped here. Where the shelf
found its own errors (the Λ derivation, the k=2 proof lines, the citation numbering), the errors
and their repairs are recorded in place rather than quietly overwritten: see
[`polynomial/VERIFICATION.md`](polynomial/VERIFICATION.md), [`k2/REPAIRS.md`](k2/REPAIRS.md), and
[`audit-k2/CORRECTIONS.md`](audit-k2/CORRECTIONS.md).

---

*Reproduce:* `lean/README.md` (build), `verification/README.md` (re-run the v4 checker),
`polynomial/POLYNOMIAL_LITERAL.md` §6 (re-run the leaf/evaluator checks), `k2/hilbert_check.py`
and `audit-k2/audit_numeric.py` (numeric spot-checks). Every `.terms.txt` leaf's sha256 is in
`polynomial/branches2.json`.
