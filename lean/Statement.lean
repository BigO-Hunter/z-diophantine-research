/-
Statement.lean — trusted-statement DRAFT for the bigospeedrun race
"Z is Diophantine in Q" (row z-diophantine-in-q).

Pattern follows darkhipo/omr-statement (the #145 house pattern):
explicit binders, `autoImplicit false`, no `sorry`, definitions transcribed
from the race statement. NOT COMPILED — no Lean/Mathlib toolchain was run
in this window; the marking below is honest. Every non-definitional claim
about the incumbents lives in DESIGN.md, not here (it cannot be proven
without their construction).

Verbatim race statement being transcribed
(https://bigospeedrun.com/other/z-diophantine-in-q, 2026-11-06):

  "A polynomial P(q,w_1,…,w_k) with integer coefficients defines Z in Q
   when, for every rational number q, q is an integer exactly when
   P(q,w_1,…,w_k)=0 for some rational numbers w_1,…,w_k. ...
   The score is the number of variables, k+1. Fewer variables rank
   higher; on a tie, a lower degree ranks higher, then fewer nonzero
   terms, then a smaller largest absolute coefficient."

Conventions fixed here (documented, since the race statement does not fix
them): the input `q` is the LAST argument of the variable vector
(`Fin.snoc w q`); witness variables are indexed `Fin k`. Variable order
does not affect the property, only the transcription.
-/

import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.Algebra.MvPolynomial.Eval

set_option autoImplicit false

/-- `P` with integer coefficients in `k+1` variables, evaluated at rational
points through the canonical map ℤ → ℚ. -/
noncomputable def evalQ {k : ℕ} (P : MvPolynomial (Fin (k + 1)) ℤ)
    (x : Fin (k + 1) → ℚ) : ℚ :=
  MvPolynomial.eval x (MvPolynomial.map (Int.castRingHom ℚ) P)

/-- `P` defines ℤ in ℚ with `k` witness variables (`k + 1` total): for every
rational `q`, `q` is an integer iff some rational witness tuple makes `P`
vanish. This is the race's defining property, verbatim in structure. -/
def DefinesZ (k : ℕ) (P : MvPolynomial (Fin (k + 1)) ℤ) : Prop :=
  ∀ q : ℚ,
    (q ∈ Set.range fun n : ℤ => (n : ℚ)) ↔
      ∃ w : Fin k → ℚ, evalQ P (Fin.snoc w q) = 0

/-- The race score gate: ℤ is Diophantine in ℚ using at most `n` total
variables. Lower `n` is better; ties break on degree, then nonzero terms,
then largest absolute coefficient (recorded on the score function of the
polynomial, not needed to state the gate). -/
def ZDiophantineInQWithin (n : ℕ) : Prop :=
  ∃ k : ℕ, k + 1 ≤ n ∧ ∃ P : MvPolynomial (Fin (k + 1)) ℤ, DefinesZ k P

/- ### Explicit row adapters (targets, NOT proven here)

The incumbent rows on the race page are exactly these instances. None is
proven in this draft — proving one requires that row's explicit polynomial
AND its arithmetic argument, which is precisely the incumbents' unfinished
work (their Lean main declaration still has `sorry`). They are recorded as
documentation, not as `theorem` declarations, so this file carries no
`sorry`:

  ZDiophantineInQWithin 4973    -- quartic v4, release quartic-4973-version-4 (Nov 6 15:49Z)
  ZDiophantineInQWithin 9625    -- quartic v3, release quartic-9625-version-3 (Nov 6 14:17Z)
  ZDiophantineInQWithin 12504   -- quartic v2, release quartic-12504-version-2 (Nov 6 02:59Z)
  ZDiophantineInQWithin 211983774909  -- qqwref PR #1 (Nov 5 23:50Z)
  ZDiophantineInQWithin 292890231905  -- Glazer agent breakthrough (Nov 4 19:50Z)
-/
