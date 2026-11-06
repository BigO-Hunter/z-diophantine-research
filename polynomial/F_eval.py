"""The assembled polynomial as a self-contained straight-line evaluator (exact, Fractions).

    F = (F_main * F_patch)^2 + (X*iota - 1)^2
    F_main  = F_Phi^2 + F_Theta^2
    F_Theta = prod_{tau in Lambda} [ (delta_tau zeta - 1)^2 + Phat_tau^2 + ((D zeta' - 1) P0_tau)^2 ]
    F_patch = prod_{p in E_exc} F_p ,   F_p = pi_p X^2 G_p(y, r, s) - p^2

Constants: S = {2}, u = 1, pi = 2,
  Lambda = (1, 17, 33, 49, 3, 11, 19, 27)     [(4 lifts per local class; see E_EXC.md)]
  E_exc  = (3, 5, 7, 11, 13, 17, 19, 23)      [8 primes, all of them forced]

The argument of each O_(p) formula is X/p (m_p = p*O_p), hence the constant term p^2.

Usage:  python3 F_eval.py            # self-checks against the emitted term lists
"""
from fractions import Fraction as Q

PI = 2
U = 1
LAMBDA = (1, 17, 33, 49, 3, 11, 19, 27)
# (p, pi_p, A_p, B_p, a_p)   -- per-prime Prop 4.2 constants, all hypotheses machine-checked.
# The union defined is U_{w in V_K \ S0} m_w with the prescribed S0 = empty (Q \ Z = {X : 1/X in
# U_{all w} m_w}), while the freezing construction uses S = {2}; Sun's "return from S to S0" step
# adjoins U_{v in S \ S0} m_v = m_2.  So the patch set is E_exc u {2}: 9 primes.
PATCH = (
    (2, 6, -1, 2, 4),
    (3, 15, 1, -3, 3),
    (5, 15, -1, 5, 7),
    (7, 35, 1, -7, 9),
    (11, 33, -1, 11, 1),
    (13, 65, 1, -13, 4),
    (17, 51, -1, 17, 13),
    (19, 133, -2, 19, 1),
    (23, 69, -1, 23, 7),
)
E_EXC = (3, 5, 7, 11, 13, 17, 19, 23)          # Sun's exceptional set (subset of V_K \ S)
PATCH_PRIMES = (2,) + E_EXC                    # S \ S0 = {2} is adjoined by the return step (9.4)


def _A(a):
    return 1 + 4 * a * a


def _G(a, b):
    return 16 * a ** 4 * b ** 2 - (b - 1) ** 4 * (1 + 4 * a * a)


def _N(a, b, X, iota):
    z = iota ** 3      # h-bridge variable is iota = 1/X, not X
    return a * a * z * z * _G(a, b)


def _D(a, b, X, iota):
    z = iota ** 3
    return _A(a) * b * b * (1 - z - a * a * z * z)


def _delta(a, tau):
    return 1 - _A(a) * (tau * tau)


def _Phat(a, b, X, tau, y, r, s, iota):
    A = _A(a)
    N = _N(a, b, X, iota)
    D = _D(a, b, X, iota)
    d = _delta(a, tau)
    B = b * PI
    return d * (N * N - A * y * y * D * D) - 16 * B * (r * r - A * s * s) * D * D - 16 * D * D


def _P0(a, b, X, tau, y, r, s):
    A = _A(a)
    d = _delta(a, tau)
    B = b * PI
    return -d * A * y * y - 16 * B * (r * r - A * s * s) - 16


def _F_Phi(a, b, b1, sigma, upsilon):
    return (b * b1 - 1 - sigma * PI) ** 2 + (a - U - upsilon * PI) ** 2


def _F_Theta(a, b, X, y, r, s, zeta, zetap, iota):
    acc = Q(1)
    D = _D(a, b, X, iota)
    for tau in LAMBDA:
        d = _delta(a, tau)
        p1 = d * zeta - 1
        p3 = D * zetap - 1
        acc *= (p1 * p1 + _Phat(a, b, X, tau, y, r, s, iota) ** 2
                + (p3 * _P0(a, b, X, tau, y, r, s)) ** 2)
    return acc


