"""R06: exact check of the heterogeneous-latent corollary (notes/heterogeneous_latent.md).

Calibration unit i has its own latent law G_i and Gaussian noise sigma_i Z; the new unit has law
G_0 with r0 = Q_q(|W_new|) = 1. Unit parameters are drawn i.i.d. from a design, so the indicators
1{|V_i| < r0} are i.i.d. with H = E pi(theta), pi(theta) = pr(|V_i| < r0 | theta), and the latent
reliability of rank k is pr{Bin(K, H) <= k - 1} exactly (as in R03). The corollary says
pi(theta) <= Psi_N(q) whenever G_i is bi-log-concave and Q_q(|W_i|) >= r0.

Latent laws are exponential tails W = b - E/u (rate u), the extremal laws of Proposition 1, with
b chosen so that Q_q(|W|) = r_i; sigma is adversarial per unit (pi maximal).
Designs:
  homogeneous extremal       r_i = 1, one u, adversarial sigma (Theorem 2 tight)
  heterogeneous, condition   u_i lognormal, r_i = 1 + tau_i/u_i, tau_i = |N(0, 0.02^2)|
  10% easier units           as above but 10% of units have tau_i = -0.02 (condition fails)
  random unit (mixture)      point masses at 0 and 1 + eta, the new unit a random calibration unit

  python experiments/r06_heterogeneous_latent.py
Writes results/heterogeneous_latent.csv.
"""
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize_scalar
from scipy.special import log_ndtr, ndtr

from latentcov.levels import level
from latentcov.rank import rank_for_level

RESULTS = Path(__file__).resolve().parents[1] / 'results'
DELTA = 0.05
KS = [110, 1000, 10_000, 100_000, 1_000_000]


def cdf_v(x, b, u, sigma):
    """pr(b - E/u + sigma Z <= x)."""
    d = (x - b) / sigma
    return float(ndtr(d) + math.exp(u * (x - b) + (u * sigma) ** 2 / 2 + log_ndtr(-d - u * sigma)))


def b_for(r, u, q):
    """b with Q_q(|b - E/u|) = r: e^{-u(b - r)} (1 - e^{-2ur}) = q, needs 1 - e^{-2ur} > q."""
    return r + math.log(-math.expm1(-2 * u * r) / q) / u


def pi(r, u, sigma, q, r0=1.0):
    b = b_for(r, u, q)
    return cdf_v(r0, b, u, sigma) - cdf_v(-r0, b, u, sigma)


def pi_adv(r, u, q):
    """max over sigma of pr(|V| < 1) for the exponential tail with Q_q(|W|) = r."""
    res = minimize_scalar(lambda ls: -pi(r, u, math.exp(ls), q), bounds=(-12, 3),
                          method='bounded', options={'xatol': 1e-12})
    return -res.fun


def designs(q, rng, n=4000):
    u_h = 200.0                                   # scale of the homogeneous extremal law
    yield 'homogeneous extremal', 'adversarial sigma', pi_adv(1.0, u_h, q)
    # offsets of r_i beyond r0 in units of the tail scale 1/u_i: tau = 0.03 already lowers pi
    # by 0.03 at q = 0.9, so offsets of a few percent of 1/u keep every unit near the worst case
    u = 200 * rng.lognormal(0, .7, n)
    tau = np.abs(rng.normal(0, .02, n))
    yield ('heterogeneous, condition holds', 'adversarial sigma',
           np.mean([pi_adv(1 + t / ui, ui, q) for t, ui in zip(tau, u)]))
    tau_bad = np.where(rng.random(n) < .1, -.02, tau)
    yield ('10% easier units (tau = -0.02)', 'adversarial sigma',
           np.mean([pi_adv(1 + t / ui, ui, q) for t, ui in zip(tau_bad, u)]))
    # random unit: a share w of point masses at 1 + eta, the rest at 0, w just above 1 - q, so
    # Q_q of the mixture is 1 + eta; small Gaussian noise; pr(|V| < 1 + eta) at the two atoms
    w, eta, s = (1 - q) * 1.001, 1e-3, 1e-4
    p_out = ndtr(0.0) - ndtr(-2 * (1 + eta) / s)
    p_in = ndtr((1 + eta) / s) - ndtr(-(1 + eta) / s)
    yield 'random unit (mixture of point masses)', 'sigma = 1e-4', w * p_out + (1 - w) * p_in


def main():
    rng = np.random.default_rng(20261007)
    rows = []
    for q in (0.8, 0.9):
        psi = level('gaussian', q).sufficient
        ranks = {'usual': lambda K: rank_for_level(K, q, DELTA),
                 'Gaussian class (Theorem 2)': lambda K: rank_for_level(K, psi, DELTA),
                 'no latent shape': lambda K: rank_for_level(K, 1 - (1 - q) / 2, DELTA)}
        for design, noise, H in designs(q, rng):
            for K in KS:
                for name, f in ranks.items():
                    k = f(K)
                    rel = float('nan') if k is None else float(stats.binom.cdf(k - 1, K, H))
                    rows.append(dict(q=q, design=design, noise=noise, H=H, psi=psi,
                                     H_minus_psi=H - psi, K=K, rule=name, k=k, reliability=rel))
    d = pd.DataFrame(rows)
    d.to_csv(RESULTS / 'heterogeneous_latent.csv', index=False)
    pd.set_option('display.width', 250)
    hs = d.drop_duplicates(['q', 'design', 'noise'])[['q', 'design', 'noise', 'H', 'H_minus_psi']]
    print(hs.to_string(index=False))
    wide = d.pivot_table(index=['q', 'design', 'noise', 'rule'], columns='K', values='reliability')
    print(wide.round(4).to_string())


if __name__ == '__main__':
    main()
