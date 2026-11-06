# COUNTS.md — the single numbers

## Headline

| Route | Variables (k+1 incl. X) | Status | Unconditional? |
|---|---|---|---|
| **Sun 2026 (R2), collapsed** | **7** | exact, published (Sun §9 count) | ✅ (arXiv:2607.28606 Thm 1.1) |
| **Sun 2026 (R2), fully explicit (this lane)** | **11** | exact, derived here (POLYNOMIAL.md) | ✅ (same proof, constructive folds) |
| Koenigsmann-negation (R1) | ≈3·10²–1.5·10³ | **estimate, NOT closed** | ✅ (Koenigsmann Cor 2) but no polynomial |

**The single number for the campaign: 7** (bankable, published, unconditional).
**The single number for a constructively writable artifact: 11** (same theorem, folds made explicit).

## How 7 is derived (verified against Sun §9, verbatim structure)

⋃_{w∉S₀} m_w is ∃⁷-definable: parameters a,b (2) + Φ_u^S (∃³, Daans Lemma 5.2) + Θ (∃³,
Sun (4.10)); conjunction by DDF Thm 1.4 (arXiv:2102.06941, "Theorem 1.4 (Corollary 5.11)":
rk^∃(D₁∩D₂) ≤ rk^∃(D₁)+rk^∃(D₂)−1 for K finitely generated over a perfect field) gives 3+3−1 = 5;
+2 = 7. Duality (Daans Cor 2.4 context / Sun (1.1)): ⋂O_v = (K∖(⋃m_v)^{-1}) ∪ {0}; the t ≠ 0 cut
merges with the ∃¹ set {Xι = 1} at the same −1 rate ⇒ Q∖Z is ∃⁷. Sun's abstract states n = 7
for Q∖Z explicitly. **Depends on the non-constructive collapse** (Daans Prop 2.2 via DDF
Cor 4.12; DDF §1: "we do not write down an existential formula…") — see CATCHES gap G3.

## How 11 is derived (this lane; POLYNOMIAL.md §3)

| Component | Witnesses | Mechanism (all explicit) |
|---|---|---|
| a, b | 2 | quantified quaternion parameters |
| Φ_u^S | 3 | bb₁−1 = σΠ_S, a−u = υΠ_S, conjunction f²+g² = 0 (ordered Q) |
| Θ | 5 | y,r,s + ζ (δ_τζ = 1 ⟺ δ_τ ≠ 0) + ζ′ (Dζ′ = 1 ∨ P₀ = 0 fold for the h-denominator) |
| Φ ∧ Θ | 3+5 = 8 | f²+g² (no DDF −1 without model theory) |
| patch ⋃_{p∈T} m_p | max(8+2, 3) = 10 | padded product union |
| X ≠ 0 | +1 | X·ι = 1 |
| **Total** | **11** | |

11 − 7 = 4 = 2 (explicit ≠-absorption: ζ, ζ′, standing in for DDF Cor 4.12's collapse)
+ 1 (no constructive −1 in the Φ∧Θ intersection) + 1 (no constructive −1 in the t≠0 intersection).
Each saving rung is a named published mechanism: Becher–Daans constructive companion (announced
in DDF §1 for perfect fields) → 10, then 9; a constructive Cor 4.12 → 7.

## Secondary counts (updated 2026-11-06, correction pass: see G1_FREEZING.md §3-bis, §6)

- **|Λ_local| = 2** (τ = 1 unless c ≡ 0 mod 4, τ = 3 otherwise — executor-proved, digit-independent,
  machine-verified: 0/524,288 grid + 0/60,000 deep-random + 2000/2000 explicit witnesses). ≤ 8
  under Sun's 4-lifts-per-class convention. **The earlier |Λ| ≤ 512 cell-bound is STRICKEN**
  (refuted derivation + exhaustive counterexample; correction history in G1_FREEZING.md §3, §6).
  S = {2}, u = 1, π = 2 exact; patch constants exact for p = 2; |E_exc| small (τ = 1 collision-free,
  τ = 3 collides only with p | 24) and computable.
- Degree: deg_X ≈ 24·|Λ| + deg(F_patch) + 2 = **≈ 50 + deg(F_patch)** (executor measured the
  expanded branch degrees exactly: P̂_τ = (12,14,8,2,2,2), Θ-factor = (24,28,16,4,4,4,2,2) —
  matching this doc's per-branch table). Per-branch terms ≈ 10²–10³ (estimate).
- R1 (Koenigsmann-negation): the constructions-lane figures (≈16/T^×, 64/I, 128/J, 256/J(R),
  ×3 branches) are cost *estimates* from Koenigsmann's constructions (Cor 15, Prop 16); his
  paper states no n. Closing R1 to a number requires extracting and counting his ∃-definitions
  — a separate derivation, not done here (gap G5). R1 is dominated on count by R2 regardless.

## Bottom line

- Board score analogue for Q∖Z (lower better): **7** — the unconditional artifact, 40×–2·10⁵×
  under the incumbents' conditional 4,973-row axis, but it defines the *complement* set and so
  is score-N/A on the board (as the constructions lane already ruled: complement of Σ₁ is Π₁,
  never convertible).
- Certifiable explicit artifact: **11 variables**, recipe-complete modulo finite constants.
