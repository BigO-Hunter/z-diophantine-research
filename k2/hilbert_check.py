#!/usr/bin/env python3
"""Spot-check Thm 3(iii): Hilbert symbol (f(q0), g(q0))_p at denominator primes
p | b is independent of the numerator a, given by
  (f_D/p)^{-e D_g} (g_D/p)^{-e D_f} (-1)^{e D_f D_g (p-1)/2}.
Also demonstrates the numerator-prime wall is real (non-vacuous)."""
from sympy import legendre_symbol, factorint, Rational
from sympy import symbols

def hilbert_p(a: Rational, b: Rational, p: int) -> int:
    """Hilbert symbol (a,b)_p for odd prime p (standard formula)."""
    va, vb = 0, 0
    ua, ub = Rational(a), Rational(b)
    # strip p-adic valuations across numerator/denominator
    def vp(x: Rational) -> int:
        n, d = x.p, x.q
        e = 0
        while n % p == 0 and n: e += 1; n //= p
        while d % p == 0 and d: e -= 1; d //= p
        return e
    va, vb = vp(a), vp(b)
    def unit(x: Rational, v: int) -> int:
        # x * p^{-v} reduced mod p (p-adic unit as residue)
        num, den = (x * p**(-v)).p, (x * p**(-v)).q
        return (num * pow(den, -1, p)) % p
    ua_res, ub_res = unit(a, va), unit(b, vb)
    # (a,b)_p = (-1)^{va*vb*(p-1)/2} * (ua/p)^{vb} * (ub/p)^{va}
    t = legendre_symbol(ua_res, p)**vb * legendre_symbol(ub_res, p)**va
    sign = -1 if (va*vb*((p-1)//2)) % 2 else 1
    return sign * t

def poly_val(f, q: Rational) -> Rational:
    return sum(Rational(c) * q**i for i, c in enumerate(f))

# f(q) = q^2 + 1 (D_f=2, f_D=1),  g(q) = q + 3 (D_g=1, g_D=1)
f, g = [1, 0, 1], [3, 1]
Df, Dg, fD, gD = 2, 1, 1, 1

print("=== denominator primes: prediction vs direct computation ===")
ok = True
for (a, b) in [(1, 3), (5, 7), (11, 6), (23, 15), (7, 35)]:
    q0 = Rational(a, b)
    for p in factorint(b):
        if p == 2:  # Hilbert formula here is for odd p; p=2 folds into the finite CRT choice (doc Thm 3(iii))
            continue
        e = factorint(b).get(p, 0)
        pred = (legendre_symbol(fD, p)**(-e*Dg) * legendre_symbol(gD, p)**(-e*Df)
                * (-1)**(e*Df*Dg*(p-1)//2))
        actual = hilbert_p(poly_val(f, q0), poly_val(g, q0), p)
        flag = "OK " if pred == actual else "MISMATCH"
        if pred != actual: ok = False
        print(f"q0={a}/{b} p={p} e={e}: predicted {int(pred):+d}, actual {int(actual):+d}  {flag}")
print("all denominator-prime predictions match" if ok else "!! prediction failed")

print("\n=== numerator-prime wall: odd-valuation primes of F~(a,b)*G~(a,b) ===")
# homogenize: F~(a,b)=a^2+b^2, G~(a,b)=3b+a
from sympy import n_order
def unit_residue(x: Rational, p: int) -> int:
    n, d = x.p, x.q
    while n % p == 0: n //= p
    while d % p == 0: d //= p
    return (n * pow(d, -1, p)) % p
wall_shown = 0
for (a, b) in [(1, 3), (2, 3), (1, 7), (5, 7), (3, 5), (4, 9), (1, 21)]:
    Ft, Gt = a*a + b*b, 3*b + a
    for p in factorint(Ft*Gt):
        if p in (2,) or b % p == 0: continue
        vf = 0; x = Ft
        while x % p == 0: vf += 1; x //= p
        vg = 0; x = Gt
        while x % p == 0: vg += 1; x //= p
        if vf % 2 and vg == 0:
            u = unit_residue(poly_val(g, Rational(a, b)), p)
            leg = legendre_symbol(u, p)
            if leg == -1:
                print(f"a={a} b={b}: numerator prime p={p} | f-valuation {vf} odd, "
                      f"(g-unit/p)=-1  -> FIBER LOCALLY INSOLUBLE at {p} (wall real)")
                wall_shown += 1
                break
print(f"wall demonstrated at {wall_shown} of 7 sample points (odd-valuation obstruction)")
