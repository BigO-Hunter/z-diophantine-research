# RACE_NOTES — board row `z-diophantine-in-q`, captured state

Provenance snapshot (verbatim from the race page and site history, captured 2026-11-06 ~16:20Z
by the campaign gate pass — source shelf file: `diophantine-zq/GATE_NOTES.md`). The Discord/ranking
section of the original notes is not reproduced here (private-coordination channel detail).

## Verbatim statement (race page)

> A polynomial $P(q,w_1,\dots,w_k)$ with integer coefficients defines $\mathbb Z$ in $\mathbb Q$ when, for every rational number $q$, $q$ is an integer exactly when $P(q,w_1,\dots,w_k)=0$ for some rational numbers $w_1,\dots,w_k$. The polynomial must be explicit: a public list of its terms, or a public program that writes them out. The score is the number of variables, $k+1$. Fewer variables rank higher; on a tie, a lower degree ranks higher, then fewer nonzero terms, then a smaller largest absolute coefficient. Koenigsmann (2016) showed that $\mathbb Q\setminus\mathbb Z$ is Diophantine in $\mathbb Q$. Whether $\mathbb Z$ itself is Diophantine in $\mathbb Q$ was open, and Mazur's conjectures (1992) predicted that it is not.

## Verbatim policy bits (race page + site commit message)

- Evidence levels: **Claimed** = "The result is published, but no review repository accepted it and we have not checked a Lean proof." **Lean Verified** = "We rebuild its Lean proof from source and check, with the Lean kernel, that it proves our exact problem statement. A result also counts when prove2.me ... proved it and we reviewed that its Lean statement is our problem statement."
- Site commit message: "No baseline: no Diophantine definition existed before ... The rows, all Claimed (no review repository; the Lean development's main theorem still has a sorry)".
- Explicitness rule: public term list OR public program that writes the terms.
- Submission route observed: publish in a GitHub repo/release; the site lists rows from repo artifacts. The race board (board.bigospeedrun.com/other-z-diophantine-in-q) is the community thread — **empty as of 2026-11-06 ~16:05Z ("No posts yet")**.

## Refresh (2026-11-06 ~19:40Z, fetched from the live page; "Data updated Nov 6, 11:36 AM PT")

The leaderboard moved ~4h after the capture above. Current verbatim ranking order on the page:
"Results rank by degree first, lower is better; then by the number of variables, $k+1$; then by
the number of nonzero terms; then by the largest absolute coefficient. A stated upper bound,
such as degree below $2\uparrow\uparrow 7$, counts as that value. Degree 4 is the lowest possible
for one defining polynomial (Brox, and the Version 6 manuscript of Glazer and others), so among
quartics the number of variables decides."

| Rank | Vars | What | Source | Date |
|---|---|---|---|---|
| 1 | **962** | Version 6: degree 4, 55,409 nonzero terms, max coeff 64·3^(2^28) (constant S = 3^(2^27)); builds on a reconstruction of Jose Brox's public notes; collective agentic notes of the **eight** authors | release `quartic-962-version-6`, commit `a9e834ba` | Nov 6, 9:51 AM PT |
| 2 | 1,272 | Version 5 | release `quartic-1272-version-5` | Nov 6, 9:10 AM PT |
| 3 | 1,315 | Jose Brox's repo (smallest quartic; conditional polynomial presentation taking the Glazer arithmetic inputs as given) | JoseBrox/diophantine-z-q_improvements | Nov 6, 8:33 AM PT |
| 4 | **4,973** | **Version 4 — the row independently verified in `verification/`** | release `quartic-4973-version-4` | Nov 6, 7:33 AM PT |
| 7 | 41 | Jose Brox, finite-fibre construction: degree < 2^9,566,673, coefficient-graph form; conditional on the Glazer arithmetic inputs + Sun's prime-pattern theorem (arXiv 2610.20691) | JoseBrox repo | Nov 6, 8:33 AM PT |
| 8 | 211,983,774,909 | qqwref PR #1 (merged in his fork) | qqwref/diophantine-z-q | Nov 5, 3:50 PM PT |
| 9 | 292,890,231,905 | Agent breakthrough (Glazer) | repo | Nov 4, 11:50 AM PT |

All rows still **Claimed**. New board facts relevant to the research note: (i) a degree-4 lower
bound for one defining polynomial is now public (Brox; v6 manuscript); (ii) Glazer states that
with unlimited degree a definition with under 100 variables is within reach, so the open
question is the fewest variables of a quartic; (iii) the author list grew to eight
(+Stefan Baranczuk, +Jose Brox). The page's per-row proof-scope note stands: the certificate
check shows the polynomial is equivalent to the manuscript's equation system; it does not check
the arithmetic argument; the Lean development is incomplete.
