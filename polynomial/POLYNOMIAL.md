# POLYNOMIAL.md — the explicit artifact (recipe; constants now computed/bounded — G1_FREEZING.md)

Target theorem (all quantifiers over Q):

> There are constants c₁,…,c_M ∈ Z (listed in §5, all effectively computable, none yet computed)
> and a polynomial **F ∈ Z[X, a, b, b₁, σ, υ, y, r, s, ζ, ζ′, ι]** — 11 quantified variables —
> such that for every X ∈ Q:
>
> **X ∉ Z ⟺ F(X, a, b, b₁, σ, υ, y, r, s, ζ, ζ′, ι) = 0 has a rational solution.**
>
> With the non-constructive collapse of Daans Prop 2.2 / DDF Cor 4.12 / DDF Thm 1.4 (published,
> unconditional) the same set is defined by one polynomial in **7** unknowns (Sun 2026, Thm 1.1).

The 11-variable F below is *constructive*: every fold is an ordered-field identity, every set
equality is verified in §3, so Sun's proofs apply verbatim. Status: **recipe** — writing F down
as integer coefficients requires only the constants of §5.

## 1. Constants — status after the 2026-11-06 continuation (details: G1_FREEZING.md, G2_REDERIVATION.md)

- **S = {2}, u = 1, π = 2 — EXACT, verified** (properties (i)–(iii) of Daans Thm 5.6 hold;
  X²−X−1 irreducible over Q₂). Π_S = 2; Φ_u^S = {(a,b) : b ∈ Z₂^×, a odd}.
- **Patch constants for p = 2 — EXACT**: Q = [1,2)_Q ≅ (5,2)_Q, ΔQ = {2,5}, π₄ = 10, 𝔞 = 8;
  the explicit ∃₃ formula for Z_(2) is written in G2_REDERIVATION.md §1. Other patch primes:
  same template, per-prime finite search (not yet executed).
- **Λ — EXACT: Λ = {1, 3}**, dispatch rule *τ = 1 unless c ≡ 0 mod 4, τ = 3 if c ≡ 0 mod 4*
  (executor-proved digit-independent case analysis + machine-verified: 0/524,288 grid,
  0/60,000 deep-random, 2000/2000 explicit witnesses). **[Correction: the earlier cell-bound
  |Λ| ≤ 512 is stricken — refuted derivation, see G1_FREEZING.md §3/§6.]**
- **E_exc — bounded and computable** from Λ: ⊇ {primes ≤ 25} ∖ {2}, plus the prime divisors
  of τ(τ²−1) per τ; finite; per-prime patch constants by the §1-template search.

## 2. The polynomial, branch by branch

Quantified variables: a, b (quaternion parameters); b₁, σ, υ (Φ); y, r, s (Θ witnesses);
ζ, ζ′ (inequation witnesses); ι (X ≠ 0 witness). Plus X.

**(i) Quaternion parameters and the trace-sum branch (Sun (2.1), char≠2, per τ ∈ Λ):**

    A      := 1 + 4a²
    δ_τ    := 1 − A·τ²                    (τ constant ⇒ δ_τ(a) polynomial in a)
    z      := X³
    G      := 16a⁴b² − (b−1)⁴·(1+4a²)      [so g(a,b) = G/((1+4a²)b²), Daans Lemma 5.3 / Sun (9.1)]
    N      := a²·z²·G
    D      := (1+4a²)·b²·(1 − z − a²z²)    [so c := h(a,b,X³) = N/D as a term, 0⁻¹=0 semantics]
    P̂_τ    := δ_τ·(N² − A·y²·D²) − 16·(b·π)·(r² − A·s²)·D² − 16·D²      [= D²·P_τ]
    P₀_τ   := −δ_τ·A·y² − 16·(b·π)·(r² − A·s²) − 16                      [= P_τ at c := 0]

**(ii) Φ_u^S (Daans Lemma 5.2, explicit shape — self-contained, valuation-verifiable):**

    F_Φ := (b·b₁ − 1 − σ·Π_S)² + (a − u − υ·Π_S)²

(b ∈ ⋂_{p∈S}O_p^× ⟺ ∃b₁,σ: bb₁ − 1 = σ·Π_S;  a ≡ u mod Π_S ⟺ ∃υ: a − u = υ·Π_S.)

**(iii) Θ (the frozen disjunction, folded explicitly — see §3, fold E3):**

    F_Θ := ∏_{τ∈Λ} [ (δ_τ·ζ − 1)² + P̂_τ² + ((D·ζ′ − 1)·P₀_τ)² ]

**(iv) Main body (conjunction Φ ∧ Θ over the ordered field Q — fold E1):**

    F_main := F_Φ² + F_Θ²        [10 quantified variables so far]

