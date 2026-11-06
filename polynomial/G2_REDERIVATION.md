# G2_REDERIVATION.md — Daans 2024 §4/§5 re-derived (gap G2 closed to named cited inputs)

Source: Daans, arXiv:2301.02107v2 (J. LMS 109 (2024) e12864). Everything below was extracted
from the paper and re-derived here; only the items explicitly marked **[cited]** remain black-box.

## 1. Prop 4.2 (O_S is ∃₃-definable) — re-derived, with explicit constants for S = {2}

**Lemma 4.1 [Daans, extracted; proof re-verified]** — with a nonreal quaternion Q over K,
S ⊆ ΔQ, and π, 𝔞 ∈ K^× such that ∀v ∈ ΔQ: v(π) = 1, v(𝔞) ≥ v(1+4𝔞) = 0, and
X²−X−𝔞 has a root over K_v ⟺ v ∈ S, then:

    ⋂_{v∈S} O_v = {0} ∪ {x ∈ K : Q splits over K_(𝔞−(πx²)^{-1})},   K_(t) := splitting field of X²−X−t.

Proof re-verified: (⇐) x ∈ O_v ⟹ X²−X−(𝔞−(πx²)^{-1}) has no root over K_v (if α root then
2v(α) = v(α²−α−𝔞+(πx²)^{-1}) = −1−2v(x), parity contradiction); (⇒) x ∉ O_v ⟹ the polynomial
reduces to X²−X−𝔞 mod m_v ⟹ root by Hensel; and Q splits over the quadratic extension iff it
IS one (Prop 3.3 [cited, elementary: inv_L(res Q) = [L:K]·inv_K(Q) = 0]), plus the global
reduction "split over L ⟺ split over all L_w" = ABHN **[cited = Daans Thm 3.5 = NSW08 8.1.17]**.

**Prop 3.6(iii) [Daans, extracted — the explicit ∃₃ shape]:** for Q = [A,B)_K
(characteristic-independent: e²−e = A, j² = B, ej+je = j) and c,d ∈ K:

    Q splits over the splitting field of X²−cX+d
    ⟺ ∃x₁,x₂,x₃ ∈ K, (2x₁−c, x₂, x₃) ≠ (0,0,0):
       x₁² + x₁(c−2x₁) − A(c−2x₁)² − B(x₂² + x₂x₃ − A x₃²) = d.

(Norm/trace algebra of [Daa21 §3]; the not-all-zero condition excludes the degenerate witness
α ∈ K. Verified: (ii)⟹(i) via K(α) = the quadratic splitting field and [Sch85 5.4].)

