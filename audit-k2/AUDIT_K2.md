# AUDIT_K2.md — second-opinion audit of ~/bigo-campaign/dzq-k2/ (FRONTIER.md @ 91f9fb5/b4c164b)
Auditor: independent session, 2026-11-06. Read-only on source. Line refs = FRONTIER.md line numbers.

## Claim 1 — Lemma 1 (L17–33): VERIFIED, with two proof footnotes + a citation defect
- Statement (L17–18) is **true**: C/Q irreducible curve, π: C → A¹ nonconstant, π(C(Q)) ⊆ Z ⇒ π(C(Q)) finite.
- Genus ≥ 2 arm: Faltings ✓. Genus 1 arm: Mordell–Weil + Siegel (everywhere-integrality is an S-integrality condition, S = all primes) ✓. Genus 0 arm (L24–27) is elementary and **sound**: π(1/N) ∈ Z and π(1/N) → π(0) forces π(1/N) = π(0) for all large N; π − π(0) then has infinitely many roots ⇒ π constant, contradicting nonconstant.
- Footnote 1 (not stated): the genus-0 step uses C ≅ P¹_Q, which needs C(Q) ≠ ∅ AND geometric integrality. For irreducible-but-geometrically-reducible C, C(Q) lies in the finite intersection of conjugate components, so the conclusion still holds — add one remark. Singular C: pass to the normalization (π pulls back). No counterexample found in either direction.
- Cross-validation (L10–12, L30–31): the quoted mechanism **exists verbatim — in arXiv v1 only**. v1 Lemma 19: "…π a Q-linear projection. Then V(Q) ∩ π⁻¹(Q∖Z) is also Q-Zariski dense… (For n=1 the Lemma holds unconditionally, by Siegel's Theorem.)" — the lane's L31 quote "unconditionally, by Siegel's Theorem" matches v1 word-for-word. BUT in arXiv v2 (= accepted version, ORA copy) the same statement is **Lemma 22**, and v1's Thm 20 is v2's **Corollary 23**. The published Annals version (183 (2016) **73–93**, not "405" as L136 says) renumbered again. Verdict: content cross-validates; **pointer defect** — see CORRECTIONS.md.

## Claim 2 — Theorem 2 (L36–69)
- **(a) VERIFIED** (L55–57): argument correctly exploits "infinite subset of A¹ is dense" — Z infinite ⊆ π(closure) = ∪π(Dᵢ(Q)), each π(Dᵢ(Q)) finite by Lemma 1 ⇒ contradiction. Sound.
- **(b) GAP-NAMED**: L40–41 claims "**Every curve** C ⊆ S has C(Q) finite". The proof (L58–59) covers only π|C **nonconstant** (horizontal) curves; the constant branch ("image ≤ 1 pt") bounds the image, not C(Q). A vertical curve inside a fiber over q₀ ∈ Z is NOT excluded by π(S(Q)) = Z. All downstream uses (sections, rational/elliptic multisections, L141–146) consume only horizontal curves, so the repair is one word ("every **horizontal** curve"). Verified in the precise form: no horizontal curve with infinitely many Q-points; no rational section (would put Q∖finite ⊆ π(S(Q)) = Z, absurd); a multisection useful for k=2 must carry infinitely many rational points over integers ⇒ its horizontal curve dies by Lemma 1. "No elliptic multisection" holds in exactly that sense (finite-Q-point elliptic curves are excluded trivially).
- **(c) VERIFIED for non-unirationality** (L60–63): φ = π∘U restricted to a line ℓ with φ|ℓ nonconstant gives a rational function integer-valued on cofinite Q; the Lemma-1 genus-0 argument forces it constant — contradiction. The chain CLOSES. **Overclaim**: "not ruled (over Q, rationally)" (L44) is unsupported as written (ruled ≠ unirational; E×P¹ is ruled, not unirational). The same argument in fact kills dominance from any Y carrying a rational curve along which φ is nonconstant — state that, or drop "ruled".
- **(d) VERIFIED** (L45–51, L63–64): SoS shape P = ΣE_j² ⇒ S(Q) = common zero set of the E_j ⇒ (≥2 independent equations in A³) ≤ 1-dimensional ⇒ Lemma 1 ⇒ dead; common-factor collapse handled by the factor reduction, which is sound (Gauss lemma; "π-image ⊆ Z, infinite" transfers to each factor; minimal factor WLOG ✓). This IS the "conjunction unusable at k=2" argument: with 2 witnesses, a free conjunction = codim ≥ 2 = curve/points, never a surface. Closes.
- **(e)** corollary-status, consistent (split P¹ generic fiber ⇒ P¹_{Q(q)} has a point ⇒ section ⇒ immediate contradiction; conic ⇒ Thm 3(iii)).