**(v) Patch (Sun (9.4)):** for each p ∈ T, F_p(X, w₁, w₂, w₃) := the single polynomial of
Daans Prop 4.2 expressing p·X ∈ Z_(p) (t ∈ m_p ⟺ p·t ∈ Z_(p)), existential witnesses taken
from (y, r, s). Then

    F_patch := ∏_{p∈T} F_p        [finite product; 3 witnesses, shared]

**(vi) Final (union by padded product — fold E2; X ≠ 0 cut — fold E4):**

    **F := (F_main · F_patch)² + (X·ι − 1)²**

## 3. The folds, verified set-exact (all over Q, which is ordered)

- **E1 (conjunction):** over an ordered field, f = 0 ∧ g = 0 ⟺ f² + g² = 0. Used for
  F_Φ ∧ F_Θ and for the final X·ι = 1 conjunct. *Exact.*
- **E2 (union, padded product):** F_main·F_patch = 0 ⟺ F_main = 0 ∨ F_patch = 0; the witness
  block is the 10 main variables, with F_patch reading only (y,r,s); unused witnesses are free,
  so the union costs max(10, 3) = 10. *Exact.*
- **E3 (disjunction over Λ + the two inequations, in ONE equation and 5 witnesses):**
  For each τ: P̂_τ² + ((Dζ′−1)P₀_τ)² = 0 ⟺ P̂_τ = 0 ∧ (Dζ′ = 1 ∨ P₀_τ = 0). Given
  P̂_τ = D²·P_τ and P̂_τ|_{D=0} ≡ 0, this is equivalent to the *term equation*
  P_τ(c:=h(a,b,X³)) = 0 (case D≠0: P̂ = D²P; case D=0: the term c equals 0 by the 0⁻¹=0
  convention and the constraint reduces to P₀_τ = 0 — the c:=0 instance). Then
  (δ_τζ − 1)² + … = 0 adds δ_τζ = 1, i.e. δ_τ ≠ 0 — **load-bearing**: without it, δ_τ(a) = 0
  makes P_τ = −16B(r²−As²) − 16, satisfiable with c arbitrary, breaking soundness. The product
  over τ realises ⋁_{τ∈Λ} exactly (only one factor must vanish; ζ, ζ′ are shared and each
  vanishing factor fixes its own values). *Exact; preserves Sun's set D_Θ.*
- **E4 (X ≠ 0):** ∃ι: X·ι = 1. *Exact; needed because 0⁻¹ = 0 ∈ ⋃m_p would otherwise admit
  the false witness X = 0.*
- **Denominator clearing** of h: handled inside E3's case split (no new variables, no lost
  solutions; both cases are genuine (2.1)-instances, both sound).

Every fold preserves the underlying set, so Sun's Proposition 9.1 inclusions and §§5–8
constructions apply verbatim to F. **The set defined is exactly Q∖Z.**

## 4. Degree / size bookkeeping (scaling, not exact — depends on N = |Λ| and Daans's F_p)

Per branch: P̂_τ has degree ≤ 12 in X (N², D² with z = X³), ≤ 14 in a, ≤ 8 in b, ≤ 2 in y,r,s.
F_Θ squares these (≤ 24 in X) and multiplies over N branches: deg_X(F) ≈ 24N + deg_X(F_patch) + 2.
Per-branch term count ≈ 10²–10³; total ≈ 10³–10⁶ for plausible N. Estimates, marked as such.

## 5. Status (updated 2026-11-06)

- **Fully explicit:** every identity; the variable list; the fold mechanism; the O_{{2}} patch
  formula with concrete constants; the per-cell τ construction path.
- **Exhibited modulo mechanical execution:** S, u, π exact; **Λ = {1,3} proved + verified**
  (G1_FREEZING.md §3-bis); E_exc small and computable; the per-prime patch constants for
  T ∖ {2} are finite computations, then F expands (deg_X ≈ 50 + deg(F_patch)).
- **Sharpening candidate (unproven):** Sun §9's rational-only observation — the two τ-free
  branches τ₀ = 0 and τ₁ = 2a/A (δ ≡ 1 resp. 1/A, both never 0, so no ζ needed; his eqs (9.5)
  `(c²−Ay²) − 16·2b·(r²−As²) = 16` and (9.6) `c²−Ay²−16·2bA(r²−As²) = 16A`) would remove the
  freezing machinery entirely; Sun explicitly does **not** claim their sufficiency ("no unproved
  rational case division is required here"). If proven, the recipe loses Λ and E_exc shrinks;
  the variable count does not change (still 11 explicit / 7 collapsed).
