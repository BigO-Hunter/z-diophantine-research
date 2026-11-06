# VERIFICATION.md — independent machine verification of G1_FREEZING.md §3

Lane `dzq-exec`. Inputs read **read-only** from `../dzq-c1/` at commit fcb4477 (G1_FREEZING.md,
G2_REDERIVATION.md, POLYNOMIAL.md, COUNTS.md, CATCHES.md, sun2026.txt). Nothing here was derived
by the derivation lane; every number below was recomputed from the definitions.

**Headline: the persistence CONCLUSION is true, but the DERIVATION in G1 §3 does not survive.**
Three of the five displayed valuation facts are wrong as stated, the causal chain through Sun's
quantitative Lemma 3.1 fails at the margin in every cell, and the specific frozen parameter the
canonical construction produces **does not serve its cell** (explicit, rigorously confirmed
counterexamples). The conclusion is re-established here by a different, complete and elementary
route that needs only **two** τ values — so the theorem is fine and the bound improves, but the
`|Λ| ≤ 512` derivation cannot be banked as written.

Everything is exact 2-adic arithmetic (`padic.py`: 200-bit tracked precision; every reported
valuation is far below the precision floor, so all valuations are exact, not lower bounds).

---

## 0. Machinery, and why it is independent

| file | what it does |
|---|---|
| `padic.py` | Q₂ with tracked precision; E = Q₂(ζ), ζ²+ζ+1 = 0 (unramified quadratic) in the integral basis {1,ζ}; square roots of units ≡ 1 mod 8 by Newton |
| `test_padic.py` | 20 field-law / residue / trace / norm checks on the machinery itself |
| `cells.py` | the 32 (a mod 8, c mod 8) canonical constructions of G1 §3 |
| `verify_hensel.py`, `measure.py` | the perturbation inequalities, 12,800 exact perturbation points |
| `solve_test.py` | the direct ψ_τ solvability criterion (below) |
| `brute_check.py` | two arm's-length checks that do not use the criterion at all |
| `exhaustive.py`, `periodic.py`, `refine.py` | full-grid coverage scans |
| `verify_tau_map.py` | the replacement τ map, with witness construction |

Two facts carry the solvability analysis; both are checked, not assumed:

* **Norm-form image** (`brute_check.py (A)`): for A ≡ 5 mod 8 the form r² − As² is the norm form
  of the unramified E/Q₂, and its image is `{x : v(x) even} ∪ {0}`. Verified by exhaustive
  enumeration mod 2⁶ and mod 2⁸ for A = 5, 101, 197, 13 (all four sets equal); A = 3 (≡ 3 mod 8,
  not our case) differs, as it must.
* **Obstruction search** (`brute_check.py (B)`): a 2-adic solution must reduce to a solution mod
  2^K for every K, so enumerating y mod 2^K against `32b · Im_K` is a *rigorous* no-solution test.
  Used on every counterexample below (K = 10 and 12).

---

## 1. The cell decomposition and the residue layer — VERIFIED

`cells.py` builds the canonical data of G1 §3 for all 32 (a mod 8, c mod 8) cells (a odd ⟹ 4
residues; c ∈ Z₂ ⟹ 8). **All 17 checks pass in all 32 cells** (measurements.json):

