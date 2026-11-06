# FRONTIER.md — Lane 6 (dzq-k2): the k=2 double-or-nothing

Problem (board z-diophantine-in-q): find P ∈ Z[q, w₁, w₂] with
{q ∈ Q : ∃w₁,w₂ ∈ Q, P(q,w) = 0} = Z (score k+1 = 3), or prove none exists.
Setup: S := V(P) ⊂ A³_Q, π := q-projection. k=2 ⟺ π(S(Q)) = Z. Throughout,
"C(Q)" = Q-rational points; "horizontal" (curve C ⊆ S) = π|C nonconstant.

Notation from the lane docs (OPTIMIZATION_MACHINERY, PACKING_BOUNDARY) is reused;
B9's k=1 proof is re-derived here as Lemma 1 with a strengthening (finiteness, not
just non-surjectivity), which powers everything below. Cross-validation: Lemma 1's
genus-1 step is Koenigsmann's [Koe16, **v1 Lemma 19** = v2 Lemma 22, n=1 case],
unconditional there by Siegel — the two lanes derived the same engine
independently. All Koe16 pointers in this doc use **arXiv v1 numbering**; the
citation-revision map (before the ledger) pins every cross-validated reference.

--------------------------------------------------------------------
## Lemma 1 (curve finiteness; unconditional; the engine)

**Lemma 1.** Let C/Q be an irreducible curve and π: C → A¹ nonconstant. If
π(C(Q)) ⊆ Z, then π(C(Q)) is *finite*.

*Proof.* Genus ≥ 2: Faltings ⇒ C(Q) finite. Genus 1: C(Q) finitely generated
(Mordell–Weil); C minus the pole divisor of π is affine of genus 1; π(P) ∈ Z is
an integrality condition (stronger than S-integrality, S = primes of the
coefficients); Siegel ⇒ finite. [Equivalent EDS route as in B9: Silverman AEC /
Ward 1987.] Genus 0: C(Q) = ∅ trivial; else C ≅ P¹_Q, π = Q(t) ∈ Q(t)
nonconstant, and Q(t) ∈ Z for ALL t ∈ Q off finitely many poles. Choose the
parametrization so Q is regular at t = 0; then |Q(1/N) − Q(0)| ≤ c/N, so
Q(1/N) ∈ Z forces Q(1/N) = Q(0) for all large N ⇒ Q ≡ Q(0): contradiction. ∎

*Remark (audit, Claim 1):* the genus-0 arm uses C ≅ P¹_Q, which needs C(Q) ≠ ∅
and geometric integrality; for irreducible-but-geometrically-reducible C, C(Q)
lies in the finite intersection of conjugate components and the conclusion holds
a fortiori. Singular C: pass to the normalization (π pulls back).

Status: genus 0 elementary (here); genus 1 = Siegel 1929 (cit.) + Mordell–Weil
(cit.); genus ≥ 2 = Faltings 1983 (cit.). Same mechanism as [Koe16, **v1 Lemma
19** = v2 Lemma 22]
n=1 ("unconditionally, by Siegel's Theorem." — v1 wording verbatim). **This is lane-original tightening
of B9**: B9 proves non-surjectivity; Lemma 1 gives finiteness, which is what the
density and multisection arguments below consume.

--------------------------------------------------------------------
## Theorem 2 (unconditional structural constraints on any k=2 candidate)

**Theorem 2.** Assume π(S(Q)) = Z. Then:
**(a)** S(Q) is Q-Zariski dense in S.
**(b)** Every **horizontal** curve C ⊆ S (π|C nonconstant) has C(Q) finite.
Hence no rational section of π, no rational/elliptic multisection covering
infinitely many integers, and no horizontal curve with infinitely many Q-points.
(Vertical curves inside fibers over q ∈ Z are NOT excluded by π(S(Q)) = Z and
are not used downstream — repair C2/audit.)
**(c)** S is not unirational over Q. More generally, no dominant rational map
U: Y ⇢ S from any Y carrying a rational curve along which π∘U is nonconstant.
(The earlier "not ruled" is dropped per audit C3 — ruled ≠ unirational, e.g.
E×P¹ is ruled but not unirational.)
**(d)** (assembly exclusion) If S(Q) is contained in a finite union of curves ∪
points, dead. Hence every P of the SoS-assembly shape P = Σ_{j≥2} E_j² with
{E₁=…}= a curve is dead (over Q, S(Q) = {∀j: E_j=0}(Q) ⊆ that curve): **at k=2
the "conjunction is free" machinery (M1/M2 gadgets) is structurally unusable;
a candidate must be a single genuinely-surface-defining equation (irreducible
factor WLOG — every irreducible factor with infinite image inherits (a)–(c),
so take a minimal-degree factor).**
**(e)** The generic fiber of π has genus ≥ 1 or is a non-splitting conic family
(else killed by Lemma 1/Thm 3).

