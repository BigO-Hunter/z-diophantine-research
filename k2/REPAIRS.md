# REPAIRS.md — audit-repair pass on FRONTIER.md (post 91f9fb5/b4c164b)

Audit: ~/bigo-campaign/dzq-k2-audit/ (AUDIT_K2.md + CORRECTIONS.md), verdict
9 VERIFIED / 5 GAP-NAMED / 0 REFUTED. Author applied all owed repairs; history
preserved (this commit is additive; no silent deletion — every replaced passage
is named here with its disposition). **Rebuttals: none** — all six mechanical
repairs, the citation pin, and the addendum accepted on the audit's evidence
(C4's cofinite kill is strictly stronger than the original garbled line; C7
correctly identified the misstated mechanism).

| # | Item | Repair applied | Where |
|---|---|---|---|
| 1 | Thm 2(b) overclaim "every curve" | inserted **horizontal**; vertical-curves caveat added; proof line aligned; downstream uses re-scoped ("multisection covering infinitely many integers") | Thm 2(b) stmt+proof, frontier ¶, Horn B ¶ |
| 2 | Thm 3(i) garbled equivalence | replaced with audit's cofinite-image kill (∃w₁[A≠0 ∨ B=0]; A≢0 ⇒ cofinite ⊋ Z; A≡0 ⇒ Lemma-1 curve kill) | Thm 3(i) |
| 3 | Thm B0 abs-irreducibility gap | one-liner added (factor with infinite π-image is automatically absolutely irreducible; codim-2 conjugate-intersection argument), mirroring Koe16's own reduction | Thm B0 mechanism ¶ + ledger |
| 4 | lens (i) overreach | "structurally dead" → "dead for all natural folds; general case open"; mechanism corrected: binary fold IS a Hasse-norm condition; real obstruction = square-class invariance + finite-index norm group; surviving folds still face Thm 3(iii) wall + Thm 2(c) | lens (i) |
| 5 | Conjecture G well-posedness | "split fiber" defined = has a Q-rational point (trivial torsor class), explicit not-split-as-fibration caveat; "one polynomial" = hypersurface in A³_Q with π the q-projection; added G-false ⟺ k=2 exists ⟺ Z ∃-definable | Conjecture G |
| 6 | Thm 3(iii) small print | p ∤ a·2·f_D·g_D stated in the theorem itself; load-bearing note (audited 32/32 failures when p | f_D); such primes folded into the finite CRT choice | Thm 3(iii) bullet |
| C1 | citation pin | all [Koe16] pointers repinned to **arXiv v1** numbering; new **Citation-revision map** section (v1 Lemma 19/Thm 20 = v2 Lemma 22/Cor 23; v2's "Lemma 19" unrelated; published Annals 183 (2016) **73–93**, was wrongly "405"); ledger rows repinned | header, Lemma 1 status, Thm B0, new map section, ledger |
| C9 | HP addendum (audit-sourced) | HP(F,G) TRUE for demo pair: q₀ = 4/3 explicit hit, 1035/6662 ≈ 15.5% soluble — Thm 3(iii) kill operative, not vacuous; labeled "source: audit" | Thm 3(iii) |
| — | Lemma 1 remark | audit Claim-1 footnotes folded in: genus-0 arm needs C(Q) ≠ ∅ + geometric integrality; geometrically-reducible case holds a fortiori; singular → normalization | Lemma 1 |
| — | Thm 2(c) "not ruled" | dropped per C3; restated as the correct stronger form (no dominant U from any Y with a rational curve along which π∘U is nonconstant) | Thm 2(c) |
| — | script hygiene | dead placeholder line removed (hilbert_check.py), typo INSOLUBLE fixed; behavior re-verified identical (7/7 + 3/7) | hilbert_check.py |

Nothing in the audit's "Unchanged / confirmed as-is" list was touched.
Post-repair package status: same theorem content, tightened statements, correct
revision-pinned citations, operative kill measurement recorded.
