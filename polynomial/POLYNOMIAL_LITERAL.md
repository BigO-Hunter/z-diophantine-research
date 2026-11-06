# POLYNOMIAL_LITERAL.md — the assembly, now fully literal (no open constant)

**One line: every constant in F is computed and machine-checked, and every leaf factor is emitted as
a hashed sparse term list with a straight-line evaluator that provably agrees with it. The single
open item left is representational, not mathematical: the top-level product/square is left as a
product (expansion measured infeasible).**

    F = (F_main · F_patch)² + (X·ι − 1)²
    F_main  = F_Φ² + F_Θ²
    F_Θ     = ∏_{τ∈Λ} [ (δ_τ·ζ − 1)² + P̂_τ² + ((D·ζ′ − 1)·P₀_τ)² ]
    F_patch = ∏_{p∈Π} [ π_p·G_p(y,r,s) − p²·X² ]

    Λ = (1, 17, 33, 49, 3, 11, 19, 27)     4 parameters for each of the 2 local classes
    Π = (2, 3, 5, 7, 11, 13, 17, 19, 23)   E_exc ∪ {2}  (8 exceptional + the adjoined m_2)
    S = {2}, u = 1, π = 2, z = ι³, ι = 1/X

## 1. What changed in this continuation (three corrections, all measured)

| # | earlier draft | now | why |
|---|---|---|---|
| 1 | z = X³ in the h-bridge term | **z = ι³** | the polynomial defines ⋃m_w's *inverse image* (Sun (1.1) duality); ⋃_w m_w ⊊ Q∖Z (1/3 ∈ Q∖Z ∖ ⋃m_w), so the un-inverted reading defines too small a set. `SMOKE2 §7` |
| 2 | F_p = πX²G − 1 | **F_p = π_p·G_p − p²X²** | the O_(p) formula applies to x = 1/(pX); cleared it is π G = p²X². The old form fires for v_p(X) ≥ 1 instead of v_p(X) ≤ −1 (`SMOKE2 §1`) |
| 3 | patch over "T", 1 prime computed | **9 primes, all computed** | E_exc = {3,…,23} (8, forced by \|κ\| ≤ 25) and m_2 is adjoined because S₀ = ∅ (`E_EXC.md`) |

## 2. Λ: eight parameters, two classes — not 512, not 4

The freezing layer needs four parameters per local class (Sun's pigeonhole: four distinct residues,
three forbidden values {0,±1}):

* class A = {v₂(c) ≤ 2}: **1, 17, 33, 49** (≡ 1 mod 16);
* class B = {v₂(c) ≥ 2}: **3, 11, 19, 27** (≡ 3 mod 8).

All eight verified to serve their whole class exhaustively (0 obstructions; `E_EXC.md §2`). The
derivation lane's `|Λ| ≤ 512` (4 per mod-8 cell) is superseded: the correct cover is 2 classes × 4
parameters = **8**.

## 3. The emitted leaves (all sha256-pinned, artifact-lane sparse format)

Format: `# comment` header, then `<coeff> <var>:<exp> ...`, sorted by sparse key.
Variables `0=X 1=a 2=b 3=y 4=r 5=s 6=ζ 7=ζ′ 8=b₁ 9=σ 10=υ 11=ι`.

### Freezing + trace-sum leaves

| object | terms | degrees (ι,a,b,y,r,s,ζ,ζ′,b₁,σ,υ) | sha256 |
|---|---|---|---|
| `phi2.terms.txt` — F_Φ | 11 | 0,2,2,0,0,0,0,0,2,2,2 | `6e8c6af48996e85348a9e65f3111124978ab95b946dece3ccc328109de682c76` |
| `Phat_tau1` | 103 | 12,14,8,2,2,2 | `7c893e36ef8dc9388f141c34e3982d402c421da4e41aea550939911b859a9cec` |
| `Phat_tau3` | 116 | 12,14,8,2,2,2 | `ee1a4f94b95ce6f1be4d833c44e91692cd7ffea33437ada9ad8223116f32e788` |
| `Phat_tau17` | 116 | 12,14,8,2,2,2 | `c95f3e57c6eedbfd0f8037ff4e1b641379406283e2713ecb39ccf7fa511023f6` |
| `Phat_tau33` | 116 | 12,14,8,2,2,2 | `d1e3658206bc3cc09fd0ef8be3018a8e54a180d886bb5c24277c596954562879` |
| `Phat_tau49` | 116 | 12,14,8,2,2,2 | `4d26a7015f5300a11a56184e5eb7374e98d9adbde87ace548729fc7bef5127c2` |
| `Phat_tau11` | 116 | 12,14,8,2,2,2 | `382786674c1afcb96d47d634429ad02fbfc9d0918c969fcf698e71f917996d00` |
| `Phat_tau19` | 116 | 12,14,8,2,2,2 | `ed737c81ead30e00db39a008df17b896e5485d85ad53361ece9bb6bd7af1aeda` |
| `Phat_tau27` | 116 | 12,14,8,2,2,2 | `dd74bc898fe17627b61781b25933a35bf525f43b0628e244fc16b111cea4c3c2` |
| `P0_tau{1,3,11,17,19,27,33,49}` | 6–7 | 0,4,1,2,2,2 | see `branches2.json` |

P̂_τ/P₀_τ were re-emitted with z = ι³, so the leading degree is in **ι** (12), not X; term counts are
unchanged. All hashes are in `branches2.json`
(sha256 `097cc10e83985ba97474c25686f97a5408b0aac98e8ab126d53ae047073813e6`).

### Θ leaves (one per τ), degrees (ι,a,b,y,r,s,ζ,ζ′) = (24,28,16,4,4,4,2,2)