*Proof.* (a) If S(Q) not dense, its Q-Zariski closure C ⊊ S is a finite union of
Q-irreducible curves (or points); Z = π(S(Q)) ⊆ π(C(Q)) = ∪π(Dᵢ(Q)); Z infinite
⇒ some Dᵢ(Q) infinite with π|Dᵢ nonconstant ⇒ contradicts Lemma 1. (b) for
horizontal C: C(Q) ⊆ S(Q) ⇒ π(C(Q)) ⊆ Z; if C(Q) infinite then π(C(Q)) infinite
(π|C nonconstant, finite fibers) — apply Lemma 1 to a Q-irreducible component
carrying infinitely many points. (c) U: Y ⇢ S dominant from rational Y;
φ := π∘U dominant Y ⇢ A¹; restrict φ to a line ℓ with φ|ℓ nonconstant (exists,
else φ constant): φ|ℓ(t) ∈ Z for all t ∈ ℓ(Q) off a finite set, contradicting
the Lemma 1 genus-0 step. (d) as stated; factor reduction: each factor's image ⊆
Z, infinite for some factor, and (a)–(c) need only "π(S(Q)) ⊆ Z, infinite". ∎

Status: fully proved here; inputs = Lemma 1 + elementary algebraic geometry.
**Consequence for the board: (c) kills every currently-known construction idiom
at k=2** — sum-of-squares assemblies (d), norm-form cores (they live on rational
or unirational surfaces), positivity gadgets (need 4 witnesses anyway, B8).

--------------------------------------------------------------------
## Theorem 3 (the deg_w ≤ 2 stratum: dead, one hypothesis)

Write d_w = deg_w P (degree in (w₁,w₂) jointly).

**(i) d_w ≤ 1: impossible, unconditional.** P linear in w₂: P =
A(q,w₁)w₂ + B(q,w₁). Solubility in (w₁,w₂) ⟺ ∃w₁ [A(q,w₁) ≠ 0 ∨ B(q,w₁) = 0].
If A ≢ 0, then π(S(Q)) ⊇ {q : A(q,·) ≢ 0}, a **cofinite** subset of Q — cofinite
⊋ Z, dead immediately, no Lemma 1 needed (repairs the earlier garbled equivalence
— audit C4). If A ≡ 0, P = B(q,w₁) and π(S(Q)) = π(V(B)(Q)), an A²-curve's image:
Lemma 1 ⇒ finite ≠ Z. ∎

**(ii) d_w = 2, generic fiber reducible over Q(q): impossible, unconditional.**
P = c(q)·P̃₁·P̃₂ (c ≠ 0 const-factor): image = finite ∪ π(S̃ᵢ(Q)); each S̃ᵢ is an
(i)-shape ⇒ finite. ∎

**(iii) d_w = 2, genuine conic bundle (P irreducible, generic fiber smooth conic
over K=Q(q)): impossible conditional on HP(F,G).** Diagonalize the generic fiber
over K: C ≅ {x² = F(q)y² + G(q)z²}... concretely the fiber over q₀ is soluble
over Q iff the quaternion algebra (f(q₀), g(q₀)) splits over Q, i.e. iff the
Hilbert symbol (f(q₀),g(q₀))_v = 1 for every place v (Hasse; f,g ∈ Q[q] explicit
from P). **Computed structure of the symbol (all elementary; p ∤ 2, write
q₀ = a/b, e = v_p(b) ≥ 1, F̃,G̃ the homogenizations):**
  * At p | b, p ∤ a·2·f_D·g_D: v_p(f(q₀)) = −e·deg f, v_p(g(q₀)) = −e·deg g, and
    the whole symbol reduces to a character independent of a:
    (f,g)_p = (f_D/p)^{−eD_g}·(g_D/p)^{−eD_f}·(−1)^{eD_fD_g(p−1)/2}
    (D_f = deg f etc.). So the a-dependence cancels (total (a/p)-exponent
    −2eD_fD_g is even), and **denominator primes can always be chosen good**:
    finitely many fixed quadratic characters ⇒ a positive-density Chebotarev
    class of good b. Plus the real place (sign) and p = 2 (mod-8 squareclasses)
    fold into the same finite CRT/Chebotarev choice — as do primes p | 2f_Dg_D.
    **The divisibility is load-bearing** (audited: 32/32 closed-form failures
    when p | f_D, since F̃(a,b) ≡ 0 mod p then gives v_p(f(q₀)) ≠ −e·D_f;
    audit C5 / audit RECHECK.md arm B).
  * At p ∤ 2b: only numerator primes of F̃(a,b)G̃(a,b) can obstruct; at such p
    with α = v_p(f(q₀)), β = v_p(g(q₀)): symbol = (−1)^{αβ(p−1)/2}(u_f/p)^β
    (u_g/p)^α; if exactly one valuation is odd you need the other's unit to be a
    QR mod p. **This is the wall: these conditions are uncontrolled arithmetic
    of the integer F̃(a,b)G̃(a,b).**

