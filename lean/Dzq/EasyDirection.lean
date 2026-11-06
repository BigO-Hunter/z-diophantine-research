/-
EasyDirection.lean — TIER 2, easy half: the witness-family pattern.

Direction 1 of the board property is `q ∈ ℤ ⇒ ∃ w, P(q,w) = 0`. For every actual
construction this is CONSTRUCTIVE: one explicitly given family of rational witness
tuples, substituted into the residuals. So the lane's whole obligation for this half is

    supply `W : ℚ → Fin k → ℚ` and prove `hW : ∀ q j, residual_j(W q, q) = 0`.

`easyDirection_of_witnessFamily` below turns exactly that into `EasyDirection C`.
Nothing else is needed — no arithmetic geometry, no global argument, no hypotheses.

Then a concrete end-to-end demonstration on a 2-variable toy, which exercises the
same machinery a real candidate would (concrete `MvPolynomial`, concrete rational
point, `norm_num`), INCLUDING the control arm that kills a naive candidate in one line.

STATUS: kernel-checked, toolchain v4.34.1 / Mathlib d13f23b7.
-/

import Dzq.Scaff
import Mathlib.Tactic.NormNum.GCD

set_option autoImplicit false

namespace Dzq

/-! ### 1. The witness-family pattern (the only thing the easy half must supply) -/

/-- **Easy-direction reduction.** If some witness family `W` solves the residual
system at every rational input, then every integer input has a witness tuple.

This is the entire content of direction 1 for a concrete construction: the lane
provides `W` (rational functions of `q`) plus `hW` (polynomial identities). -/
theorem easyDirection_of_witnessFamily (C : SosCert) (W : ℚ → Fin C.k → ℚ)
    (hW : ∀ q : ℚ, ∀ j : Fin C.m, evalQ (C.quad j) (Fin.snoc (W q) q) = 0) :
    EasyDirection C := by
  intro n
  refine ⟨W (n : ℚ), ?_⟩
  exact (C.evalQ_eq_zero_iff (Fin.snoc (W (n : ℚ)) (n : ℚ))).mpr (hW (n : ℚ))

/-- Same pattern stated directly against `P`, for constructions that do not (yet)
expose a residual system. -/
theorem easyDirection_of_P_witness {k : ℕ} (P : MvPolynomial (Fin (k + 1)) ℤ)
    (W : ℚ → Fin k → ℚ) (hW : ∀ n : ℤ, evalQ P (Fin.snoc (W (n : ℚ)) (n : ℚ)) = 0) :
    ∀ n : ℤ, ∃ w : Fin k → ℚ, evalQ P (Fin.snoc w (n : ℚ)) = 0 :=
  fun n => ⟨W (n : ℚ), hW n⟩

/-! ### 2. Concrete end-to-end demonstration (2 variables, 1 residual)

Toy residuals, deliberately NAIVE, to exercise the plumbing and the control arm:

  r₀ = X₀ · (X₀ − 1)        (a witness idempotent)
  P  = r₀²

This is the classic first guess — "make the witness idempotent and encode the input
in a residual" — and it is WRONG, which is the point: §4 kills it mechanically.
-/

/-- The toy residual system: `k = 1` witness, `m = 1` residual. -/
noncomputable def toyQuad : Fin 1 → MvPolynomial (Fin 2) ℤ :=
  fun _ => MvPolynomial.X 0 * MvPolynomial.X 0

/-- The toy polynomial `P = r₀²`. -/
noncomputable def toyP : MvPolynomial (Fin 2) ℤ := (toyQuad 0) ^ 2

/-- The structured Tier-1 artifact for the toy: `P` really is the sum of residual squares. -/
noncomputable def toyCert : SosCert where
  k := 1
  m := 1
  P := toyP
  quad := toyQuad
  ident := by
    rw [Fin.sum_univ_one]
    rfl

/-- Tier-1 machinery works on a concrete instance: `P` vanishes iff the residual does. -/
example : ∀ x : Fin 2 → ℚ,
    evalQ toyP x = 0 ↔ ∀ j : Fin 1, evalQ (toyQuad j) x = 0 :=
  fun x => toyCert.evalQ_eq_zero_iff x

/-- And it evaluates concretely: at `X₀ = 0`, `X₁ = q` the residual is zero. -/
example (q : ℚ) : evalQ (toyQuad 0) (Fin.snoc (fun _ => (0 : ℚ)) q) = 0 := by
  rw [evalQ_eq_eval₂, toyQuad]
  simp [MvPolynomial.eval₂_X, MvPolynomial.eval₂_mul, Fin.snoc_castSucc]

/-! ### 3. Evaluating at concrete rational points (the `norm_num` recipe)

The witness `X₀ = 0` makes the toy residual vanish at EVERY input — so the toy would
claim all of ℚ. That is exactly the failure the control arm must catch.
-/

/-- At `X₀ = 0` the toy residual is zero for every input. -/
theorem toyQuad_zero_at_witness_zero (q : ℚ) :
    evalQ (toyQuad 0) (Fin.snoc (fun _ => (0 : ℚ)) q) = 0 := by
  rw [evalQ_eq_eval₂, toyQuad]
  simp [MvPolynomial.eval₂_X, MvPolynomial.eval₂_mul, Fin.snoc_castSucc]

/-! ### 4. THE CONTROL ARM, demonstrated: the naive candidate dies on `q = 1/2`

No arithmetic geometry, no `sorry`, no `native_decide` — a single rational witness
tuple and one non-integer input. This is the trust signal that needs no research. -/

/-- `1/2` is not an integer (the scoring form `q.den = 1`). -/
theorem half_den_ne_one : ((1/2 : ℚ)).den ≠ 1 := by norm_num [Rat.den_eq_one_iff]

/-- The toy candidate does NOT define ℤ: `q = 1/2` is not an integer, yet the residual
system is solvable at it (witness `0`). -/
theorem toy_not_definesZ : ¬ DefinesZ toyCert.k toyCert.P := by
  refine not_definesZ_of_noninteger_residual toyCert (1/2) ?_ (fun _ => 0) ?_
  · exact half_den_ne_one
  · intro j
    exact toyQuad_zero_at_witness_zero (1/2)

end Dzq