| τ | terms | sha256 |
|---|---|---|
| 1 | 2,022 | `3a9d490bf05deb54ef68e86b9dbe0284f56251e960bc0bbd709be7a74f055b70` |
| 17 | 2,347 | `0051bbdbf2881067c2126e64de6ccebd7d99db447a22353869d015738b13b009` |
| 33 | 2,347 | `f962a0a8dc7c991d9ae71277c0e7c8da38aa8e33302b58a967c2d9480d1cd3ca` |
| 49 | 2,347 | `3b058c2225c8edd00c8452ce6ec273aa1be6773adee19eae38b5d8e94c9e63e3` |
| 3 | 2,347 | `9d9b557f47b732447595ba26a6fd47e7e2fddf5919b8277155aefacaa58653b0` |
| 11 | 2,347 | `de245e35c38b653cdc641a5e4dd52b7837ad5af337dc357c169236ee0f312b7a` |
| 19 | 2,347 | `bd24fb120a3d1c43f6b26c84ca0e6a664128d530c3a8bd78f2a0d1adfa6a8e3c` |
| 27 | 2,347 | `eb433fd71a788d3b4356b6a9ab17c9c27201f2a780cf7b031bf3bc32962fd9ce` |

### Patch leaves (7 terms each, degrees 2 in X and 2 in each witness)

| p | (π, A, B, 𝔞) | sha256 |
|---|---|---|
| 2 | (6, −1, 2, 4) | `339abc900ba6b6adb3c635c4bfe98460f2ed2c884da0698236c0a23ea6a8f758` |
| 3 | (15, 1, −3, 3) | `a4c8757957e4984e06240f2dde886ddcdffa55461ca1852fe782b4f4adbf3ca3` |
| 5 | (15, −1, 5, 7) | `706ae88d5a262962a17d2dc5250a59e99421dcdc4a6a8aa78d98521e623b8949` |
| 7 | (35, 1, −7, 9) | `7b178eefcb9672c541f9e21115794bb7af874f2da897d2bdf06c3669c611c796` |
| 11 | (33, −1, 11, 1) | `e9e3e213f83e65852e04fef4afc1badc0316855d710f9664a7d9254fc08acc9a` |
| 13 | (65, 1, −13, 4) | `b75241ee6c05e17f17a89e5745da9e8ee6c5349bac2d517a99d66d6bb3154d3a` |
| 17 | (51, −1, 17, 13) | `90529395256324b552fc0aafda35ba6af8bac5a0ba184c7789685dc4eb2a8f9b` |
| 19 | (133, −2, 19, 1) | `72a6edf52297a64c907ddfdd74d91e80bd2921eee99f76fe3f4f79104c806ed2` |
| 23 | (69, −1, 23, 7) | `94827d3aa557d926336e76e00c805138f4fa70083ea9721a42a6f173a3ade19b` |

### Machine records

| file | sha256 |
|---|---|
| `F_recipe.json` — the whole structural spec, every constant filled | `ab723bec3c811c159dfb6a84147b99b0fc0eb491c424b19b279f2d103df82a66` |
| `branches2.json` — every leaf's term count, degrees, hash | `097cc10e83985ba97474c25686f97a5408b0aac98e8ab126d53ae047073813e6` |
| `perprime.json` — nine constant rows + checks | `b523be5f632aa476cc25ae3b7ded0a2c8cc1e8d82d7151a2d2703759f9e93ebe` |
| `e_exc.json` — E_exc derivation | `dc523137e3d4e12bddeb2c44876011f911f9b123497a7727a3c89cfe25810b3a` |
| `TAU.json` — per-cell frozen data (still valid; superseded Λ noted in `E_EXC.md`) | `8abc4350a5fb6bca01fb49bd945fbb178ee47986774661f2ae7a66a6b75392ed` |
| `measurements.json` — every number in `VERIFICATION.md` | `74c04e6757d485ce7d26391d83e264493499753f4198d6e0bfe884aacebf2cb3` |

## 4. Why there is still no single expanded term list

Measured: a Θ-factor has 2,022–2,347 terms; F_Θ is a product of **eight** of them, F_patch a product
of nine 7-term factors, and F squares F_main·F_patch. F_Θ alone is ~10²⁶ terms if expanded naively;
the final square puts the count far beyond anything writable. So the top-level product and squares
stay as products — exactly the shape POLYNOMIAL.md §2 writes. **This is a representation limit, not
an open constant.**

The polynomial *is* evaluable: `F_eval.py` computes F exactly over `Fraction` with all constants
literal, and `python3 F_eval.py` re-checks evaluator ≡ leaves on 12 random witness tuples for each of
34 objects (**0 mismatches**).

## 5. Status of the variable count

11 quantified variables (X; a, b; b₁, σ, υ; y, r, s; ζ, ζ′; ι) — unchanged by all three corrections,
and matching COUNTS.md. The polynomial now defines Q ∖ Z through the duality, with the patch
covering exactly the primes that a denominator can occupy.

## 6. Reproduce

```bash
cd ~/bigo-campaign/dzq-exec
python3 hilbert.py          # Hilbert symbols, (5,2) control arm
python3 e_exc.py            # E_exc, class coverage, residue scan to 3000
python3 perprime.py         # the nine constant rows + F_p term lists
python3 assemble2.py        # all 34 leaves + branches2.json
python3 gen_recipe2.py      # F_recipe.json
python3 F_eval.py           # evaluator == leaves
python3 checks2.py          # hypotheses, symbolic identity, criterion==brute
python3 smoke2.py           # SMOKE2.md's suite
```