**Hypothesis HP(P):** there exist a ∈ Z, b > 1 in the good Chebotarev class,
a ≡ 1 (mod rad(b)), q₀ = a/b avoiding the finite set where the fiber degenerates,
such that for every prime p | F̃(a,b)G̃(a,b), p ∤ 2b, the parity/QR conditions
above hold (and the real + 2-adic conditions). This is the computable,
per-candidate form of "the fiber over some non-integer q₀ is everywhere locally
soluble" — equivalent to it by the standard conic criterion (Hasse–Minkowski for
conics; cit. Serre, Course in Arithmetic, Ch. IV; ABSENT in Mathlib per A4).

**Theorem 3(iii): HP(P) ⇒ π(S(Q)) ⊋ Z** (Hasse ⇒ the fiber over q₀ has a Q-point;
q₀ ∉ Z). Contrapositive: a k=2 conic-bundle candidate **commits to ¬HP**: for
EVERY (a,b) as above, some numerator prime violates the pattern — a strong,
search-semi-decidable, Schinzel-flavored arithmetic commitment. Status: HP is
open in general (contains Schinzel-type prime-value difficulty); provable in
individual instances by finite search; **per-construction semi-decision kill:
enumerate (a,b) — any hit kills the candidate outright.**

**Addendum (source: audit measurement):** for the demo pair (f,g) = (q²+1, q+3)
below, HP is **TRUE**: explicit hit q₀ = 4/3 (f(q₀) = 25/9 a square ⇒ the fiber
splits), with 1035/6662 ≈ 15.5% of audited (a,b) candidates giving
everywhere-soluble fibers. The Thm 3(iii) kill is operative, not vacuous. ∎

--------------------------------------------------------------------
## Theorem B0 (conditional floor; literature)

**Theorem (Koenigsmann [Koe16, **v1 Thm 20 = v2 Cor 23**]).** Assume BL*: for V/Q absolutely
irreducible ≥1-dim with V(Q) Q-Zariski dense, ∪_φ φ(A(Q)) (φ: A ⇢ V nontrivial
rational maps from ≥1-dim abelian A/Q) is also dense. Then **no infinite subset
of Z is existentially definable in Q**. In particular k=2 (and every k) is
impossible: score = ∞ under BL*.
Mechanism: [Koe16, v1 Lemma 19 = v2 Lemma 22]: density of V(Q) forces density of
V(Q) ∩ π^{-1}(Q∖Z), via BL* + Faltings integrality on abelian varieties
([F, Cor 6.2]). **Sharpening contributed here: the lemma's density hypothesis is
FREE for k=2 candidates — it is Theorem 2(a), which we prove unconditionally.**
The imported reduction needs one line (audit C6, mirroring Koe16's own proof of
v1-Thm-20/v2-Cor-23): the Q-irreducible factor carrying the infinite π-image is
automatically **absolutely irreducible** — if geometrically reducible, its
Q-points lie in the codim-2 intersection of conjugate components, giving finite
π-image. So the combination "Thm 2(a) + [Koe16 v1 L.19/v2 L.22] ⇒ under BL*,
every k=2 candidate has π(S(Q)) ⊋ Z" is seamless. For n=1 (k ≤ 1) the lemma is
unconditional (Siegel) — recovering B9. Status: cited ([Koe16] =
arXiv:1011.3424; published Annals 183 (2016) 73–93; numbering differs per
revision — see the citation-revision map); Faltings "Rational points" (1984)
Cor 6.2 (cited).

--------------------------------------------------------------------
## The frontier (what is actually open)

By Thm 2/3, any k=2 candidate must have **d_w ≥ 3**: fibers are plane cubics
(genus 1) or worse; by Thm 2(b) the fibration has **no section and no rational
or elliptic multisection covering infinitely many integers**; by Thm 2(c) S is
not unirational; under BL* also not
of general type (Thm 2(a) + [Koe16]). Residue: **S is a genus-one fibration
(possibly K3-like for d_w = 4) over A¹ whose fibers have Q-points exactly over
Z.** The open core, named:

