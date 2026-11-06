/-
Scaff.lean — generic certificate skeleton for the race row
`z-diophantine-in-q` ("Z is Diophantine in Q").

AUTHORITY / NON-DUPLICATION
The board statement itself (`evalQ`, `DefinesZ`, `ZDiophantineInQWithin`) is owned by
the gate lane in `diophantine-zq/Statement.lean`. The two definitions below are
MIRRORED VERBATIM from it so this harness can be typechecked standalone; if that file
changes, re-sync. The convention there — and therefore here — is
`Fin.snoc w q`: witnesses occupy `Fin k`, the input `q` is the LAST coordinate.

DESIGN: TWO TIERS
  Tier 1 (MECHANICAL, certifiable today):
    P is a sum of squares of residual polynomials. Then
        evalQ P x = 0  ↔  every residual vanishes at x
    over ℚ, because ℚ is an ordered field and a sum of squares of rationals is
    zero iff each term is. THAT IS ONE GENERIC LEMMA (`sum_sq_eq_zero_iff` below),
    applied to any number of residuals — NOT 4,552 per-residual proofs.
    The only per-construction obligation in Tier 1 is the single polynomial
    identity `P = ∑ quad j ^ 2`, which is a coefficient comparison and is
    meant to be checked by reflection (see GAP_LIST.md §Tier-1), never by
    hand-expanding a 72,925-term `MvPolynomial` expression.

  Tier 2 (ARITHMETIC, research-level): named hypotheses `h_easy` / `h_hard`.
    Nothing here pretends to prove them.

STATUS: every declaration in this file is checked by the Lean kernel.
Toolchain: leanprover/lean4 v4.34.1, Mathlib d13f23b7 (see lean-toolchain + lakefile).
-/

import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.MvPolynomial.Equiv
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

set_option autoImplicit false

namespace Dzq

/-! ### 1. The board statement (mirrored from the gate lane) -/

/-- `P` with integer coefficients in `k + 1` variables, evaluated at rational points
through the canonical map ℤ → ℚ. Mirrored verbatim from
`diophantine-zq/Statement.lean`. -/
noncomputable def evalQ {k : ℕ} (P : MvPolynomial (Fin (k + 1)) ℤ)
    (x : Fin (k + 1) → ℚ) : ℚ :=
  MvPolynomial.eval x (MvPolynomial.map (Int.castRingHom ℚ) P)

/-- `P` defines ℤ in ℚ using `k` witness variables (`k + 1` total). Race-defining
property, mirrored verbatim. -/
def DefinesZ (k : ℕ) (P : MvPolynomial (Fin (k + 1)) ℤ) : Prop :=
  ∀ q : ℚ,
    (q ∈ Set.range fun n : ℤ => (n : ℚ)) ↔
      ∃ w : Fin k → ℚ, evalQ P (Fin.snoc w q) = 0

/-- The race score gate. Fewer total variables is better. -/
def ZDiophantineInQWithin (n : ℕ) : Prop :=
  ∃ k : ℕ, k + 1 ≤ n ∧ ∃ P : MvPolynomial (Fin (k + 1)) ℤ, DefinesZ k P

/-! ### 2. Evaluation as a ring homomorphism — the calculation form

`evalQ` is written in the gate lane's `eval ∘ map` shape. For pushing through sums
and powers we use the equivalent `eval₂Hom`, bridged by
`MvPolynomial.eval₂_eq_eval_map`. -/

/-- `evalQ` in `eval₂` form, via `MvPolynomial.eval₂_eq_eval_map`. -/
theorem evalQ_eq_eval₂ {k : ℕ} (P : MvPolynomial (Fin (k + 1)) ℤ)
    (x : Fin (k + 1) → ℚ) :
    evalQ P x = MvPolynomial.eval₂ (Int.castRingHom ℚ) x P := by
  rw [evalQ, ← MvPolynomial.eval₂_eq_eval_map]

theorem evalQ_sum {k m : ℕ} (Q : Fin m → MvPolynomial (Fin (k + 1)) ℤ)
    (x : Fin (k + 1) → ℚ) :
    evalQ (∑ j, Q j) x = ∑ j, evalQ (Q j) x := by
  rw [evalQ_eq_eval₂, MvPolynomial.eval₂_sum]
  exact Finset.sum_congr rfl fun j _ => (evalQ_eq_eval₂ (Q j) x).symm

