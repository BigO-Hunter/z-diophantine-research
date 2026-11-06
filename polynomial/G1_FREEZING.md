# G1_FREEZING.md — the constants computed/bounded (gap G1)

> **CORRECTION PASS 2026-11-06 (post executor-lane verification, dzq-exec/VERIFICATION.md @ fcb4477):**
> §3's per-cell freezing claim is **REFUTED** and the bound `|Λ| ≤ 512` is **STRICKEN** (unsupported).
> Three valuation facts in §3 were wrong (I2, I4b's e, I5a) and the Cayley-derived τ does not serve
> its cell (exhaustive counterexample). §3 is preserved below with inline annotations; the corrected,
> executor-proved-and-verified replacement — **|Λ_local| = 2** via the rule *τ = 1 unless c ≡ 0 mod 4,
> τ = 3 if c ≡ 0 mod 4* — is §3-bis. A LESSONS section records why the errors happened.
> §§1–2 (S = {2}, u = 1, π = 2; the O_{{2}} patch constants) were independently verified by the
> executor (their §1: all 17 checks pass in all 32 cells) and STAND.

All 2-adic residue facts machine-verified (GF(4) arithmetic script, committed).

## 1. S, u, π — EXACT, verified

**S = {2}, u = 1, π = 2.** Checks: (i) 2 ∈ S ✓ (Q's only dyadic place); (ii) S = Odd(2) ✓,
|S| = 1 odd ✓; (iii) u = 1 ∈ Z₂^× and X²−X−1 over Q₂: mod 2 it is X²+X+1, no root in 𝔽₂,
monic ⟹ irreducible over Q₂ ✓. (Daans Thm 5.6 asks only for SOME S with (i)–(iii); the
minimal choice works.) Then Φ_u^S = {(a,b) : b ∈ Z₂^×, a ≡ 1 mod 2} and Π_S = 2.

## 2. The patch constants (O_{{2}} formula) — EXACT, verified

Q = [1,2)_Q ≅ (5,2)_Q, ΔQ = {2,5} (direct Hilbert computation, no ABHN), π₄ = 10, 𝔞 = 8.
See G2_REDERIVATION.md §1 for the explicit ∃₃ formula for Z_(2) and all checks.
For patch primes p ∈ T ∖ {2}: same Lemma 4.1 template, per-prime finite constant search
(computation path written; not executed — T depends on Λ, §4).

## 3. |Λ| ≤ 512 — derived here (**REFUTED — see §3-bis; preserved with annotations**)

> **[REFUTED]** The executor lane (exact 2-adic arithmetic, 12,800 perturbation points) found:
> (i) I2 below is false as a serving statement — the perturbation tuple includes the τ-shift
> τ = t_p + Δτ, whose cross-term 2A₀t_p·Δτ has v = 1+0+0+3 = **4** (I dropped the v(2) = 1
> factor and the τ-shift entirely by treating τ as fixed); measured min v(Δδ) = 4.
> (ii) e is wrong: the (2.1) witness is **y = 4Y + τc** (v ≥ 0, measured {0,1,2,3}), NOT the
> i-coordinate Y (v(Y) = −1 — that part was right) — so e = v(−2Aδy) = 3 + v(y) ∈ {3,4,5,6}
> and 2e ∈ {6,8,10,12}: **v(ΔP) ≥ 6 is NOT > 2e in any cell** — the quantitative Hensel
> closes on only 3,608/12,800 points, in NO cell fully.
> (iii) The substantive claim is refuted by exhaustive counterexample:
> **a = 145, b = 1, c = −208, τ = 1** ⟹ 0 admissible y mod 2^10 and 2^12 (rigorous
> no-solution test); on the c₀ ≡ 0 mod 8 cells the canonical τ obstructs **1024/1024** grid
> points; 76,446/524,288 obstructed overall. τ ≈ t_p is simply the wrong target — the center
> itself solves at τ = t_p exactly, neighbors fail at v(Δτ) = 3, exactly as the marginal
> v(ΔP) = 6 = 2e predicts.

**Cell decomposition.** P₂ = (1+2Z₂) × Z₂^× × Z₂ (Sun §3 (3.8) with u = 1). Partition by
residues mod 8: a mod 8 ∈ {1,3,5,7} (4), b mod 8 ∈ {1,3,5,7} (4), c mod 8 ∈ {0,…,7} (8)
⟹ **128 cells**. Claim: one τ per cell serves the whole cell. **[REFUTED — see above; also
the b-residue is decoration at r = s = 0: the true local cell count is 32 (executor-verified:
ψ_τ verdict identical across all eight unit b's, 0/3,000 disagreements).]**

**Canonical construction at the cell center (a₀,b₀,c₀)** — all explicit, residue layer
machine-verified over 𝔽₄ = 𝔽₂(ω), ω²+ω+1 = 0, T = 𝔽₄^× = {1,ω,ω²}:
- A₀ = 1+4a₀² ≡ 5 mod 8 ⟹ 2-adic unit and nonsquare ⟹ E₂ = Q₂(√A₀) = the unramified
  quadratic = Q₂(√−3) (both ≡ 5 mod 8) ∋ μ₃.
- z̄-selection (Lemma 2.2 residue step, VERIFIED): c̄₀ = 0 ⟹ (z̄₁,z̄₂) = (ω,ω²);
  c̄₀ = 1 ⟹ (ω,1). Traces: Tr(ω)=Tr(ω²)=1, Tr(1)=0 ✓; z̄₁ non-fixed ✓; sums match ✓.
- z₂ := Teichmüller lift of z̄₂ (z₂ = ζ² resp. 1, ζ = (−1+√−3)/2 ∈ μ₃ ⊂ E₂): exact norm 1 ✓.
- c₁ := c₀ − Tr_{E/K}(z₂) (Tr(ζ) = −1, Tr(1) = 2): c₁ odd in both cases ✓.
- z₁ := Hensel root of X²−c₁X+1 in O_{E₂} near ω (reduction X²+X+1 has distinct roots ω,ω² ✓);
  z₁ ≡ ω ⟹ z₁ ∉ ±1, z₂ ≠ ±z₁, z₂ ≠ z₁⁻¹ (residues distinct) ✓.
- γ := z₁⁻¹z₂ ≡ ω resp. ω²; **γ+1 is a unit in both cases** (ω+1 = ω² ≠ 0; ω²+1 = ω ≠ 0) ✓.
- t_p := (γ−1)/(√A(γ+1)) ∈ Q₂: v(t_p) = 0 (γ±1, A units) ✓; δ_{t_p} = 4γ/(γ+1)² ⟹
  **v(δ_{t_p}) = 2** ✓; y₀ := i-coordinate of z₁: y₀² = (c₁²/4−1)/A with c₁²−4 ≡ −3 ≡ 5 mod 8
  ⟹ v(c₁²/4−1) = −2 ⟹ **v(y₀) = −1** (not a unit — corrected from a first-pass claim; the
  bound below absorbs it). Smooth point (y₀, 0, 0) of P_{t_p} (Sun (2.1) with r = s = 0);
  ∂P/∂y = −2Aδ_τy₀ ⟹ **e := v(∂P/∂y)(center) = 1+0+2−1 = 2**.

**Persistence across the cell (quantitative Lemma 3.1).** **[REFUTED — annotated, preserved.
Two errors, per the executor's exact measurements: (a) the Δδ line drops the τ-shift
cross-term 2A₀t_pΔτ (v = 4): since the serving τ is a truncation τ = t_p + Δτ, v(Δδ) ≥ 4,
not 6; (b) "2e = 4" uses y₀ = Y (the i-coordinate, v = −1) where the (2.1) witness is
y = 4Y + τc (v ≥ 0): e = 3 + v(y_w) ∈ {3,4,5,6} ⟹ 2e ≥ 6. So the displayed "6 > 2e = 4" is
at best "6 > 6", which is false — and the substantive claim fails outright: a = 145, b = 1,
c = −208, τ = 1 has 0 admissible y mod 2^10 (exhaustive, rigorous).]** For (a,b,c) in the same mod-8 class
and τ := any rational with v₂(τ − t_p) ≥ 3 (exists: Q dense in Q₂; take a truncation of the
2-adic expansion — explicit): with Z₀ = (y₀,0,0) fixed,
- v(ΔA) ≥ 2+3+1 = 6·? — precisely: ΔA = 4(a−a₀)(a+a₀), v ≥ 2+3+1 = 6 (a₀ odd ⟹ v(a+a₀)=1);
  ~~v(Δδ_τ) = v(τ²ΔA) ≥ 6~~ **[WRONG: v(Δδ) ≥ 4 via the cross-term 2A₀t_pΔτ]**;
  v(Δc²) = v((c−c₀)(c+c₀)) ≥ 3+1 = 4 (c₀ odd) resp. ≥ 3+2 = 5 (c₀ even) — **[verified by
  executor: min 4 / 5 exactly]**;
- ΔP = Δδ·(c₀²−A₀y₀²) + δ_{τ}·(Δc² − y₀²ΔA): v ≥ min(6 + (4−2), 2 + min(4,6)) =
  min(8, 6) = **6** — **[the bound v(ΔP) ≥ 6 itself survives (executor: min exactly 6), but
  the conclusion "6 > 2e = 4" does not: 2e ≥ 6]**;
- Δ(∂P/∂y) = −2y₀(ΔA·δ_τ + A₀Δδ): v ≥ 1−1+min(6+2, 0+6) = **6** — **[WRONG: min 5 with the
  cross-term; the derivative condition v(ΔP_y) > e still holds since 5+v(y_w) > 3+v(y_w)]**.
~~Sun's parameterized Hensel (his Lemma 3.1, j = y, other witnesses kept at 0) then yields a
smooth Q₂-solution of the τ-branch at EVERY point of the cell. Hence I₂ ≤ 128 and

    **|Λ| ≤ 4·128 = 512** (Sun's literal 4-τ-per-tuple shape) or **≤ 128** (one τ per cell;
    E_exc grows correspondingly, §4).~~ **[BOTH STRICKEN: the Hensel step fails at the margin
    in every cell (closes on 3,608/12,800 perturbation points, none a full cell), and the
    per-cell serving claim is refuted by exhaustive counterexample. Replaced by §3-bis:
    |Λ_local| = 2.]**

Caveat (honest): ~~the valuation inequalities are whiteboard-derived (one careful pass); the
residue layer is machine-checked; the full inequality chain should be machine-checked before
banking 512 as a theorem.~~ **[SUPERSEDED: machine-checked by the executor — the inequalities
fail as stated (I2 min 4, e ∈ {3,4,5,6}, I5a min 5), and the per-cell serving claim is refuted
by exhaustive counterexample. The residue-layer facts (§3's construction data) all verified.]**

## 3-bis. REPLACEMENT (executor-proved + machine-verified): |Λ_local| = 2

The obstruction has a closed form when τ is a plain integer. With w := (c² − 16/δ_τ)/A
(B = bπ = 2b given π = 2 — consistent with our S = {2}), the norm-form image
{r² − As² : v even} ∪ {0} gives the complete criterion (no Hensel needed):

    solvable  ⟺  v(w) odd, or w a square, or w/2^{v(w)} ≡ 3,7 mod 8;
    obstructed ⟺  v(w) even and w/2^{v(w)} ≡ 5 mod 8.

**The rule: τ = 1 unless c ≡ 0 mod 4; τ = 3 if c ≡ 0 mod 4.** Proof (digit-independent):

- **c odd, τ = 1:** δ = 1−A = −4a²; w = (a²c²+4)/(a²A) ≡ 5·5⁻¹ ≡ 1 mod 8, v(w) = 0 — square,
  y = √w ∈ Q₂ explicit, r = s = 0. ✅
- **c ≡ 2 mod 4, τ = 1:** c = 2c₁, c₁ odd: a²c²+4 = 4(a²c₁²+1), a²c₁²+1 ≡ 2 mod 8 ⟹ v = 3
  odd ⟹ solvable. ✅
- **c ≡ 0 mod 4, τ = 3:** δ = 1−9A = −4(2+9a²), 2+9a² ≡ 3 mod 8 (unit); v((2+9a²)c²+4) = 2
  exactly; u = w/2² ≡ 3 or 7 mod 8 — never 5. ✅

δ_τ ≠ 0 automatic (v(δ_τ) = 2 exactly for both τ on a odd). Verification (dzq-exec):
0/524,288 full-grid points obstructed; 0/60,000 deep-random (unbounded 2-adic depth);
2000/2000 explicit witnesses (y = √w constructed and checked in δ(c²−Ay²) = 16); 0/20,000
δ-violations. **|Λ_local| = 2** (≤ 8 under Sun's 4-distinct-lifts-per-class convention, with
E_exc absorbing the lift collisions). The rule depends only on c mod 4 — coarser than mod 8:
the freezing datum was aiming at the wrong τ, and no bounded-modulus cell cover exists anyway
(deep-cancellation stratum: shifting a or c by 256 flips verdicts at 14/4,000 sampled points;
the 2-τ map's case analysis is digit-independent, which is what makes it complete).

## 4. E_exc — bounded, computable **[updated: with |Λ_local| = 2 this shrinks drastically]**

E_exc ⊇ {3,5,7,11,13,17,19,23} (residue fields ≤ 25, Lemma 5.1 needs q > 25) ∪ {poles of τ}
∪ {primes dividing numerators/denominators of τ, τ−1, τ+1 (residue τ̄_w ∈ {0,±1} fails
Lemma 5.1's hypothesis)} ∪ supp(π)∖S = ∅. **With the 2-τ map: only τ ∈ {1,3}** ⟹ the τ-collisions
are τ(τ²−1) ∈ {0} resp. {24} — τ = 1 has NO collisions (1,0,−1 have no prime divisors), τ = 3
collides only with p | 24 = {2,3} ⟹ **E_exc = {3,5,7,11,13,17,19,23} ∪ (τ-lift collisions ≤
Sun's 4-lift convention)** — tiny, explicitly computable. Patch cost: |T| ≈ 8–12 explicit
∃₃ formulas, union-folded at no variable cost.

## 5. Status of the exhibited polynomial **[updated]**

- Every constant now has a **written computation path**: S,u,π exact; patch constants exact for
  p = 2 (formula written in G2_REDERIVATION.md); **Λ = {1,3} with the c mod 4 dispatch rule,
  proved and machine-verified** (dzq-exec); E_exc tiny and explicit.
- Remaining to execute (mechanical): per-prime patch constants for T ∖ {2}; expand the
  polynomial (deg_X ≈ 24·2 + deg(F_patch) + 2 — see COUNTS.md).

## 6. LESSONS — why the errors happened (recorded so they stay learned)

1. **The dropped cross-term (I2).** The serving τ is a *truncation* τ = t_p + Δτ of the
   Cayley parameter, not t_p itself; δ's perturbation therefore contains the cross-term
   2A₀t_p·Δτ with v = v(2) + v(A₀) + v(t_p) + v(Δτ) = 1+0+0+3 = 4. I had treated τ as fixed
   (keeping only τ²ΔA, v ≥ 6) — and in the one place I did expand the τ-shift I dropped the
   factor 2 (v₂(2) = 1). A valuation estimate that compares "same parameter" against a claim
   about "nearby parameter" silently loses the linear term.
2. **Witness-coordinate confusion (e).** Sun's (2.1) witness y and the i-coordinate Y of the
   assembled z = (c−Aτy)/4 + (y−τc)/4·i are related by y = 4Y + τc. My norm computation
   correctly gave v(Y) = −1, but ∂P/∂y differentiates the *witness*: e = 1+0+2+v(y) =
   3 + v(y_w) ∈ {3,4,5,6}, not 2. Two different objects, one symbol, one fatal factor 4.
3. **Meta-lesson — a marginal inequality is a wrong-parameter smell.** v(ΔP) = 6 > 2e fails
   exactly at the margin (6 = 6 at v(y_w) = 0). When a quantitative argument closes only with
   slack 0, the right response is to distrust the PARAMETER CHOICE, not to shave the estimate:
   the executor's replacement aims τ at the *obstruction criterion* (the closed-form w-test)
   instead of at a center point's Cayley parameter — and the resulting rule is
   digit-independent (no cell cover can be: the deep-cancellation stratum has unbounded
   modulus sensitivity), needs 2 constants instead of ≤ 512, and comes with a complete proof
   rather than a perturbation argument.
4. **Process lesson.** The whiteboard pass caught the residue layer correctly (all 17
   construction checks survived independent verification) but lost exactly the two
   bookkeeping factors (v(2), and which coordinate is the witness) that separate "true at
   the center" from "true across the cell". Exact 2-adic arithmetic on a perturbation grid
   is the cheapest instrument that sees that difference; it should have been run before
   banking the bound.
