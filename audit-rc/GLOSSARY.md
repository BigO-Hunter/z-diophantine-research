# GLOSSARY — hypothesis names → plain math (quartic_4973.tex)

- **Board problem (z-diophantine-in-q)**: find P(q,w₁,…,w_k) ∈ Z[q,w] with, for every q ∈ Q:
  q ∈ Z ⟺ ∃w ∈ Qᵏ P(q,w)=0. Score k+1; lower wins. Leader: quartic-4973-version-4
  (k=4,972, degree 4, 72,925 monomials).
- **`hyp:RC` (Restricted converse, line 1020)**: for every squarefree ℓ ≡ 11 (mod 12), the
  elliptic curve E_ℓ: y² = x(x−ℓ)(x+3ℓ) (a quadratic twist of j = 35152/9, non-CM) satisfies:
  IF the 2-primary Selmer group has Z₂-corank 1 THEN the L-function L(E_ℓ,s) vanishes at s=1 to
  order exactly 1. Why nontrivial: corank 1 is an ALGEBRAIC upper-bound statement (Kummer:
  rank + Sha-corank = 1); parity (Dokchitser–Dokchitser Thm 1.8, a theorem) gives root number −1,
  hence ord L odd (1 or 3 or 5…). Concluding EXACTLY 1 needs a bound on the ANALYTIC side — the
  Gross–Zagier/Kolyvagin circle, or a substitute. Their substitute: the (O.8) device below.
- **`hyp:PC` (Pole completeness, 1016)**: a completeness statement for the pole predicate Φ(B):
  rational B with square reduced denominator, 0<B<1/2, v_p(B)≥4 at all bad primes ⟹ Φ(B) holds.
  Proved (1032–1136) by 2-Selmer dimension bookkeeping plus TWO applications of hyp:RC. Inherits
  RC's gap.
- **`lem:pole` (One-sided obstruction, 1004)**: soundness of the pole test — if B≠0 and Φ(B),
  then v_p(B) is never negative-odd outside S₀. Short, independently checkable.
- **(O.8) "visibility implication" (display tag 13084, Prop ex:app-visibility)**: for twists E^D:
  if the 2-adic valuation of the precision-M modular-symbol/theta coefficient a_M(D) is < M
  (i.e. the coefficient is nonzero at precision M), then ord_{s=1} L(E^D,s) = 1 and the "native
  genus index" j_gen(D) ≤ v₂a_M(D)+C_det. THIS is what converts 2-adic bookkeeping into analytic
  rank 1. Proof rests on (O.7), a "rank-one free lattice", and one asserted clause; uncited,
  unpublished, unreviewed. Load-bearing for all of hyp:RC.
- **Ultrafilter framework**: the RC chain takes limits of coefficient-stage matrices over
  Λ = Z₂[[t]] along a FIXED NONPRINCIPAL ULTRAFILTER (lines 2557, 4418, 4459, 4696, 4836, 13801)
  to obtain exact identities; nonstandard, appears in no cited source.
- **`lem:forward-rank` (1093–1113)**: the honest, classical piece — IF ord L ≤ 1 THEN rank = ord
  and Sha finite (BCDT modularity + Kolyvagin Thm 1 + Kato Cor 14.3). Used AFTER RC to convert
  analytic rank 1 into witnesses. Note direction: it cannot prove RC; RC needs algebraic ⟹ analytic.
- **`hyp:o8-height` (five-contact height estimate, 6670)**: h(a) ≤ H_*·M₅(a)²⁴, where M₅(a)
  measures odd contact of (a:1) with {∞,0,1,2401,−343/32} outside S_* = primes ≤ 76176, and
  log₂H_* < 4,783,227. Converts the ∀ over contact primes into a finite box (the ∀-elimination).
  Claimed proof: Shimura curve of discriminant 210 (g=5), Atkin–Lehner quotients (~800 lines).
  Authors' own caveats at 6645 and 7500 (see SEAMS.md).
- **`thm:quartic-height19` (8738)**: sharpened exponent-19 version (log₂H₁₉ < 2,093,966) reused by
  the quartic stage via sec:v4-inherited.
- **"With precisely the inherited arithmetic hypotheses and qualifications" (8691)**: the quartic
  theorem's own conditional clause — the polynomial identity and certificate are finite and
  checked; the ARITHMETIC characterization of Z comes from the earlier claimed theorems
  (RC, PC, height, prime-pattern, formal group), retained with their proof status (9117–9205).
  Encoded in Lean as the `sorry` on the main declaration (README, "Verification status").
- **Selmer corank / parity**: Sel_{2^∞}(E/Q) is a cofinitely generated Z₂-module; its corank
  equals rank E(Q) + corank Sha[2^∞] (Cassels). Parity theorem: corank odd ⟺ root number −1.
