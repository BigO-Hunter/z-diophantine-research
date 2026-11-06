# SEAMS — exact chains and usage points (quartic_4973.tex line numbers)

## Chain: RC → PC → pole-predicate → quartic

1. **`lem:pole`** (One-sided obstruction, 1004–1015). Short soundness proof (parity of v_p on the
   cubic at a unit parameter) — verified as written; cheap direction only.
2. **`hyp:PC`** (Pole completeness, 1016–1019): for rational B with square reduced denominator,
   0<B<1/2, v_p(B)≥4 ∀p∈S₀ ⟹ Φ(B).
3. **PC proved FROM RC**: 1032 "We now prove Theorem~hyp:PC from this restricted converse.";
   descent reduction 1034–1136; two applications of RC at 1123 ("Applying Theorem~hyp:RC to both
   n and nθ, Lemma~lem:forward-rank gives rank one and finite Sha, hence Sha[2]=0"); concludes
   1135–1136 "This proves Theorem~hyp:PC, with both restricted-converse applications in their
   stated domain." **PC inherits RC's gap entirely.**
4. **RC proof chain**: claimed at 1029–1031; strategy 1816–1822 ("fixed-form Euler-system
   calculation → varying-companion arithmetic estimate → genus-point lower bound → normalization
   → fixed-field determinant argument excludes a zero derivative"); parity input ~1808 (DD Thm
   1.8); even scalar 1840+; Kato 13.4(2) at 1899; genus bound 2418; odd forms 2475; **(O.8)
   applied at 2596–2603**; Heegner-descent subsection 2849+; limits/ultrafilters 4397–5758;
   determinant clearing 5501; conclusion ≈5746–5753. Appendices: app:even-source 10472+,
   app:endpoints (carries (O.2)/(O.7)/(O.8)/(F.4), e.g. 13084, 13828).
5. **Pole predicate → polynomial**: sec:pole 988–1136; seven-variable pole lemma `hyp:o8-pole`
   7536+ "proved from Theorem~hyp:RC; it is not inferred from Theorem~hyp:PC, which has different
   variables and a restricted completeness domain" (6646–6648) — the manuscript's own domain caveat.
6. **Quartic**: `thm:quartic` 8691–8706 ("With precisely the inherited arithmetic hypotheses and
   qualifications of Section~sec:degree8-original and Appendix~app:sources"); proof 10208–10229
   via `thm:quartic-selected-source` + certificate; boundary statement 10231–10233: "The finite
   checks do not replace the inherited rank, height, prime-pattern, formal-group, norm or pole
   arguments." Sec:v4-inherited (9117–9205): "the restricted converse, rank and original
   arithmetic assertions retain their stated proof status"; "None of the finite source or
   polynomial checks strengthens these assumptions."

## Seam 2: hyp:o8-height — REAL burden, HONESTLY DISCLOSED (no smuggling)

- Statement 6670–6682: h(a) ≤ H_*·M₅(a)²⁴ ∀a∈Q∖𝒟, H_* = 2(4608^165888+6^100)(∏_{p≤76176}p)²⁴+128,
  log₂H_* < 4,783,227. Claimed proof 6690–~7499 (Shimura curve X of discriminant 210, g=5,
  Atkin–Lehner quotients, Gonzalez-Jiménez-Rotger models, Riemann–Hurwitz branch deduction,
  CM estimate "over the same fiber field").
- Self-disclosure #1 (6645, before the statement): "The finite coefficient calculation does not
  establish the height bound."
- Self-disclosure #2 (7500, after the numeric log₂ computation): "This is a check of the number H,
  not a proof that H is a height constant."
- Reading verified in context: caveat #2 qualifies the NUMERIC bound (size of H), not the
  inequality; the inequality rests on the ~800-line claimed proof. Caveat #1 qualifies the
  polynomial certificate. Both are the authors' own boundary statements — our audit CONFIRMS the
  disclosed conditionality; it does not expose a hidden one.
- Propagation into the quartic: `thm:quartic-height19` (8738–8750) reuses S_*, 𝒟, M₅ from
  hyp:o8-height and claims the sharper h(a) ≤ H₁₉·M₅(a)¹⁹, log₂H₁₉ < 2,093,966; consumed via
  sec:v4-inherited 9160–9163 ("This is H₁₉ of Theorem~thm:quartic-height19"). So the height seam
  sits on the quartic's critical path through sec:degree8-original → sec:quartics.

## Verification status of each manuscript link (this audit)

| link | text verified | proof verified |
|---|---|---|
| lem:pole | yes (1004–1015) | yes — short, coherent |
| corank/parity inputs | yes (1093–1136, 1808–1812) | yes — cite DD Thm 1.8, Cassels–Tate; standard |
| hyp:RC statement | yes (1020–1027) | **no — (O.8)+ultrafilter chain unreviewable here** |
| hyp:PC from RC | yes (1032–1136) | conditional on RC |
| hyp:o8-height | yes (6670–6682) | **no — ~800-line Shimura-curve claim unreviewable here** |
| thm:quartic conditional structure | yes (8691, 9117–9205, 10231) | honest (Lean `sorry` disclosed in README line 58) |