## Claim 3 — Theorem 3 (L72–120)
- **(i) GAP-NAMED**: conclusion (d_w ≤ 1 dead, unconditional) **true**; proof text (L76–79) garbled. Literal "solvability ⟺ ∃w₁: B(q,w₁)=0" is false when A(q,·) ≢ 0 — then the equation is solvable in w₂ for ANY (q,w₁). Corrected: solubility ⟺ ∃w₁ [A(q,w₁) ≠ 0 ∨ B(q,w₁) = 0]; if A ≢ 0 then π(S(Q)) ⊇ {q : A(q,·) ≢ 0}, a **cofinite** set — an even stronger one-line kill. If A ≡ 0, P = B and the Lemma-1/curve argument applies. Conclusion robust.
- **(ii) VERIFIED**: Gauss lemma ⇒ factorization over Q[q]; factors have d_w ≤ 1 (case (i)) or are vertical planes q = const (finite image).
- **(iii) computed structure VERIFIED by independent re-derivation**: at p | b, p ∤ a: F̃(a,b) ≡ f_D·a^{D_f} (mod p) gives (u_f/p) = (f_D/p)(a/p)^{D_f}((b/p^e)/p)^{−D_f}; the a- and b′-exponents are ±2eD_fD_g (even) and cancel ⇒ (f,g)_p = (f_D/p)^{−eD_g}(g_D/p)^{−eD_f}(−1)^{e²D_fD_g(p−1)/2}, and e² ≡ e (mod 2) ⇒ L92–94 exact. **Small print named**: the reduction needs p ∤ 2·f_D·g_D; L96's "good class" absorbs this and L252 honestly notes f_D = g_D = 1 in the demo, but the doc should state "p ∤ f_D·g_D" explicitly. Numerics confirm the small print is load-bearing: the closed form fails 32/32 test points when p | f_D (see RECHECK.md, arm B).
- **HP(P) (L106–112)**: essentially precisely stated (per-prime parity/QR conditions explicit; real + 2-adic conditions referenced but could be written out: sign(f(q₀)g(q₀)) and the 2-adic Hilbert symbol). Honestly labeled: "hypothesis (Schinzel-flavored, search-semi-decidable)" (L235), "open in general" (L117–118) ✓ — it is a novel per-candidate exists-statement, correctly NOT passed off as literature. Kill logic VERIFIED: Hasse ⇒ soluble fiber over non-integral q₀ ⇒ π(S(Q)) ⊋ Z ≠ Z.
- **NEW MEASUREMENT (audit)**: HP is **TRUE for the demo pair** — first hit q₀ = 4/3 (f = 25/9 square ⇒ fiber split; 1035/6662 ≈ 15.5% of tested (a,b) give everywhere-soluble fibers). The doc only demonstrated insolubility (the wall); the kill is also **operative**, not vacuous.