**Conjecture G.** There is no genus-one fibration π: S → A¹ over Q given by one
polynomial P(q,w₁,w₂) (S a hypersurface in A³_Q, π the q-projection) whose
fibers are **split in the sense of having a Q-rational point** (trivial torsor
class — "split" does NOT mean split-as-a-fibration; no section is implied)
exactly over Z. Note: Conjecture G false ⟺ a k=2 genus-one candidate exists ⟺
Z existentially definable in Q, so neither direction is currently settleable
unconditionally (definition + note per audit C8).

Known: nothing in the literature rules Conjecture G in or out. The conic-bundle
fibration method (norm descriptions of soluble sets, CT–SD-style) has **no
known genus-one analogue**: for genus-one fibers the soluble set is governed by
torsor-class specialization (descent), not by finitely many norm conditions, and
no theorem controls which base points split a genus-one torsor family. Under
BL* it dies (Thm B0). Unconditionally it is open. Also open unconditionally:
d_w ≥ 4 (fiber genus ≥ 3) — Faltings bounds fiber point counts but ≥ 1 point
per integer fiber is consistent with every unconditional tool we have.

--------------------------------------------------------------------
## The valuation/certifiability lens (per A4/CERTIFIABILITY.md)

Cheapest certifiable leaf = valuation statements over Q (`padicValRat` exists).
Verdicts for the three shapes the certificate lane proposed:

**(i) Norm-form identities forcing v_p(q) ≥ 0 ∀p: dead for all natural folds at
k=2; general case open (downgraded per audit C7).**
The Hasse fold of the Koenigsmann T_{a,b} = ∩_{p∈Δ_{a,b}} Z_(p) mechanism needs
the quaternion norm form: S_{a,b} has 4 witnesses, T = S+S has 8 — **at k=2 that
fold cannot even be written.** A 2-witness binary fold x² − a(q)y² = c is
soluble ⟺ the quaternion (a(q), c) splits ⟺ c ∈ N(Q(√a(q))) — a Hasse-norm
condition (the earlier "no local-global content" was the wrong mechanism; audit
C7). What is true: norm membership depends only on the square class of a(q)
(norm groups contain all squares), and N(Q(√c)) is finite-index constraining
only primes dividing 2c·a(q); hence the obvious folds die (a(q) = q cannot see
integrality: q and q/4 share a square class), but **no general impossibility
theorem for arbitrary polynomial a(q) is proved** — and any surviving fold still
faces the Thm 3(iii) numerator wall and Thm 2(c). First score where the
quaternion-norm fold is writable: k = 3 (same numerator-prime wall applies; same
mechanism, not re-verified in detail). The known compressed complement
constructions (Daans 2024: 10; Sun 2026: 7 witnesses for Q∖Z, lane-carried
citation) live ≥ 7 for this reason — the Z-polarity is strictly harder than the
complement because ∩_all p has no single-∃-witness carrier.

**(ii) Bound-witness (finitely many primes + size witness): dead at k=2,
unconditionally.** A size/ordering witness needs a positivity gadget; over Q,
t ≥ 0 ⟺ 4 squares and 3 provably fail (B8); any inequality-flavored condition
inherits ≥ 4 witnesses. With 2 slots the MRDP-style "carry the bound" trick has
no home — and would additionally collide with Thm 2(d) (SoS assemblies are dead
at k=2 regardless).

**(iii) Curve-family fibers with Hasse violations exactly over Q∖Z:** this is
exactly the frontier. For conic fibers the converse leaf is Hilbert-symbol/
valuation-sized (certifiable per-fiber) but the *uniform* converse is exactly
HP/¬HP (Thm 3(iii)) — killed conditional on HP, i.e. alive only in a
Schinzel-failure world. For genus-one fibers the converse leaf is torsor descent
(XL in Mathlib per A4's matrix): **even a found d_w = 3 construction would not
be certifiable today.** Net: **the only k=2 shapes with valuation-sized converse
leaves are exactly the ones Thm 3 kills (conditionally); A4's "valuation-only
converse" desideratum and a live k=2 candidate are (conditional on HP being
provable) jointly unsatisfiable.**

--------------------------------------------------------------------
## Horn A verdict / conditional template

No construction found; every classical idiom is excluded (Thm 2(c),(d), Thm 3,
lens (i),(ii)). The cleanest honest conditional statement a k=2 row could carry:

**Template row (hypothesis stated, nothing hidden):** "Assume ¬HP(F,G) fails —
i.e. assume HP(F,G) for the explicit pair (F,G) arising from the displayed P.
Then [P] is a k=2 row." — vacuous as stated (HP(P) contradicts the row being a
definition): **this is the content of Thm 3: a conic k=2 row requires the
falsity of an explicit, finite-search-checkable arithmetic statement.** For
d_w = 3: a row would carry hypothesis "Conjecture G is false for the displayed
explicit P" (decidable on each integer fiber by point search; the universal
non-integer side is the honest, named gap). Per the audit-lane doctrine, both
forms take their hypotheses directly on rational-point sets — no (O.8)-style
machinery, no ultrafilters.

## Horn B verdict

Unconditional floor: **still 3** (k=2 not excluded unconditionally; Conjecture G
open). New unconditional content: Lemma 1 (finiteness form), Thm 2(a)–(e)
(density, no sections/multisections, non-unirationality, assembly exclusion),
Thm 3(i)–(ii) (d_w ≤ 2 except genuine conic bundles), the denominator-prime
Chebotarev lemma inside Thm 3(iii). Conditional: **under BL*, score = ∞**
(Koenigsmann v1 Thm 20 = v2 Cor 23, made seamless by Thm 2(a)); **under
HP-uniformity, d_w ≤ 2 is dead**, pushing any candidate into the d_w ≥ 3
genus-one stratum.

--------------------------------------------------------------------
## Citation-revision map (repair C1)

Every cross-validated Koenigsmann reference, pinned per revision. Source of the
defect: the lane quoted arXiv **v1** numbering; v2 (accepted version, Oxford ORA
copy) and the published version renumbered.

| Content | arXiv:1011.3424 **v1** | arXiv v2 (ORA) | published: Annals 183 (2016) **73–93** |
|---|---|---|---|
| density lemma, "For n=1 the Lemma holds unconditionally, by Siegel's Theorem." | **Lemma 19** (lane quotes verbatim) | **Lemma 22** | renumbered again (BL material) |
| "no infinite subset of Z existentially definable in Q" | **Theorem 20** | **Corollary 23** | renumbered again |
| — | — | v2's "Lemma 19" is an unrelated diophantine lemma (R_p^[1]: no curves, no Siegel) | — |

All [Koe16] pointers in this doc mean v1 numbering; pull v1 when auditing quotes.
(The original "Annals 183 (2016) 405" pagination was wrong; corrected to 73–93.)

## Status ledger

| Item | Status |
|---|---|
| Lemma 1 | proved here (elementary + Siegel + Faltings; = [Koe16, v1 L.19 = v2 L.22] n=1) |
| Thm 2(a)–(e) | proved here, from Lemma 1 |
| Thm 3(i)–(ii) | proved here |
| Thm 3(iii) Hilbert reduction at p | b, independence of a | proved here (elementary QR) |
| Hasse criterion for conics | cited (Serre; Mathlib-absent per A4) |
| HP(P) | hypothesis (Schinzel-flavored, search-semi-decidable) |
| Thm B0 (BL* kills all k) | cited [Koe16, v1 Thm 20 = v2 Cor 23]; its L.19/L.22 density input supplied here unconditionally for k=2 (+ abs-irreducibility line, audit C6) |
| Faltings integrality on abelian varieties | cited [F, Cor 6.2] (via [Koe16]) |
| Conjecture G (genus-one exact-Z) | open; named here |
| Chebotarev/Dirichlet (good denominators) | cited (standard) |

Gap blocking the next step (both horns): control of **torsor-class
specialization for genus-one fibrations** — the soluble-fiber set of a genus-one
fibration has no known finite (norm-)description; proving Conjecture G or
building a counterexample requires exactly this. Secondary gap: HP(P) in
general (= a Schinzel-type statement).

--------------------------------------------------------------------
## Numeric spot-check (hilbert_check.py, this dir)

Thm 3(iii)'s closed form at denominator primes verified against direct Hilbert
computation for (f,g) = (q²+1, q+3), (a,b) ∈ {(1,3),(5,7),(11,6),(23,15),(7,35)}:
7/7 match, all +1 (here f_D=g_D=1 makes every denominator prime good).
Numerator-prime wall demonstrated: 3/7 sample points carry an odd-valuation
prime of F̃·G̃ with non-residue g-unit ⇒ fiber locally insoluble — the wall is
real, not vacuous. (p=2 excluded per doc: folds into finite CRT choice.)