| claim | status |
|---|---|
| A₀ = 1+4a₀² ≡ 5 mod 8 (2-adic unit, nonsquare) | ✅ (identity: a odd ⟹ a² ≡ 1 mod 8) |
| c̄-selection: c̄₀=0 ⟹ (z̄₁,z̄₂)=(ω,ω²); c̄₀=1 ⟹ (ω,1) | ✅ |
| Tr(ω)=Tr(ω²)=1, Tr(1)=0; Tr(z₁)+Tr(z₂)=c₀ | ✅ 32/32, exactly |
| z₂ = Teichmüller lift (ζ² resp. 1), N(z₂)=1 | ✅ 32/32, exactly |
| c₁ = c₀ − Tr(z₂) odd (ζ has Tr = −1) | ✅ |
| z₁ = Hensel root of X²−c₁X+1 near ω; integral; Tr(z₁)=c₁; N(z₁)=1 | ✅ 32/32, exactly |
| z₁ ∉ ±1, z₂ ≠ ±z₁, z₂ ≠ z₁⁻¹ | ✅ 32/32 (all exact inequalities) |
| γ = z₁⁻¹z₂ ≡ ω (c̄₀=0) resp. ω² (c̄₀=1); γ+1, γ−1 units; γ ≠ −1 | ✅ |
| t_p = (γ−1)/(√A(γ+1)) lies in **Q₂** (its ζ-coefficient is 0) | ✅ (computed, not assumed) |
| v(t_p) = 0; v(δ_{t_p}) = 1 − A t_p² = **2** | ✅ 32/32 |
| the (2.1) centre equation δ(c₀² − A y²) = 16 holds at the constructed y | ✅ 32/32, exact |
| coordinate identity cδ = 4(X + A t_p Y) (i.e. Sun (2.4) at r=s=0) | ✅ 32/32, exact |

The **128-cell count** is arithmetically right (4·4·8 = 128), but note: at r = s = 0 the
equation does not involve b at all (B = 2b enters only through the norm group, which is the whole
even-valuation set, and 2b is a unit times 2 — the parity is unchanged). So the *local* cell
count is 32, not 128, and the b-residue is decoration. That is a looseness, not an error.
Machine-checked (`extra_checks.py (b)`): the ψ_τ verdict is **identical for all eight unit b
values** {1,3,5,7,−1,−3,9,15} on 3,000 random points, 0 disagreements.

## 2. The valuation facts — verdicts

Exact measurements over 12,800 perturbation points (a ≡ a₀ mod 8, c ≡ c₀ mod 8, τ ≡ t_p mod 8;
`measure.py`):

| # | G1 claim | measured | verdict |
|---|---|---|---|
| I1 | v(ΔA) ≥ 6 | min **6** (6:6425, 7:3238, 8:1563, …) | **VERIFIED-COMPUTATIONALLY** (and by the elementary argument: v(4)+v(a−a₀)+v(a+a₀) = 2+3+1) |
| I2 | v(Δδ_τ) ≥ 6 | min **4** (4:6400, 5:3200, 6:1565, …) | **FAILS** |
| I3 | v(Δc²) ≥ 4 (c₀ odd) / 5 (c₀ even) | min **4** for c₀ odd, **5** for c₀ even (`extra_checks.py (a)`) | **VERIFIED-COMPUTATIONALLY** |
| I4a | v(ΔP) ≥ 6 | min **6** | **VERIFIED-COMPUTATIONALLY** |
| I4b | v(ΔP) ≥ 6 **> 2e = 4** | 6 > 2e holds on only **3,608/12,800** points | **FAILS** |
| I5a | v(Δ(∂P/∂y)) ≥ 6 | min **5** | **FAILS** |
| I5b | v(Δ(∂P/∂y)) > e | **12,800/12,800** | **VERIFIED-COMPUTATIONALLY** |
| E1 | v(y₀) = −1 for y₀ the i-coordinate of z₁ | v(Y) = **−1** in all 32 cells | **VERIFIED-COMPUTATIONALLY** |
| E2 | e := v(∂P/∂y)(centre) = 2 | e ∈ **{3,4,5,6}** | **FAILS** |

### 2.1 Why I2 fails (and why it does not, by itself, break anything)

Δδ as G1 computes it is `τ²ΔA` — i.e. it compares δ at the *same* τ. But the perturbation tuple
is `(a, c, τ)` with τ a **fixed** constant of Λ while the centre has τ = t_p. Writing τ = t_p + Δτ
with v(Δτ) ≥ 3,

    Δδ = A₀t_p² − Aτ² = −(2A₀t_p·Δτ + A₀Δτ² + ΔA·t_p² + …),  v(2A₀t_pΔτ) = 1+0+0+3 = 4.

So v(Δδ) ≥ 4, and 4 is attained (6,400 of 12,800 points). The Δτ term was dropped.

