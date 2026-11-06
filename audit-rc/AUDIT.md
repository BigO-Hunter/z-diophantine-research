# AUDIT — hyp:RC gap finding, hardened against quartic_4973.tex (Version 4, 2026-11-06)

Source: `~/bigo-campaign/diophantine-zq/upstream/quartic_4973.tex` (719,455 bytes, sha256 of
companion coefficient table matches README). All line numbers below are line numbers of that file.

## VERDICT: CONFIRMED-GAP — mechanism revised; deep validity = UNRESOLVABLE-WITHOUT-X

The construction-lane finding survives: **the bridge from `corank Sel = 1` to
`ord_{s=1} L(E_ℓ,s) = 1` is not closed by any cited, established mathematics anywhere in the
manuscript.** Two parts of the finding's stated mechanism are WRONG and must be corrected before
any delivery:

1. WRONG: "their section never attempts the analytic upper bound." They DO attempt it — via their
   own constructed "(O.8) visibility implication" (below), not via Gross–Zagier/Kolyvagin.
2. WRONG: "stated as a theorem ... so it is an inherited assumption." hyp:RC is NOT presented as an
   inherited conjectural input; the manuscript claims it is PROVED (line 1029–1031: "Theorem
   hyp:RC is proved in Sections sec:rc–sec:limits, with its coefficient and normalization
   arguments in Appendices app:even-source–app:endpoints"). So the honest-conditional defense does
   not apply at manuscript level. It DOES apply at the Lean/release level (their README: the main
   bounded-polynomial declaration "still contains `sorry`"; certificate checks "do not prove the
   source system's arithmetic characterization"; thm:quartic, line 8691: "With precisely the
   inherited arithmetic hypotheses and qualifications").

## Verified evidence

### The statement (verbatim, lines 1020–1027)
```
\begin{theorem}[Restricted converse, RC]\label{hyp:RC}
For every positive squarefree ℓ ≡ 11 (mod 12),
  corank_{Z₂} Sel_{2^∞}(E_ℓ/Q) = 1 ⟹ ord_{s=1} L(E_ℓ,s) = 1,
\end{theorem}    [E_ℓ: y² = x(x−ℓ)(x+3ℓ), stated line 1000–1002]
```

### GZ/Kolyvagin are genuinely absent from the RC proof chain
Grep counts in lines 1775–5759 (sec:rc through sec:limits; 200,048 chars — the construction lane
said "133k-char", likely a narrower range or the handoff's separate section file; same ballpark):
**Gross 0, Zagier 0, Kolyvagin 0, Heegner 5, Waldspurger 1, Kato 5, ultrafilter 8.**
(Our lane earlier recorded "Gross 2, Zagier 2, Kolyvagin 2" — those hits are OUTSIDE the RC range:
`gz`/`kolyvagin` are cited only in `lem:forward-rank` (line ~1093–1113, in sec:pole) for the
OPPOSITE direction — "If ord L = r ≤ 1, then rank = r and Sha finite" via BCDT + Kolyvagin Thm 1 +
Kato Cor 14.3 — and in the bibliography.)

### The parity step is real and correctly used (a theorem, not the gap)
Line ~1808–1812: Selmer parity theorem, Dokchitser–Dokchitser Thm 1.8, "gives root number −1 under
the left side of (RC). This application does not replace Selmer corank by Mordell–Weil rank and
does not assume finite Sha." So: corank 1 (hypothesis) → root number −1 → ord L odd. As our lane
said: odd alone gives 1 or 3 or 5 or ….

### The only bridge: the self-defined "(O.8) visibility implication"
Application site, lines 2596–2603 (verbatim):
```
If the intrinsic odd limit symbol is a unit at the empty configuration,
choose an actual stage carrying that value with M_θ > δ_o. The index D=1
lies in every moving support and then satisfies v₂a_{M_θ}(1) = δ_o < M_θ.
The visibility implication (O.8) gives ord_{s=1}L(E,s)=1, which is
exactly (RC). No final companion or determinant bound is needed in this case.
```
The "implication" is a manuscript-internal display (O.8), Proposition `ex:app-visibility`
("Visibility and the native genus index"), lines 13055–13087, tag at 13084 (verbatim):
```
v₂a_M(D) < M ⟹ ord_{s=1} L(E^D,s) = 1   and   j_gen(D) ≤ v₂a_M(D) + C_det.
```
Its proof (~30 lines, 13061–13087) rests on (O.7), a "native rank-one free lattice", and the
sentence "the first inequality below holds for a known simple-zero D; **the visibility implication
holds for every admissible D**" — the central analytic nonvanishing step is asserted in one clause,
deriving ord L = 1 for an infinite twist family from 2-adic valuation data. If valid, (O.8) alone
would be a first-class result in arithmetic geometry; it cites no external theorem that gives it.

### The supporting machinery is nonstandard and self-contained
Load-bearing devices in the RC chain: "fixed-form Euler-system calculation" (1816), "intrinsic odd
limit symbol", "native genus index", and **nonprincipal ultrafilters** as stage-limits (lines
2557, 2560, 2627, 4418, 4459–4460, 4696, 4836, 13801–13807 — e.g. 4418 "One fixed nonprincipal
ultrafilter gives a diagram over Λ", 13807 identities "on a set in this same ultrafilter").
No cited source introduces this framework; the RC proof's assembly inputs are unpublished generated
files (source map, line 10290: S17 `z-in-q-restricted-converse-assembly.txt`, "RC assembly inputs";
S18/S29/S30/S32 frozen .tex). README: manuscript "produced by Elliot Glazer with Astra 6, Sol 6.1,
and Opus 5.5, with auditing from Fable 5.1"; "AI review and successful finite checks do not
constitute independent human peer review".

### Final claimed step (verbatim, ≈5746–5753)
```
Hence L'(E/K,1) ≠ 0. The complementary value L(E^{(k)},1) is nonzero, and
L(E/K,s) = L(E,s)L(E^{(k)},s), so E has analytic rank one.
This proves (RC), and hence Theorem hyp:RC, using the classical
applications and finite constructions specified above.
```

## Why CONFIRMED-GAP and not NO-GAP
NO-GAP would require the RC chain to be a proof in the ordinary sense: every load-bearing step
either classical or clearly derived. The entire analytic-rank conclusion funnels through (O.8) and
the ultrafilter framework — uncited, unpublished, machine-generated, never reviewed — establishing
a Gross–Zagier-scale statement for an infinite family. The claim `hyp:RC` is therefore
unestablished by the standards of published mathematics; the quartic construction is conditional on
it in exactly the way the Lean `sorry` encodes. Sub-structure: *the deep validity of (O.8) and its
supporting chain is UNRESOLVABLE-WITHOUT X, X = expert human audit of sec:rc–sec:limits +
app:even-source + app:endpoints (~250k chars of original arithmetic).*

## What must NOT be claimed publicly
- "They never attempted the upper bound" — false; (O.8) is the attempt.
- "They assume RC without proof" — false at manuscript level; conditional at Lean level (disclosed).
- "The proof is wrong" — unverified; we can only say: load-bearing steps are outside the cited
  literature, unreviewed, and would each be significant original results.
- Count corrections: Gross/Zagier/Kolyvagin = 0/0/0 (not 2/2/2) in the RC chain; RC section ≈ 200k
  chars in the .tex (lane said 133k).