theorem evalQ_pow {k : ℕ} (Q : MvPolynomial (Fin (k + 1)) ℤ)
    (x : Fin (k + 1) → ℚ) (n : ℕ) :
    evalQ (Q ^ n) x = evalQ Q x ^ n := by
  rw [evalQ_eq_eval₂, evalQ_eq_eval₂, MvPolynomial.eval₂_pow]

/-! ### 3. `q ∈ ℤ` in the board's two equivalent forms

The race SCORE is stated with `q.den = 1`; the gate lane's `DefinesZ` states it as
`q ∈ Set.range (Int.cast)`. These are equivalent, and the bridge is what lets the
scoring form and the statement form be used interchangeably. -/

theorem mem_range_intCast_iff_den_eq_one (q : ℚ) :
    (q ∈ Set.range fun n : ℤ => (n : ℚ)) ↔ q.den = 1 := by
  constructor
  · rintro ⟨n, rfl⟩
    exact Rat.den_intCast n
  · intro h
    exact ⟨q.num, (Rat.den_eq_one_iff q).mp h⟩

/-! ### 4. TIER 1 CORE — the sum-of-squares collapse (one lemma, any arity)

Over ℚ every square is nonnegative, so a finite sum of squares vanishes iff every
term does. This is the whole mathematical content of the "4,552 residuals collapsed
by summing squares" step: it needs NO arithmetic geometry and no per-residual work.
`m` is the number of residuals and is unconstrained — 4,552 or 4,552,000. -/

theorem sum_sq_eq_zero_iff {ι : Type*} (s : Finset ι) (f : ι → ℚ) :
    (∑ i ∈ s, (f i) ^ 2 = 0) ↔ ∀ i ∈ s, f i = 0 := by
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => sq_nonneg (f i))]
  exact ⟨fun h i hi => by
          have h2 : f i * f i = 0 := by simpa [pow_two] using h i hi
          exact mul_self_eq_zero.mp h2,
         fun h i hi => by simp [h i hi]⟩

/-- Unindexed form over `Fin m`: the one actually applied to a residual system. -/
theorem sum_sq_eq_zero_iff_fin {m : ℕ} (f : Fin m → ℚ) :
    (∑ i, (f i) ^ 2 = 0) ↔ ∀ i, f i = 0 := by
  simpa using sum_sq_eq_zero_iff Finset.univ f

/-! ### 5. The structured Tier-1 artifact

A 72,925-term quartic over 4,973 variables cannot be elaborated as an `MvPolynomial`
expression (see GAP_LIST.md §Tier-1 for the sizing argument). The artifact is
therefore STRUCTURED: the residual system plus the single identity relating it to `P`.
`ident` is the one obligation a transcriber must discharge; everything else is generic. -/

/-- A sum-of-squares certificate: `P` is the sum of the squares of `m` residuals. -/
structure SosCert where
  /-- number of witness variables -/
  k : ℕ
  /-- number of residual polynomials -/
  m : ℕ
  /-- the race polynomial, `k + 1` variables -/
  P : MvPolynomial (Fin (k + 1)) ℤ
  /-- the residual system -/
  quad : Fin m → MvPolynomial (Fin (k + 1)) ℤ
  /-- THE TIER-1 OBLIGATION: `P` is exactly the sum of squared residuals.
  A coefficient identity — check by reflection, not by expansion. -/
  ident : P = ∑ j, (quad j) ^ 2

/-- **Tier-1 theorem (the partial certificate).** Given the SoS identity, `P` vanishes
at a rational point iff the whole residual system vanishes there. This is sorry-free
and generic: it is the same proof for every construction and every arity. -/
theorem SosCert.evalQ_eq_zero_iff (C : SosCert) (x : Fin (C.k + 1) → ℚ) :
    evalQ C.P x = 0 ↔ ∀ j : Fin C.m, evalQ (C.quad j) x = 0 := by
  rw [C.ident, evalQ_sum]
  have hsquare : ∀ j : Fin C.m, evalQ (C.quad j ^ 2) x = (evalQ (C.quad j) x) ^ 2 :=
    fun j => evalQ_pow (C.quad j) x 2
  simp only [hsquare]
  exact sum_sq_eq_zero_iff_fin fun j => evalQ (C.quad j) x