The consequence is bounded: in ΔP the δ-term already had valuation 2 + min(v(Δc²), v(ΔA)+2v(y)) = 6,
so **v(ΔP) ≥ 6 survives** (min measured exactly 6). Sun's Hensel inequality, however, needs
`v(P) > 2e`, and e is where the real error is (§2.2).

### 2.2 Why e = 2 fails — G1 conflates two different quantities

G1 writes *"y₀ := i-coordinate of z₁: y₀² = (c₁²/4−1)/A ⟹ v(y₀) = −1 … ∂P/∂y = −2Aδ_τy₀ ⟹
e = 1+0+2−1 = 2"*. The i-coordinate identity is **correct** (v(Y) = −1 in all 32 cells, exact).
But Y is *not* the witness of (2.1). Solving Sun's coordinate map
`z = (c−Aτy)/4 + ((y−τc)/4)i` for the (2.1) witness gives

    y_witness = 4Y + τc        (checked exactly: this y satisfies δ(c²−Ay²) = 16 in 32/32 cells,
                                and the companion identity cδ = 4(X+AτY) holds too).

Since v(4Y) = 2 + v(Y) = **1** and v(τc) = v(c) ≥ 0, one gets v(y_witness) ≥ 0 — measured
**{0,1,2,3}**. Hence

    e = v(−2Aδ y_witness) = 1 + 0 + 2 + v(y_witness) = 3 + v(y_witness) ∈ {3,4,5,6},

i.e. **2e ∈ {6,8,10,12}**, and `v(ΔP) = 6` is no longer `> 2e`. **The quantitative Hensel
argument does not close**, in any of the eight c-classes. (I5b survives because it only needs
5 + v(y_w) > 3 + v(y_w).)

## 3. The freezing claim itself — REFUTED for the canonical τ

Beyond the inequality chain, the *substantive* per-cell claim can be tested directly. ψ_τ(a,b,c) is

    δ_τ ≠ 0  ∧  ∃y,r,s ∈ Q₂:  δ_τ(c²−Ay²) − 16·(2b)·(r²−As²) = 16,

and since the norm form's image is `{even valuation} ∪ {0}` there is a **complete criterion**
(`solve_test.py`), no Hensel needed:

    with w := (c² − 16/δ_τ)/A :   solvable ⟺ v(w) odd, or w is a square, or w/2^{v(w)} ≡ 3,7 mod 8.
    Obstructed ⟺ v(w) even and w/2^{v(w)} ≡ 5 mod 8.

