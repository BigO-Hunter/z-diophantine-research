# E_EXC.md — the exceptional set, computed exactly

**Answer: E_exc = {3, 5, 7, 11, 13, 17, 19, 23} — 8 primes. The polynomial's patch set is
E_exc ∪ {2} = 9 primes, because the prescribed S₀ is empty (see §3).**

Nothing here is inherited: `e_exc.py` recomputes the set from Sun's own exclusion rule and from
this lane's freezing parameters, and `e_exc.json` holds the machine record.

## 1. Sun's rule, verbatim

Sun 2026, the paragraph before (5.11) (char ≠ 2, our case):

> "We exclude once for any finite set of places containing the support of π, the poles of the
> elements of Λ and the zeros of all pairwise differences among the four parameters attached to
> each **i**, and all places with |κ_w| ≤ 25."

So, for K = Q (|κ_w| = p):

    E_exc = supp(π) ∪ {poles of Λ} ∪ {zeros of pairwise differences in Λ} ∪ {p ≤ 25}

and everything is taken inside V_K ∖ S with S = {2}.

## 2. The freezing parameters this lane uses

The local cover of P₂ has two closed-open classes, and — as required by Sun — **four** parameters
per class (so that at every place four residues are available and only three of them can be in
{0, ±1}):

| class | set | parameters | why they work |
|---|---|---|---|
| A | v₂(c) ≤ 2  (c ≢ 0 mod 8) | **1, 17, 33, 49**  (≡ 1 mod 16) | δ = 1−Aτ² has δ/4 ≡ 7 mod 8, which makes w = (c²−16/δ)/A a square for c odd and gives v(w) = 3 for v(c) = 1 |
| B | v₂(c) ≥ 2  (c ≡ 0 mod 4) | **3, 11, 19, 27**  (≡ 3 mod 8) | δ/4 ≡ 1 or 5 mod 8, so the obstruction class u ≡ 5 never occurs |

Machine checks:

* each of the eight serves its whole class, exhaustively over a ≡ odd mod 2⁹ and c mod 2⁹
  (`e_exc.py`, `SMOKE2.md §4`): **0 obstructions in 114,688 (class A) and 32,768 (class B) points**;
* the derivation lane's single parameter set (τ ≡ t_p mod 8) is *not* usable: it is 100 %
  obstructed for c ≡ 0 mod 8 — that is `VERIFICATION.md §3`'s refutation.

## 3. Computing the four contributions

**supp(π) = {2}.** π = 2 for S = {2}. Inside V_K ∖ S this contributes ∅.

**Poles of Λ.** All eight parameters are integers. ∅.

**Zeros of pairwise differences.** Within class A the differences are 16, 32, 48; within class B
they are 8, 16, 24. Primes involved: {2, 3}. (Cross-class differences also give {5,7,11,13,19,23} —
all already excluded below, and in any case Sun's exclusion is per cell, i.e. within a class.)
So this contributes {3}, which is already forced.

**|κ_w| ≤ 25.** Lemma 5.1's hypothesis is |κ| = q > 25, so every place with q ≤ 25 is excluded:
{2,3,5,7,11,13,17,19,23}, minus S = {2} ⟹ **{3, 5, 7, 11, 13, 17, 19, 23}**.

**Union.** E_exc = {3,5,7,11,13,17,19,23}; the τ-divisor contributions add nothing new. So

    |E_exc| = 8,  E_exc = {3,5,7,11,13,17,19,23}.

The bound does **not** grow with Λ: the eight are forced by the residue-field bound alone, and a
larger Λ can only *add* to the difference set — with the arithmetic-progression lifts above even
the differences stay inside {2,3}. Under the derivation lane's rule the extra term was
"Σ_τ #prime divisors of τ(τ²−1)"; with these eight parameters that sum is empty, so the earlier
"8 + Σ…" collapses to exactly 8.

## 4. Residue conditions verified outside E_exc

For every prime w ≤ 3000 with w ∉ E_exc, both classes have four pairwise distinct residues and at
least one of them lies outside {0, ±1} (`e_exc.py` §c): **no failures**. Beyond 3000 the pigeonhole
argument takes over — four distinct residues, three forbidden values.

## 5. Why the patch set is E_exc ∪ {2}

The polynomial defines ⋃_{w ∈ V_K ∖ S₀} m_w. The target Q ∖ Z = {X : 1/X ∈ ⋃_{all w} m_w}
fixes the prescribed set S₀ = **∅**, while the freezing construction runs with S = {2} (Daans
Thm 5.6's enlargement). Sun's return step (9.4) then adjoins the missing places:

    ⋃_{w∉S₀} m_w = (⋃_{w∉S} m_w) ∪ (⋃_{v∈S∖S₀} m_v),   S∖S₀ = {2}  ⟹  m_2 is adjoined.

So the patch is applied at **9** primes: {2} ∪ E_exc. That the p = 2 factor is genuinely needed is
not a convention — `SMOKE2.md §3` measures it: X = 3/10 has v₂ = −1, and its patch factors are
solvable at exactly {2, 5}; without the p = 2 member the polynomial would miss 3/10.

## 6. Files

| file | content |
|---|---|
| `e_exc.py` | recomputes E_exc from Sun's rule; verifies the 8 parameters serve their classes; scans residues to 3000 |
| `e_exc.json` | machine record (sha256 `dc523137e3d4e12bddeb2c44876011f911f9b123497a7727a3c89cfe25810b3a`) |
| `perprime.json` | the per-prime constants and the checks for all nine primes (`PER_PRIME.md`) |