## Claim 4 — Theorem B0 (L123–137)
- BL* statement (L125–128) matches the paper's "Bombieri-Lang Conjecture" (v1 wording nearly verbatim; v2 swaps "≥1-dim/non-trivial" for "positive-dimensional/non-constant" — cosmetic).
- "No infinite subset of Z existentially definable in Q" = v1 **Thm 20** = v2 **Cor 23**, verbatim content ✓. Deduction to score = ∞ is one line and valid: any finite-k construction existentially defines the infinite set Z ⇒ contradicts the corollary. Quantifiers fine.
- "Sharpening" (Thm 2(a) supplies Lemma 19's density hypothesis unconditionally): valid, **but needs one unstated line**: the surviving Q-irreducible factor is automatically absolutely irreducible (if geometrically reducible, Q-points lie in the codim-2 intersection of conjugate components ⇒ finite π-image, contradicting the infinite hypothesis). Koe16's own Cor-23 proof performs exactly this reduction ("this ensures that the irreducible components V of W̄ are geometrically irreducible"); the lane should import it. GAP-NAMED (minor).
- Numbering: cite the revision (see CORRECTIONS.md) — L136's "Annals 183 (2016) 405" is also wrong on pagination (published: 73–93).

## Claim 5 — Conjecture G (L149–159)
- **WELL-POSEDNESS: GAP-NAMED.** "Split fibers" is ambiguous: in genus-one-fibration usage "split" attaches to the fibration (section) or isotriviality. The intended meaning, per L146 ("fibers have Q-points exactly over Z"), is **"the fiber has a Q-rational point"** — state this in the conjecture. With that definition, and "given by one polynomial" = a hypersurface in A³_Q with π the q-projection, the statement is well-posed.
- Literature-silent claim (L152–159): **survives spot-check.** 2025-era activity is adjacent but none of it controls the exact split-fiber set of a genus-one fibration (statistics of local solubility for families of quadratic forms/Fermat curves; Hasse-norm-principle statistics; Campana-point local-global) — no finite norm-type description exists in the literature, and Sha-specialization results (soluble-but-pointless fibers in positive proportion in elliptic-curve families) confirm torsor-class specialization is genuinely not norm-controlled. Since Conjecture G false ⟺ a k=2 genus-one candidate ⟺ Z existentially definable, neither direction can currently be settled unconditionally — silence is the correct state.

## Claim 6 — valuation lens (L162–197)
- **(i) GAP-NAMED**: L171–172 "a binary form in 2 witnesses … its solubility has **no local-global content** — square-class conditions only" is **wrong as stated**: solubility of x² − a(q)y² = c is precisely a Hasse-norm condition — the quaternion (a(q), c) splits ⟺ Hilbert symbol +1 at every place. What is true and kills the natural folds: membership in N(Q(√c)) depends only on the square class of a(q) (norm groups contain all squares) and constrains only primes dividing 2c·a(q); the square-class invariance makes integrality-in-q unrepresentable for folds like a(q) = q (q and q/4 share a class). But **no general impossibility proof for arbitrary polynomial a(q) is given** — "structurally dead at k=2" (L167) is a verdict, not a theorem. Corrected status: "dead for the natural folds; general case open, and any live fold would still face the Thm 3(iii) numerator wall and Thm 2(c)".
- **(ii) VERIFIED**: t ≥ 0 ⟺ 4 squares (Lagrange); 3 squares fail (Legendre: t = 3 squares ⟺ t ≠ 4^k(8m+7), and the obstruction class is invariant under multiplication by squares, so no 2-slot scaling trick exists); MRDP-style bound-carrying has no 2-witness home; consistent with Thm 2(d) (a 4-square SoS is itself an SoS assembly). Lane refs B7/B8 are internal and were re-derived from first principles here instead.

## Claim 7 — numeric artifact (L248–255)
RECHECKED: 7/7 denominator-prime matches and 3/7 wall demos reproduce exactly (run_original.txt). Script notes: dead placeholder line (hilbert_check.py:26, computes `pow(-1,…,2)` and discards it), typo "INSOLEUBLE" (:77), and only 7 sampled points. Independent re-verification (audit_numeric.py): closed form 344/344 on a random grid; small-print breakage demonstrated; HP-hits found (arm C). Tool output vs doc claim: **match**.

## Verdict table
| # | Claim | Verdict |
|---|---|---|
| 1 | Lemma 1 | VERIFIED (2 proof footnotes) + citation-numbering defect |
| 2 | Thm 2(a) | VERIFIED |
| 2 | Thm 2(b) "every curve" | GAP-NAMED → "every horizontal curve" |
| 2 | Thm 2(c) unirational / "not ruled" | VERIFIED / overclaim to drop |
| 2 | Thm 2(d) SoS dead | VERIFIED |
| 3 | Thm 3(i) | conclusion VERIFIED, proof line garbled (fix: cofinite-image kill) |
| 3 | Thm 3(ii) | VERIFIED |
| 3 | Thm 3(iii) closed form + wall | VERIFIED (state p ∤ 2f_Dg_D; confirmed load-bearing) |
| 3 | HP(P) statement/honesty | VERIFIED; HP **true** for demo pair (new measurement) |
| 4 | Thm B0 | content VERIFIED; numbers are v1's; + 1-line abs-irreducibility gap |
| 5 | Conjecture G | well-posed once "split" = "has a Q-point"; literature-silent survives |
| 6 | lens (i) binary norm dead | GAP-NAMED (mechanism misstated; verdict plausible, unproven in general) |
| 6 | lens (ii) positivity ≥ 4 | VERIFIED |
| 7 | numerics | VERIFIED + strengthened |
