# CERTIFIABILITY — which construction can actually be certified

All Mathlib claims below were verified by `#check` in compiled Lean
(v4.34.1 / Mathlib `d13f23b7`). `ABSENT` means the identifier does not resolve.

---

## Headline

**The mechanical half is COMMON to every mechanism and is now certifiable. The
arithmetic half is missing for all four mechanisms, and no mechanism escapes it.**

Concretely: the sum-of-squares collapse (`sum_sq_eq_zero_iff`, PROVED) reduces
`P(q,w) = 0` to a residual system for **one generic lemma at any arity**. Every
construction of the "P = Σ R_i²" shape therefore reduces to: (i) a transcription
identity `ident`, and (ii) the arithmetic argument on the residuals. (i) is bounded
engineering. (ii) is research-level for all candidates.

So the choice facing the constructions lane is **not** "which mechanism has the
smallest gap" — it is **"which mechanism's arithmetic leaf is smallest"**, and
variable count is a secondary criterion.

## Matrix

| Mechanism | Mathlib readiness | Missing pieces (size) | Verdict |
|---|---|---|---|
| **SoS collapse of a residual system** (any mechanism) | `Finset.sum_eq_zero_iff_of_nonneg` ✓, `sq_nonneg` ✓, `mul_self_eq_zero` ✓ | none. **PROVED in this repo** | **CERTIFIABLE NOW** |
| **Incumbent v4** — elliptic model + height + Selmer + L | `WeierstrassCurve` ✓ `.Δ` ✓ `padicValRat` ✓ `Nat.log2` ✓ `Nat.size` ✓ `Zsqrtd` ✓ | elliptic Selmer over ℚ (XL), L-functions & analytic rank (XL), Néron–Tate heights (XL), Mordell–Weil (XL), curve points/group law (L) | mechanical half certifiable; **arithmetic half blocks the row** |
| **Hasse–Minkowski / local–global** | **ABSENT** — no `HasseMinkowski`, no `IsHassePrinciple` | whole theory of quadratic forms over ℚ, Hilbert symbol (XL) | **worst** — nothing to build on |
| **Universal-polynomial / p-adic definability** | ℚ_p API exists; `padicValRat` ✓ | Hilbert symbol (XL), quaternion algebras over local fields (XL), local–global for conics (XL) | poor |
| **Koenigsmann quadratic forms** | nothing specific | as above, plus the definability machinery (XL) | poor |

### The one nuance that matters for A3

A3 reported "positivity needs exactly 4 squares". Correct, but **not for the collapse.**
The collapse needs only `sq_nonneg` — one square. Four squares are needed to
*represent* a positive rational (`Nat.sum_four_squares` ✓ EXISTS; the `Rat`-level
corollary is ABSENT and is ~S to derive). Two different lemmas; conflating them
overstates the collapse's cost.

---

## What the constructions lane should optimize for

**Optimize for the arithmetic leaf, not the variable count.**

Reasoning:
1. The mechanical half is mechanism-independent and already solved here. A construction
   with 4,973 variables and a 5,000-variable alternative cost the *same* in Tier 1.
2. The board's own leader is 4,973 variables, and the incumbent rows are conditional.
   Beating 4,973 is worth little if the row still carries a Selmer/L-function leaf.
3. A construction whose `HardDirection` reduces to **valuation arguments over ℚ**
   (where `padicValRat` already EXISTS) is dramatically closer to certifiable than one
   needing Selmer coranks or heights. That is the single most valuable discriminator
   available today.
4. Tie-breakers (degree, term count, max coefficient) are mechanical and already
   cheaper than the arithmetic — they should decide between otherwise-equal candidates,
   not drive the choice.

**Recommendation:** rank candidates by *arithmetic-leaf size* first; variable count
second. A slightly worse variable count with a valuation-only converse is the better
row, because it is the only kind of row that can become a verified row.

---

## What a verified row requires, honestly

A sorry-free row needs both:
1. `SosCert` with `ident` discharged by reflection — **engineering, achievable.**
2. `HardDirection` discharged — **research-level arithmetic geometry.**

The harness makes (1) mechanical and makes (2) an explicitly-named, comparable
obligation (`RC_stmt`, `H_is_height_constant`, `PC_derivation`). That is the strongest
honest position: the row's trust reduces to exactly the hypotheses the incumbents
already carry, with nothing hidden and nothing smuggled.

## Priorities for the next session

1. Reflection layer for sparse polynomial data (§1 of GAP_LIST) — turns `ident` from
   intractable elaboration into a `decide`-able comparison. **Bounded, no new math.**
2. Then the arithmetic leaf, mechanism permitting.
