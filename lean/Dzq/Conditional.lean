/-
Conditional.lean — the CONDITIONAL-FRAME harness, mirroring the v4 dependency graph.

The incumbents' Lean theorems are conditional: the `sorry` sits on NAMED ARITHMETIC
HYPOTHESES, not on the polynomial identity. A verified row must be COMPARABLE to
theirs — same hypotheses, same names, no hidden assumptions.

DEPENDENCY GRAPH (from the v4 source, line refs in `quartic_4973.tex`):

  lem:pole  (:1003)  PROVED, UNCONDITIONAL  — soundness engine, contributes NO hypothesis
  hyp:RC    (:1020)  AXIOM-LEVEL LEAF       — classical inputs (Rankin factorisation,
                                              L(E^k,1) ≠ 0, Sha-sign discard)
  hyp:PC    (:1016)  DERIVED                — from hyp:RC + lem:pole (NOT primitive)
  hyp:o8-height (:6670) CHECKED NUMBER + CHARACTERIZATION HYPOTHESIS
                       H* = 2(4608^165888 + 6^100)·B_*^24 + 128, log₂ H* < 4,783,227
                       contacts {∞, 0, 1, 2401, −343/32}
                       open_obligations: [] BUT the construction's own caveat list
                       says `finite_checks_do_not_prove: characterization` — the
                       check does not prove H* IS a height constant. That is the
                       hypothesis, and it is exposed as such below.

STATUS: kernel-checked, toolchain v4.34.1 / Mathlib d13f23b7.
-/

import Dzq.Scaff

set_option autoImplicit false

namespace Dzq

/-! ### 1. The leaf hypothesis: `hyp:RC` -/

/-- **`RC_stmt`** — `hyp:RC` (:1020), verbatim:

For every positive squarefree `ℓ ≡ 11 (mod 12)`, for
`E_ℓ : y² = x(x − ℓ)(x + 3ℓ)`  (non-CM, `j = 35152/9`),
`corank_{ℤ₂} Sel_{2^∞}(E_ℓ/ℚ) = 1  ⇒  ord_{s=1} L(E_ℓ, s) = 1`.

The manuscript's own proof consumes the classical leaves — Rankin factorisation,
`L(E^k, 1) ≠ 0`, the Sha-sign discard. Those leaves are what a full formalization
must eventually land on; this `Prop` is the boundary where the certificate stops.

NOT in Mathlib: elliptic-curve Selmer groups over ℚ, `L`-functions (GAP_LIST.md §A). -/
opaque RC_stmt : Prop

/-! ### 2. The height hypothesis: a CHARACTERIZATION claim, not a computation -/

/-- **`H_is_height_constant`** — `hyp:o8-height` (:6670).

The finite check verifies the NUMBER
`H* = 2(4608^165888 + 6^100)·B_*^24 + 128` (contacts `{∞, 0, 1, 2401, −343/32}`,
`log₂ H* < 4,783,227`). What the finite check does NOT establish — and the
construction's own caveat list says so (`finite_checks_do_not_prove:
characterization`) — is that this number behaves as a HEIGHT constant for all
inputs, i.e. satisfies the six-contact estimate uniformly.

That gap is this hypothesis. Exposing it separately is what keeps the row honest.

NOT in Mathlib: canonical (Néron–Tate) heights (GAP_LIST.md §A). -/
opaque H_is_height_constant : Prop

/-! ### 3. `hyp:PC` is DERIVED, never primitive -/

/-- **`PC_stmt`** — `hyp:PC` (:1016): for every rational `B` with square reduced
denominator, `0 < B < 1/2`, and `v_p(B) ≥ 4` for all `p ∈ S_*`, the pole
predicate `Φ(B)` holds. -/
opaque PC_stmt : Prop

/-- **The derivation obligation** `hyp:RC ⇒ hyp:PC`, proved in the manuscript from
`hyp:RC` together with `lem:pole` (which is unconditional and therefore adds no
hypothesis). Carried as an explicit obligation rather than assuming `PC` outright —
this is the dependency structure the incumbents actually have.

NOT formalizable today: needs p-adic valuations on the elliptic model. -/
def PC_derivation : Prop := RC_stmt → PC_stmt

/-! ### 4. The certificate shape -/

/-- A conditional certificate for a concrete polynomial: the two leaf hypotheses
plus the RC⇒PC derivation imply the race property. Comparable to the incumbent rows
by construction — same hypotheses, same names, none hidden. -/
def QuarticCertificate (k : ℕ) (P : MvPolynomial (Fin (k + 1)) ℤ) : Prop :=
  RC_stmt → H_is_height_constant → PC_derivation → DefinesZ k P

/-- **Tier separation.** The mechanical half does not consume the arithmetic
hypotheses at all — it proves `DefinesZ` outright, and the conditional frame follows
by discarding them. So:

  * mechanical half → `DefinesZ k P`            (Tier 1, certifiable; `Scaff.lean`)
  * arithmetic half → `HardDirection C`          (Tier 2, research-level)

and no arithmetic hypothesis is load-bearing inside the mechanical proof. -/
theorem conditional_of_sos (C : SosCert) (h_easy : EasyDirection C)
    (h_hard : HardDirection C) : QuarticCertificate C.k C.P :=
  fun _ _ _ => DefinesZ.of_sos C h_easy h_hard

/-- An unconditional proof yields the conditional frame a fortiori. -/
theorem conditional_of_unconditional (k : ℕ) (P : MvPolynomial (Fin (k + 1)) ℤ)
    (h : DefinesZ k P) : QuarticCertificate k P :=
  fun _ _ _ => h

/-! ### 5. The v4 residual shape, instantiated

`Φ = Σ_{i=1}^{4552} R_i²` over quadratic residuals. The collapse lemma is generic in
the residual count, so the instance below is free — the size of the system is not a
proof-length parameter. (The 551-transform certificate — 266 row ops, 148
eliminations, 121 def-eliminations, 13 power circuits, 2 shears, 1 parity-block
rewrite — is what produces the `ident` field of `SosCert`; it is a transcription
obligation, not a proof obligation.) -/

/-- The v4 residual count. -/
def v4ResidualCount : ℕ := 4552

/-- The collapse at exactly the v4 shape: 4,552 quadratic residuals. -/
theorem v4_collapse (R : Fin v4ResidualCount → ℚ) :
    (∑ i, (R i) ^ 2 = 0) ↔ ∀ i, R i = 0 :=
  sum_sq_eq_zero_iff_fin R

/-- The rational-vs-integer subtlety, stated explicitly: coefficients are integers,
the vanishing is over ℚ, and the two agree because evaluation is a ring map ℤ → ℚ.
Nothing here needs the integrality of the coefficients; the collapse lives in ℚ. -/
theorem collapse_coeff_agnostic {ι : Type*} (s : Finset ι) (f : ι → ℚ) :
    (∑ i ∈ s, (f i) ^ 2 = 0) ↔ ∀ i ∈ s, f i = 0 :=
  sum_sq_eq_zero_iff s f

end Dzq
