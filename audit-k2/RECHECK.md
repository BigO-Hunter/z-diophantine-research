# RECHECK.md — numeric re-verification evidence (independent implementation)

Source: ~/bigo-campaign/dzq-k2/hilbert_check.py @ b4c164b, copied verbatim (run_original.txt).

## 1. Re-run of the original tool — map vs doc
```
q0=1/3 p=3 e=1: predicted +1, actual +1  OK
q0=5/7 p=7 e=1: predicted +1, actual +1  OK
q0=11/6 p=3 e=1: predicted +1, actual +1  OK
q0=23/15 p=3 e=1 / p=5 e=1: +1/+1 OK
q0=7/35 p=5 e=1 / p=7 e=1: +1/+1 OK
all denominator-prime predictions match          -> 7/7  (FRONTIER.md L250 claim ✓)
wall demonstrated at 3 of 7 sample points        -> 3/7  (L252–255 claim ✓)
```
Doc claim = tool output. No inflation.

## 2. Independent verifier (audit_numeric.py — own Hilbert-symbol code, sympy only for factorint)

**Arm A — closed form vs direct symbol, randomized (stricter than the doc's 7 points).**
(f,g) = (q²+1, q+3), 400 random (a,b), gcd=1, odd p | b, p ∤ 2f_Dg_D:
`344/344 match`. The L92–94 closed form is correct.

**Arm B — small-print stress: the formula when p | f_D.**
f = 3q²+1 (f_D = 3), g = q+1, p = 3: `32/32 mismatches`. The reduction F̃(a,b) ≡ f_D a^{D_f} (mod p) requires p ∤ f_D; the doc's "good Chebotarev class" dodge is **load-bearing**, and its demo pair (f_D = g_D = 1) honestly avoids the issue (L252). Repair: state "p ∤ 2f_Dg_D" explicitly in the L96 block.

**Arm C — HP(F,G) for the demo pair (new measurement; the doc never tested this side).**
Searched b odd ∈ [3,120], a < 2000, a ≡ 1 (mod rad b), gcd(a,b)=1, fiber nondegenerate; solubility = Hilbert symbol +1 at every odd prime, at 2, and at ∞:
```
checked 6662 candidates: soluble-fiber hits = 1035 (15.5%), locally insoluble = 5627
first HP hit: q0 = 4/3     (f(4/3) = 25/9 = (5/3)^2  =>  point (5/3, 1, 0))
```
**HP(F,G) is TRUE for (q²+1, q+3).** Consequence for Thm 3(iii): the per-construction semi-decision kill (L119–120) is demonstrably operative — a conic bundle over this (f,g) provably has soluble fibers over non-integers, so it can never satisfy π(S(Q)) = Z. The doc demonstrated only that the wall (insolubility) is real; both sides of the wall are now measured.

**Script-quality notes on the original tool (no effect on results):**
- hilbert_check.py:26 — dead placeholder `r = pow(-1, …, 2)` computed and never used.
- :77 — typo "INSOLEUBLE" (cosmetic).
- Only 7 denominator-prime points and 7 wall samples; arms A–C above supply the statistical depth the artifact lacked.