/-- Witness-level form of the Tier-1 theorem: solution sets of `P` and of the residual
system coincide, `q` included. -/
theorem SosCert.exists_witness_iff (C : SosCert) (q : ℚ) :
    (∃ w : Fin C.k → ℚ, evalQ C.P (Fin.snoc w q) = 0) ↔
      ∃ w : Fin C.k → ℚ, ∀ j : Fin C.m, evalQ (C.quad j) (Fin.snoc w q) = 0 := by
  constructor
  · rintro ⟨w, hw⟩
    exact ⟨w, (C.evalQ_eq_zero_iff _).mp hw⟩
  · rintro ⟨w, hw⟩
    exact ⟨w, (C.evalQ_eq_zero_iff _).mpr hw⟩

/-! ### 6. TIER 2 — the arithmetic half, as named hypotheses

Both directions are stated against `SosCert`'s residual system, so the arithmetic
lane can target the residuals rather than a 72,925-term polynomial. `h_hard` is the
research-level statement (elliptic model / height / pole predicate — see GAP_LIST.md
§Arithmetic). Nothing in this section is proven; that is the point. -/

/-- Easy direction: every integer has a rational witness tuple. For any concrete
construction this is a term-mode existence — see `EasyDirection.lean` for the pattern. -/
def EasyDirection (C : SosCert) : Prop :=
  ∀ n : ℤ, ∃ w : Fin C.k → ℚ, evalQ C.P (Fin.snoc w (n : ℚ)) = 0

/-- Hard direction: a rational witness tuple forces the input to be an integer.
Stated in residual form so the arithmetic lane never touches `P` directly. -/
def HardDirection (C : SosCert) : Prop :=
  ∀ q : ℚ, (∃ w : Fin C.k → ℚ, ∀ j : Fin C.m, evalQ (C.quad j) (Fin.snoc w q) = 0) →
    q.den = 1

/-- Bridge: `HardDirection` in residual form implies it in `P` form. -/
theorem hardDirection_P (C : SosCert) (h : HardDirection C) :
    ∀ q : ℚ, (∃ w : Fin C.k → ℚ, evalQ C.P (Fin.snoc w q) = 0) → q.den = 1 := by
  intro q hq
  exact h q ((C.exists_witness_iff q).mp hq)

/-- **The assembled certificate.** Both directions supplied, the race property follows.
This is the exact shape a submission must fill: two named hypotheses. -/
theorem DefinesZ.of_sos (C : SosCert) (h_easy : EasyDirection C) (h_hard : HardDirection C) :
    DefinesZ C.k C.P := by
  intro q
  rw [mem_range_intCast_iff_den_eq_one]
  constructor
  · intro hq
    have hq' : (q.num : ℚ) = q := (Rat.den_eq_one_iff q).mp hq
    obtain ⟨w, hw⟩ := h_easy q.num
    exact ⟨w, by simpa [hq'] using hw⟩
  · rintro ⟨w, hw⟩
    exact hardDirection_P C h_hard q ⟨w, hw⟩

/-! ### 7. The CONTROL ARM — refuting a candidate in one line of arithmetic

A wrong candidate is killed by a single explicit witness for a single non-integer
input. This is fully mechanical (`norm_num`), costs no arithmetic geometry, and is
the cheapest trust signal available: it is what stops a plausible-looking
construction from being believed. -/

/-- If a non-integer `q` admits a witness tuple, `P` does NOT define ℤ. -/
theorem not_definesZ_of_noninteger_witness {k : ℕ}
    (P : MvPolynomial (Fin (k + 1)) ℤ) (q : ℚ) (hq : q.den ≠ 1)
    (w : Fin k → ℚ) (hw : evalQ P (Fin.snoc w q) = 0) :
    ¬ DefinesZ k P := by
  intro h
  exact hq ((mem_range_intCast_iff_den_eq_one q).mp ((h q).mpr ⟨w, hw⟩))

/-- Same, in the residual form: one witness solving the residual system at a
non-integer kills the candidate. -/
theorem not_definesZ_of_noninteger_residual (C : SosCert) (q : ℚ) (hq : q.den ≠ 1)
    (w : Fin C.k → ℚ) (hw : ∀ j : Fin C.m, evalQ (C.quad j) (Fin.snoc w q) = 0) :
    ¬ DefinesZ C.k C.P :=
  not_definesZ_of_noninteger_witness C.P q hq w ((C.evalQ_eq_zero_iff _).mpr hw)

end Dzq