(The criterion is confirmed by the arm's-length necessary-condition search of `brute_check.py (B)`.)

Applying it with the τ that the canonical construction produces (τ ≡ t_p mod 8):

| c₀ (cell c mod 8) | canonical τ | obstructed points (full grid mod 256) |
|---|---|---|
| 0 | 1 | **1024 / 1024 (100%)** |
| 1,3,5,7 | 3,7,3,7 | 0 |
| 2 | 5 | 85 / 1024 (8.3%) |
| 4 | 1 | 0 here, but τ=7 and τ=9 are 100% obstructed |
| 6 | 5 | 82 / 1024 (8.0%) |

On the full grid a ≡ a₀, c ≡ c₀ mod 2^10 (524,288 points): **76,446 points are obstructed by the
canonical τ (14.6%)**.

**Explicit counterexample, rigorously confirmed** (`brute_check.py`, `measure.py`):

    a = 145, b = 1, c = −208 (so c ≡ 0 mod 8, cell (a₀,c₀) = (1,0)), τ = 1
    → admissible y residues mod 2^10: 0 ; mod 2^12: 0  ⟹ no Q₂ solution exists at all.
    (τ = 3 at the same point: solvable, v(w) = 2, u = 7.)

**Verdict: "one τ per mod-8 cell serves the whole cell" is FALSE for the Cayley-derived τ.** The
neighbourhood W of Lemma 3.1 around t_p is genuinely smaller than `{v(τ−t_p) ≥ 3}` — which is
exactly what the marginal `v(ΔP) = 6 = 2e` of §2.2 predicts.

## 4. The replacement: a 2-τ map that is complete, with proof

The obstruction has a closed form when τ is a plain integer.

**Case c odd, τ = 1.** δ = 1−A = −4a², so w = (c² + 4/a²)/A = (a²c²+4)/(a²A). With a, c odd:
a²c² ≡ 1 and a²A ≡ 5·1 mod 8, so numerator ≡ 5, w ≡ 5·5⁻¹ ≡ **1 mod 8** and v(w) = 0 — w is a
square, y = √w ∈ Q₂ exists explicitly, r = s = 0. ✅

**Case c ≡ 2 mod 4, τ = 1.** c = 2c₁ with c₁ odd: a²c² = 4a²c₁² ≡ 4 mod 32, so
a²c²+4 = 4(a²c₁²+1) with a²c₁²+1 ≡ 2 mod 8 ⟹ v = 3 odd ⟹ **v(w) = 3, odd** ⟹ solvable. ✅

**Case c ≡ 0 mod 4, τ = 3.** δ = 1−9A = −4(2+9a²), so w = ((2+9a²)c² + 4)/((2+9a²)A); a odd gives
2+9a² ≡ 3 mod 8 (a unit). v((2+9a²)c² + 4) = 2 exactly, and dividing by 4 leaves
1 + 4c₂²(2+9a²) ≡ 1 or 5 mod 8, so u = w/2² ≡ **3 or 7 mod 8** — never 5. ✅

So **τ = 1 if c ≢ 0 mod 4, τ = 3 if c ≡ 0 mod 4** serves *every* point of P₂. Machine checks:

* full grid a ≡ a₀ mod 8, c ≡ c₀ mod 8 over mod 2^10 — **0 / 524,288 obstructed**;
* 60,000 random points with unbounded 2-adic depth (|a|,|c| ≤ 2^20 plus the three c-classes) — **0 failures**, both by the criterion and by the constructive case check (including explicitly constructing y = √w and verifying δ(c²−Ay²) = 16 for every c-odd point);
* 2,000 random c-odd points with an explicit witness — 2000/2000;
* δ_τ ≠ 0 holds automatically for the map, with v(δ_τ) = 2 exactly: 0 violations in 20,000 deep random points (`extra_checks.py (c)`).

Note the map depends only on c mod 4: the freezing datum is coarser, not finer, than mod 8 — the
construction was simply aiming at the wrong τ.

**Consequences for the counts.** |Λ_local| = 2 (Sun's 4-distinct-lifts-per-class convention
would carry 4 lifts per c mod 4 class ⟹ ≤ 8, and E_exc then contains whatever primes those lifts
collide with). The quoted `|Λ| ≤ 512` is **not established**; `≤ 512` is not refuted either — it
is simply unsupported, and the correct local number is far smaller.

## 5. Bookkeeping I could also pin down (bonus)

POLYNOMIAL.md §4's degree table is exact, measured on the expanded branches
(`branches.json`): P̂_τ has degrees (X,a,b,y,r,s) = (**12,14,8,2,2,2**) and the Θ-factor
(**24,28,16,4,4,4,2,2**) — matching the doc's "≤12 in X, ≤14 in a, ≤8 in b" and "24 in X" exactly.
With |Λ| = 2 the deg_X estimate becomes ≈ 24·2 + deg(F_patch) + 2, not 12,300.

## 6. What remains unverified here

* Sun's §§5–8 local constructions at the other places, the Hasse step, and (9.4)'s E_exc — read in
  the source, not re-derived here.
* The general-`K_v` reading of Lemma 3.1 (only F = Q₂ is instantiated).
* The norm-group fact is verified exhaustively only to mod 2^10; the general statement is Serre
  V.2 (cited by Sun as [16]).
* Deep-cancellation stratum: at points with v(w) ≥ 8 the obstruction depends on digits beyond any
  fixed modulus (measured: shifting a or c by 256 flips the verdict at 14/4000 sampled points).
  The 2-τ map is *proved* for those strata by §4's case analysis (which is digit-independent),
  and the grid scans confirm it; but there is no bounded-modulus cell cover — a further reason
  `|Λ| ≤ 512` cannot be a cell-count theorem.
