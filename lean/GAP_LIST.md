# GAP_LIST — what Mathlib already has vs what the v4 certificate needs

**Every "EXISTS" below was checked by `#check` in a compiled Lean file, not inferred.**
Toolchain: `leanprover/lean4:v4.34.1`, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`
(the staircase-port campaign's built Mathlib, reused by path dependency — no rebuild).

Status of the harness in this directory: **COMPILED, zero `sorry`**
(`lake build` → *1387 jobs, Build completed successfully*).

---

## §0. What is DONE (Tier 1 — mechanical half, kernel-checked)

| Item | Status |
|---|---|
| `evalQ` / `DefinesZ` / `ZDiophantineInQWithin` mirrored from the gate lane | COMPILED |
| Bridge `q ∈ Set.range (Int.cast) ↔ q.den = 1` (`mem_range_intCast_iff_den_eq_one`) | PROVED |
| **Sum-of-squares collapse** `sum_sq_eq_zero_iff`, `sum_sq_eq_zero_iff_fin` | **PROVED** |
| `SosCert` structure + `SosCert.evalQ_eq_zero_iff` (P vanishes ⟺ residual system vanishes) | PROVED |
| `SosCert.exists_witness_iff` (witness sets coincide) | PROVED |
| `DefinesZ.of_sos` (easy + hard direction ⇒ race property) | PROVED |
| `easyDirection_of_witnessFamily` (easy half reduced to one witness family) | PROVED |
| Control arm `not_definesZ_of_noninteger_witness` / `..._residual` | PROVED |
| Control arm **demonstrated end-to-end** killing a naive candidate at `q = 1/2` | PROVED |
| Conditional frame `RC_stmt`, `H_is_height_constant`, `PC_derivation`, `QuarticCertificate` | COMPILED |
| `v4_collapse` — collapse instantiated at the v4 shape (4,552 residuals) | PROVED |

The collapse is **one generic lemma, O(1) in residual count** — the 4,552 is not a
proof-length parameter. This is the tractable core, and it is done.

### The collapse, direction by direction (both checked)

* each `= 0` ⇒ sum `= 0`: `Finset.sum_eq_zero`-style, no order used.
* sum `= 0` ⇒ each `= 0`: needs positivity only. `Finset.sum_eq_zero_iff_of_nonneg`
  (EXISTS, signature confirmed: `[AddCommMonoid N] [PartialOrder N] [IsOrderedAddMonoid N]`,
  `(∀ i ∈ s, 0 ≤ f i) → (∑ f = 0 ↔ ∀ i ∈ s, f i = 0)`) + `sq_nonneg` + `mul_self_eq_zero`.
  **One square suffices — four squares are NOT needed here.** A3's "positivity needs
  exactly 4 squares" is a different fact (Lagrange: representing a positive rational as
  a sum of four squares, `Nat.sum_four_squares` EXISTS). It is not used by the collapse.

### The rational-vs-integer subtlety (resolved, no gap)

Coefficients are `ℤ` (`P : MvPolynomial (Fin (k+1)) ℤ`), vanishing is over `ℚ`. No
subtlety arises: `MvPolynomial.eval₂ (Int.castRingHom ℚ) x` is a ring hom into `ℚ`, so
integer coefficients simply cast, and the collapse lives entirely in `ℚ`'s order. The
only real subtlety is that **sums of squares give no discreteness over ℚ** — see §3.

---

## §1. Tier 1 remaining: the transcription (`SosCert.ident`)

The one size-dependent obligation is `ident : P = ∑ j, (quad j)^2`.

**Do not elaborate 72,925 terms as an `MvPolynomial` expression.** Each term needs
monomial construction, `Finsupp` allocation, and instance synthesis in a
`Fin 4973`-indexed context; cost compounds superlinearly and the campaign's own datum
(a single 36-digit literal kernel-checks in ~176 s) is a *tiny* kernel term by
comparison. **ESTIMATE (not measured): expression-mode elaboration of the full quartic
is hours-to-days and memory-risky — not an interactive artifact.**

Recommended architecture (reflection, not expansion):
1. Store the polynomial as **sparse data**: `List (List (ℕ × ℕ) × ℤ)` — per term, a
   sorted `(variable-index, exponent)` list plus the coefficient. ~450 K pairs total.
2. Store the residual system the same way.
3. Prove one **generic** evaluator lemma: the sparse representation evaluates to the
   same value as `evalQ`. Then `ident` becomes a `decide`-able comparison of two
   sorted coefficient lists, not a 72,925-term proof.
4. Kernel-check the comparison. **ESTIMATE (not measured): tractable** — the data is
   ~1–2 MB and the comparison is ~10⁶ operations, well inside `native_decide`/
   `decide` budgets, unlike expression elaboration.

`Fin 4973` itself is fine: `Fin n` for large `n` is a lightweight subtype, and the
collapse lemma never enumerates it. What breaks is term *construction*, not the arity.

**Gap size: S (design + ~200 lines of reflection plumbing). No new mathematics.**

### The big constant `H* = 2(4608^165888 + 6^100)·B_*^24 + 128`

`log₂ H* < 4,783,227` ⇒ the literal has ~1.44 M decimal digits. **Do not write the
literal.** Keep the expression form (`Nat` exponentiation is lazy: `4608^165888` is a
term, not an expansion) and state the bound with `Nat.log2` (EXISTS) / `Nat.size`
(EXISTS). Comparisons are then computations, not elaborations. Guidance only —
**UNVERIFIED by measurement**; the harness does not yet contain a compile-time test.

---

## §2. Arithmetic half — per-ingredient gap (the `HardDirection` obligation)

The certificate stops at `HardDirection`. Here is exactly what blocks formalizing it.

| v4 ingredient | Mathlib status (checked) | Gap |
|---|---|---|
| `hyp:RC` — 2-power Selmer corank over ℚ | `SelmerGroup` exists only as `Mathlib/RingTheory/DedekindDomain/SelmerGroup.lean` — the **algebraic** `K*/(K*)^n` Selmer group, NOT the elliptic-curve Selmer group. No `SelmerGroup` over `ℚ` for `E_ℓ`. | **XL** |
| `L(E_ℓ, s)` and `ord_{s=1}` | No L-functions, no analytic rank. | **XL** |
| `H_is_height_constant` — six-contact estimate | No canonical/Néron–Tate height (`canonicalHeight`, `NeronTate`: ABSENT). | **XL** |
| Elliptic curve object | `WeierstrassCurve` EXISTS, `.Δ` EXISTS (`@WeierstrassCurve.Δ : [CommRing R] → WeierstrassCurve R → R`). `.Point` and `.nonsingular` **not found under those names** (UNVERIFIED whether renamed) — no group-law API located. | **L** (points/group law) |
| `lem:pole` — p-adic valuation argument | `padicValRat : ℕ → ℚ → ℤ` **EXISTS**. Valuation on ℚ is available; what is missing is the elliptic model it is applied to. | **M** |
| `Q(√2)` (ingredient G) | `Zsqrtd : ℤ → Type` EXISTS (ℤ[√2]). No `QuadraticField`. Field-of-fractions layer must be built. | **M** |
| Mordell–Weil / rank | `MordellWeil`, `Rank`: **ABSENT**. | **XL** |
| `Squarefree` (for `ℓ`) | `IsSquarefree` ABSENT as a root name; likely `Squarefree` — **UNVERIFIED**. | **S** (verify) |
| Hasse–Minkowski (for other mechanisms) | **ABSENT** (`HasseMinkowski`, `IsHassePrinciple`, `hilbertSymbol` all absent). | **XL** |
| Four squares (Lagrange) | `Nat.sum_four_squares` EXISTS. `Rat.sum_four_squares`, `Rat.exists_eq_sum_four_squares`: **ABSENT** (would need deriving from the `Nat` version). | **S** |

---

## §3. A structural obstruction worth recording

Over ℚ every non-negative rational is a sum of four squares, so **any** candidate built
on "q is a sum of squares" defines all of ℚ≥0, never ℤ. There is no ordering-based
discreteness available over ℚ. This is why every real mechanism must be arithmetic
(valuations, Selmer groups, heights) and why the arithmetic half is irreducible. It is
also why the `sum_sq_eq_zero_iff` collapse is a *syntactic* tool (residual-system
equivalence) and not a *defining* one (it cannot manufacture discreteness).

---

## §4. Gate-lane item: `Statement.lean` typecheck

`diophantine-zq/Statement.lean` was labelled NOT-COMPILED. Against v4.34.1 + Mathlib
d13f23b7 it has **exactly one error**:

```
Statement.lean:36:23: error: Unknown constant `MvPolynomial.map`
```

Cause: `import Mathlib.Algebra.MvPolynomial.Basic` does not provide `MvPolynomial.map`.
**Fix: add `import Mathlib.Algebra.MvPolynomial.Eval`.** With that single import added,
the file compiles clean (`lake env lean Statement_fixed.lean` → exit 0, no output).
Everything else in it — `Fin.snoc`, `Set.range`, both definitions — is correct.
