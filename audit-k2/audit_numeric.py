#!/usr/bin/env python3
"""Independent audit of Thm 3(iii) numerics. Own Hilbert-symbol implementation.
Part A: closed form (fD/p)^(-e Dg)(gD/p)^(-e Df)(-1)^(e DfDg (p-1)/2) at p|b
        vs direct Hilbert symbol, random grid, p notin {2, f_D, g_D}.
Part B: small-print stress: same formula when p | f_D (doc's 'good class'
        excludes these; we show the formula actually breaks there).
Part C: HP(P) hit search for (f,g)=(q^2+1,q+3): find (a,b), b>1 odd,
        a=1 mod rad(b), fiber everywhere locally soluble (all odd p, p=2, real).
        A hit => HP true for the sample pair => Thm 3(iii) kill is operative."""
from sympy import factorint
from random import seed, randint

def hilbert_odd(a, b, p):
    """(a,b)_p for odd p, a,b nonzero rationals, standard formula."""
    from math import gcd
    def vals(x):
        n, d = x.numerator, x.denominator
        e = 0
        while n % p == 0: n //= p; e += 1
        while d % p == 0: d //= p; e -= 1
        return e, (n * pow(d, -1, p)) % p
    ea, ua = vals(a); eb, ub = vals(b)
    s = (ea * eb * ((p - 1) // 2)) % 2
    sym = pow(-1, s)
    if eb % 2: sym *= 1 if pow(ua, (p - 1) // 2, p) == 1 else -1
    if ea % 2: sym *= 1 if pow(ub, (p - 1) // 2, p) == 1 else -1
    return sym

def hilbert_2(a, b):
    """(a,b)_2, a,b nonzero rationals: (-1)^(e(u)e(v)+a*w(v)+b*w(u))."""
    def v2(x):
        n, d = x.numerator, x.denominator
        e = 0
        while n % 2 == 0: n //= 2; e += 1
        while d % 2 == 0: d //= 2; e -= 1
        return e, n * pow(d, -1, 8) % 8
    ea, ua = v2(a); eb, ub = v2(b)
    eps = lambda u: ((u - 1) // 2) % 2
    omg = lambda u: ((u * u - 1) // 8) % 2
    return pow(-1, eps(ua) * eps(ub) + ea * omg(ub) + eb * omg(ua))

f, g = [1, 0, 1], [3, 1]           # q^2+1, q+3
Df, Dg, fD, gD = 2, 1, 1, 1
pv = lambda co, q: sum(c * q**i for i, c in enumerate(co))

seed(20261106)
print("A) closed form vs direct Hilbert, random (a,b), p|b, p notin {2}:")
mism = tot = 0
for _ in range(400):
    b = randint(2, 400)
    a = randint(1, 2000)
    from math import gcd
    if gcd(a, b) != 1: continue
    q0 = __import__('fractions').Fraction(a, b)
    for p in factorint(b):
        if p == 2: continue
        e = factorint(b)[p]
        # closed form valid only when p does not divide leading coeffs (small print)
        pred = pow(fD, -1, p)**0 if False else None
        pred = (1 if pow(fD % p, (p-1)//2, p) == 1 else -1)**(-e*Dg) \
             * (1 if pow(gD % p, (p-1)//2, p) == 1 else -1)**(-e*Df) \
             * pow(-1, e*Df*Dg*((p-1)//2))
        act = hilbert_odd(pv(f, q0), pv(g, q0), p)
        tot += 1
        if pred != act:
            mism += 1; print(f"  MISMATCH a={a} b={b} p={p} pred={pred} act={act}")
print(f"   {tot-mism}/{tot} match")

print("B) small-print stress: f=3q^2+1 (f_D=3), g=q+1, p=3 dividing f_D:")
f2 = [1, 0, 3]
mism2 = tot2 = 0
for b3 in [3, 9, 21, 12]:
    for a3 in [1, 2, 4, 5, 7, 8, 10, 11]:
        q0 = __import__('fractions').Fraction(a3, b3)
        e = factorint(b3).get(3, 0)
        if not e: continue
        pred = (1 if pow(3 % 3, 1, 3) == 1 else -1)  # (0/3) = 0 -> degenerate: formula undefined
        # formula wants (f_D/p)^(-e Dg); f_D=3,p=3 => (0/3)=0, NOT +-1: show breakage
        from sympy import legendre_symbol as ls
        pred = ls(3, 3)**(-e*Dg) * ls(1, 3)**(-e*Df) * pow(-1, e*Df*Dg*((3-1)//2))
        act = hilbert_odd(pv(f2, q0), pv(g, q0), 3)
        tot2 += 1
        if pred != act: mism2 += 1
print(f"   formula breaks/mismatches on {mism2}/{tot2} points when p | f_D (small print is load-bearing)")

print("C) HP hit search for (q^2+1, q+3): b odd in 2..120, a=1 mod rad(b), a<2000:")
from math import prod, gcd
hits = insol = checked = 0
hit_ex = None
for b in range(3, 121, 2):
    rad = prod(factorint(b))
    for a in range(1, 2000):
        if a % rad != 1 or gcd(a, b) != 1: continue
        q0 = __import__('fractions').Fraction(a, b)
        F, G = pv(f, q0), pv(g, q0)
        if F == 0 or G == 0: continue            # degenerate fiber (doc excludes)
        checked += 1
        ok = True
        for p in factorint(F.numerator * F.denominator * G.numerator * G.denominator):
            if p == 2: continue
            if hilbert_odd(F, G, p) == -1: ok = False; break
        if ok and hilbert_2(F, G) == -1: ok = False
        if ok and F < 0 and G < 0: ok = False    # real place
        if ok:
            hits += 1
            if hit_ex is None: hit_ex = (a, b)
            break_insol = insol
        else:
            insol += 1
print(f"   checked {checked} candidate (a,b): soluble-fiber hits={hits}, locally insoluble={insol}")
print(f"   first HP hit: q0 = {hit_ex[0]}/{hit_ex[1]}" if hit_ex else "   no hit in range (HP open for this pair, as expected: semi-decidable)")