def F_p(p, pi_p, A_p, B_p, a_p, X, y, r, s):
    """pi_p * [(1+4A)(y - y^2) + (a - A) - B(r^2 + r s - A s^2)] - p^2 X^2.

    Encodes "X not in Z_(p)" (i.e. 1/X in m_p): the O_(p) formula applied to x = 1/(pX).
    """
    D = 1 + 4 * A_p
    bracket = D * (y - y * y) + (a_p - A_p) - B_p * (r * r + r * s - A_p * s * s)
    return pi_p * bracket - p * p * X * X


def _F_patch(X, y, r, s):
    acc = Q(1)
    for consts in PATCH:
        acc *= F_p(*consts, X, y, r, s)
    return acc


def evaluate(X, w):
    """w = dict(a,b,y,r,s,zeta,zetap,b1,sigma,upsilon,iota)."""
    X = Q(X)
    a, b, y, r, s = (Q(w[k]) for k in ("a", "b", "y", "r", "s"))
    zeta, zetap = Q(w["zeta"]), Q(w["zetap"])
    b1, sigma, upsilon, iota = (Q(w[k]) for k in ("b1", "sigma", "upsilon", "iota"))
    f_main = (_F_Phi(a, b, b1, sigma, upsilon) ** 2
              + _F_Theta(a, b, X, y, r, s, zeta, zetap, iota) ** 2)
    f_patch = _F_patch(X, y, r, s)
    return (f_main * f_patch) ** 2 + (X * iota - 1) ** 2


def p_eval(p, w):
    names = ["X", "a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota"]
    vals = [Q(w[n]) for n in names]
    tot = Q(0)
    for k, c in p.d.items():
        term = Q(c)
        for i, e in enumerate(k):
            if e:
                term *= vals[i] ** e
        tot += term
    return tot


def selftest():
    import random

    from assemble import P0, Phat, phi_poly, theta_factor
    from assemble2 import patch_poly
    rng = random.Random(3)
    checks = {"phi": (phi_poly(), lambda w: _F_Phi(Q(w["a"]), Q(w["b"]), Q(w["b1"]),
                                                  Q(w["sigma"]), Q(w["upsilon"])))}
    for tau in LAMBDA:
        checks["Phat%d" % tau] = (Phat(tau), (lambda t: lambda w: _Phat(
            Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"]),
            Q(w["iota"])))(tau))
        checks["P0_%d" % tau] = (P0(tau), (lambda t: lambda w: _P0(
            Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"])))(tau))
        checks["thetafac%d" % tau] = (theta_factor(tau), (lambda t: lambda w: (
            (_delta(Q(w["a"]), t) * Q(w["zeta"]) - 1) ** 2
            + _Phat(Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"]),
                    Q(w["iota"])) ** 2
            + ((_D(Q(w["a"]), Q(w["b"]), Q(w["X"]), Q(w["iota"])) * Q(w["zetap"]) - 1)
               * _P0(Q(w["a"]), Q(w["b"]), Q(w["X"]), t, Q(w["y"]), Q(w["r"]), Q(w["s"]))) ** 2))(tau))
    for consts in PATCH:
        p, pi_p, A_p, B_p, a_p = consts
        checks["patch_p%d" % p] = (patch_poly(A_p, B_p, a_p, pi_p, p),
                                   (lambda c: lambda w: F_p(*c, Q(w["X"]), Q(w["y"]),
                                                            Q(w["r"]), Q(w["s"])))(consts))
    bad = 0
    for name, (poly, fn) in sorted(checks.items()):
        for _ in range(12):
            w = {k: Q(rng.randrange(-6, 7), rng.choice([1, 1, 2, 3])) for k in
                 ("X", "a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota")}
            if p_eval(poly, w) != fn(w):
                bad += 1
                print("MISMATCH", name, w)
    print("leaf equivalence: %d objects x 12 random tuples, mismatches: %d" % (len(checks), bad))
    w = {k: Q(0) for k in ("a", "b", "y", "r", "s", "zeta", "zetap", "b1", "sigma", "upsilon", "iota")}
    w["X"], w["iota"] = Q(3, 2), Q(2, 3)
    print("sample evaluation (degenerate witness, X=3/2): F =", evaluate(Q(3, 2), w))
    return bad == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
