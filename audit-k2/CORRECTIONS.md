# CORRECTIONS.md — what the original lane got wrong, with corrected statements
Each item: the defect, why it matters, the fix. None undermines the package's main results;
all are one-to-three-line repairs except the citation pin.

## C1 (biggest defect). Koenigsmann citation numbers point at a revision that no longer exists
- FRONTIER.md L11, L30–31, L128–130, L136, L236 cite "[Koe16, Lemma 19]" (n=1, Siegel) and
  "[Koe16, Thm 20]" (no infinite exists-definable subset of Z), pinned to arXiv:1011.3424 and
  "Annals 183 (2016) 405".
- Measured facts: **arXiv v1** has exactly these numbers and the lane's quotes are verbatim-correct
  there ("For n=1 the Lemma holds unconditionally, by Siegel's Theorem."). **arXiv v2** (= accepted
  version, Oxford ORA copy) renumbered: the density lemma is **Lemma 22**, the corollary is
  **Corollary 23**, and v2's "Lemma 19" is an unrelated diophantine lemma (R_p^[1], no curves, no
  Siegel). The **published** version is Annals **183 (2016) 73–93** (not p. 405) and renumbered again.
- Risk: any auditor pulling the modern arXiv finds no Siegel lemma at Lemma 19 and can mistake the
  cross-validation for fabrication.
- Fix (one line): cite as "arXiv:1011.3424**v1**, Lemma 19 & Thm 20 (= v2 Lemma 22 & Cor 23;
  Annals 183 (2016) 73–93, where the BL-material numbering differs again)".

## C2. Theorem 2(b) overclaims "every curve"
- L40–41. Corrected statement: "**Every horizontal curve** C ⊆ S (π|C nonconstant) has C(Q)
  finite; hence no rational section, no rational/elliptic multisection that covers infinitely many
  integers, and no horizontal curve with infinitely many Q-points." Vertical curves in fibers over
  q ∈ Z are not excluded by π(S(Q)) = Z and are not used downstream. All cited uses (L141–146)
  survive verbatim.

## C3. Theorem 2(c) "not ruled" is unsupported
- L44. Keep only "S is not unirational over Q" (proved); the same line-restriction argument
  additionally kills any dominant U: Y ⇢ S where Y carries a rational curve on which π∘U is
  nonconstant — state that if "ruled" is wanted, or delete the word.

## C4. Theorem 3(i) proof line is garbled (conclusion true, kill even stronger)
- L76–79. Corrected: for P = A(q,w₁)w₂ + B(q,w₁), solubility ⟺ ∃w₁ [A(q,w₁) ≠ 0 ∨ B(q,w₁) = 0].
  If A ≢ 0 then π(S(Q)) ⊇ {q : A(q,·) ≢ 0}, a **cofinite** subset of Q — cofinite ⊋ Z, dead
  immediately (no Lemma 1 needed). If A ≡ 0, P = B and the plane-curve/Lemma-1 argument applies.

## C5. Theorem 3(iii): state the small print on leading coefficients
- L92–96. The closed-form reduction requires p ∤ 2·f_D·g_D (else F̃(a,b) ≡ 0 mod p and
  v_p(f(q₀)) ≠ −e·D_f; measured: 32/32 formula failures with f_D = 3, p = 3). The "good class"
  absorbs this; make it explicit: "for p | b with p ∤ a·2·f_D·g_D".

## C6. Thm B0 "seamless" combination needs one line: absolute irreducibility
- L132–135. Lemma 19/22 requires f absolutely irreducible; Thm 2(a) supplies density for the
  Q-irreducible factor. Add: "an irreducible-over-Q factor with infinite π-image is automatically
  absolutely irreducible (otherwise its Q-points lie in the codim-2 intersection of conjugate
  components, giving finite π-image)". This is exactly the reduction Koe16 performs in the proof of
  v2 Cor 23 / v1 Thm 20.

## C7. Lens (i): "no local-global content" is the wrong mechanism
- L171–172. Corrected statement: a binary fold x² − a(q)y² = c is soluble ⟺ the quaternion
  (a(q), c) splits ⟺ c ∈ N(Q(√a(q))) — this IS a local-global (Hasse-norm) condition. What is
  true: membership depends only on the square class of a(q), and N(Q(√c)) is a finite-index
  subgroup constraining only primes dividing 2c·a(q). Hence the obvious folds die (a(q) = q: q and
  q/4 share a class; square classes cannot see integrality), but **no general impossibility theorem
  for arbitrary polynomial a(q) is proved** — downgrade "structurally dead at k=2" to
  "dead for all natural folds; general case open, and any surviving fold still faces the Thm 3(iii)
  numerator wall and Thm 2(c)".

## C8. Conjecture G: define "split fiber"
- L149–150. Insert: "a fiber is **split** if it has a Q-rational point (trivial torsor class);
  π has no section is NOT implied — the fibration need not be split as a fibration." Also state
  "given by one polynomial" = a hypersurface in A³_Q with π the q-projection. After this, the
  conjecture is well-posed and matches L146's "fibers have Q-points exactly over Z".

## C9. HP status upgrade (measurement, not correction)
- L117–118 says "HP is open in general … provable in individual instances by finite search".
  Audit measured HP(F,G) TRUE for the doc's own demo pair (first hit q₀ = 4/3; 1035/6662 soluble
  candidates) — the doc's numeric section never exercised this side. Add: "for the displayed pair,
  HP holds (q₀ = 4/3 is an explicit witness), so the Thm 3(iii) kill is operative, not vacuous."

## Unchanged / confirmed as-is
Lemma 1 statement & genus-0 engine; Thm 2(a),(d); Thm 3(ii),(iii) closed form; HP honesty of
labeling; lens (ii); numeric claims 7/7 and 3/7; literature-silence around Conjecture G.