**Constants for K = Q, S = {2} (this lane's selection, Hilbert-symbol verified):**

- Q := [1, 2)_Q ≅ (1+4·1, 2)_Q = (5,2)_Q. 2-adic Hilbert: (5,b)_2 = (−1)^{v₂(b)} ⟹ ramified
  at 2 ✓; (5,2)_5 = (2/5) = −1 ⟹ ramified at 5 ✓; split at ∞ (5,2 > 0) ⟹ nonreal ✓.
  **ΔQ = {2,5}** (even ✓, no ABHN needed — direct Hilbert computation).
- π₄ := 10 (v = 1 on ΔQ ✓). 𝔞 := 8: v(𝔞) ≥ 0 and v(1+4𝔞) = v(33) = 0 on {2,5} ✓;
  X²−X−8: disc 33 ≡ 1 mod 8 ⟹ root over Q₂ ✓; 33 ≡ 3 mod 5 nonsquare ⟹ no root over Q₅ ✓.
  So "root ⟺ v ∈ S" holds on ΔQ ✓. All Lemma 4.1 hypotheses verified.

**The explicit O_{{2}} formula** (substituting c = 1, d = −𝔞′, 𝔞′ = 8 − (10x²)^{-1}, A = 1, B = 2
into Prop 3.6(iii); LHS simplifies to 5x₁ − 5x₁² − 1 − 2x₂² − 2x₂x₃ + 2x₃²):

    **x ∈ Z_(2) ⟺ x = 0 ∨ ∃x₁,x₂,x₃ ∈ Q: 10x²·(7 + 5x₁ − 5x₁² − 2x₂² − 2x₂x₃ + 2x₃²) − 1 = 0.**

Exactness checks: for x ≠ 0 the cleared equation ⟺ the term equation (0⁻¹=0 semantics); the
x = 0 stratum is absorbed by "{0} ∪". Degenerate stratum 2x₁ = 1, x₂ = x₃ = 0 (excluded by the
not-all-zero condition) would force x² = 2/165 ∉ Q² ⟹ no spurious rational point ✓. The
x₂²+x₂x₃−x₃² anisotropy (disc 5) is not needed for soundness but keeps the stratum clean.

This closes the patch sets of POLYNOMIAL.md §2(v): **F_p for p = 2 is now explicit**; for the
finitely many other patch primes p ∈ T the same Lemma 4.1 template applies (new constants per
prime, finite search each — computation path written, not yet executed).

## 2. Lemma 5.5 (the h-bridge) — both directions re-derived

Statement [extracted]: for S = Odd(π), |S| odd, u with X²−X−u² irreducible on S, char ≠ 2:

    x ∈ ⋃_{v∉S} m_v ⟺ ∃(a,b) ∈ Φ_u^S : h(a,b,x) := a²x²g(a,b)/(1−x−a²x²) ∈ ⋂_{v∈Δ[a²,bπ)} O_v.

**(⇒) re-verified** [needs Daa21 Lemma 6.6 **[cited]**: ∃(a,b) ∈ Φ_u^S with Δ[a²,bπ) = S∪{w},
w(1+4a²) = 0, w(b) = 1 — an ABHN-class existence step]: then w(g(a,b)) = −2 (Lemma 5.3(2),
extracted ✓: v(g) = −2|v(b)| when 1+4a² is a unit and v(b) ≠ 0), v(g) ≥ 0 on S (Lemma 5.3(1) ✓),
and v(h) = 2v(a)+2v(x)+v(g) − v(1−x−a²x²) ≥ 0 on S∪{w} using the denominator valuation
v(1−x−a²x²) = min{0, 2v(a)+2v(x)} — from Lemma 4.7 [extracted ✓: homogeneous form with
anisotropic reduction; applied to Y₁²−Y₁Y₂−a²Y₂², whose reduction is anisotropic ⟺ X²−X−a²
irreducible mod v, valid where v(a) = 0; at w with v_w(a) < 0 the membership hypothesis
h ∈ O_w itself forces v_w(x) ≥ −2v(a)−v(g) > 0, keeping the formula's use in bounds sound —
case analysis re-done here].

**(⇐) re-verified, fully explicit**: (a,b) ∈ Φ_u^S ⟹ S ⊆ Δ and Q nonreal; |Δ| even (Thm 3.5
**[cited]**) and |S| odd ⟹ ∃w ∈ Δ∖S; Prop 3.4 [extracted ✓] ⟹ v_w(b) odd or v_w(1+4a²) odd;
Lemma 5.3(3) [extracted ✓, its proof is elementary: henselian + non-dyadic + the square-implies
contradiction] ⟹ v_w(g(a,b)) < 0; then 0 ≤ v_w(h) forces 2v_w(x) ≥ −2v_w(a) − v_w(g) > 0
⟹ x ∈ m_w. All steps explicit; no model theory.

## 3. Residual cited inputs (the complete list)

1. **ABHN / quaternion Hasse principle** (Daans Thm 3.5 = NSW08 8.1.17) — XL leaf, as ranked.
2. **[Daa21, Lemma 6.6]** — prescribed-ramification quaternion with (a,b) ∈ Φ_u^S (uses ABHN +
   weak approximation + Hilbert bookkeeping). Statement extracted via its use in 5.5.
3. **Hensel's lemma** (local, standard) — Mathlib-adjacent (M).
4. Prop 3.3 (quaternion splits over any quadratic ext of a LOCAL field) — elementary, provable.
5. [Sch85 5.4], [Pie82 17.10], [Alb39 IV.27] — standard quaternion-algebra facts inside
   Prop 3.6/Lemma 4.1's proofs.

Everything else in the 11-variable chain is now derived in this workspace.
