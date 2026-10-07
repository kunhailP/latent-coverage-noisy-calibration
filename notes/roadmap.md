# Roadmap toward Statistica Sinica

Biometrika desk rejection (2026): "niche" and "contribution not competitive". The revision should
read as: what latent guarantee is possible when the noise law and variance are unknown and differ
between units, and what is the smallest correction it needs.

## Status

| Step | State |
|---|---|
| Unified rank interface (`latentcov.rank`, Theorem 2 binomial form) | done, tested against Table 1 |
| R01 exact reliability curves, q = 0.8, 0.9, 0.95 | done (`results/reliability_*`) |
| Gaussian convexity: Psi_N convex => p_N(q) = Psi_N(q) | **proved** for all q > 1/e (`notes/gaussian_exact.md`); cited facts are Sampford (1953) inequalities (3), (4), checked against the text |
| Bi-log-concave non-log-concave (bimodal) latent law in the main comparison | done (R02) |
| Mixed noise laws across units within a class | done (R02 widths, R03 exact stress) |
| Heterogeneous latent laws | **proved** as a corollary of Theorem 2: per-unit q-quantile condition; exact check R06 (`notes/heterogeneous_latent.md`) |
| R04 comparison with existing methods | done (findings below) |
| Rewrite in the Sinica template | todo |

## R01 findings (Gaussian-extremal law, delta = 0.05)

The excess Psi_N(q) - q is 4.4e-3 (q = 0.8), 8.0e-4 (0.9) and 1.6e-4 (0.95). The usual rank's
latent reliability falls below 0.9 at K of about 1.4e3, 2.1e4 and 2.8e5, and below 0.5 at about
2.5e4, 4.3e5 and 5.6e6 (grid values; normal approximation z^2 q(1-q)/(Psi_N - q)^2 agrees).
The certified Gaussian rank stays at or above 0.952 throughout. So q = 0.8 shows the failure at
realistic K and should lead the illustration; q = 0.9 alone understates it.

Update after the Gaussian theorem: with the exact level Psi_N(q), the reliability at this law
tends to 0.9500 from above as K grows (0.9502 at K = 1e6, 0.9500 at 1e7, all three q). So the
rank is valid and cannot be lowered: the extremal law makes the bound of Theorem 2 tight. The
Biometrika rank (level 0.901 etc.) drifts to reliability 1, i.e. it is conservative. This is
the cleanest figure for the paper: valid, sharp, and the usual rank collapsing.

## R02 findings (same information, 2000 data sets per setting, delta = 0.05)

- 6 latent laws (4 log-concave, bimodal bi-log-concave, t3 outside) x 8 noise designs (5 single,
  mixed within symmetric unimodal, mixed within mean-zero log-concave with both signs of the
  centred exponential, mixed across classes) x q in {0.8, 0.9, 0.95} x K in {110, 1000}.
- Every rule, the usual rank included, has reliability >= 0.998 in every setting, covered or
  not (t3 latent, cross-class mixture). These laws measure the cost, not the need (that is R03).
- Cost at K = 1000 over the usual rank / saving over the no-shape rule of the same noise class:
  q = 0.8: Gaussian 0.9-1.2% / 20-26%, symm. unimodal 1.5-2.2% / 19-28%;
  q = 0.9: Gaussian 0.3-0.4% / 16-21%, symm. unimodal 0.6-1.0% / 15-24%, log-concave 1.8-2.9% / 19-33%;
  q = 0.95: no cost (same rank) / 12-20%. At K = 110 the class ranks equal the usual rank.
- K = 110, q = 0.95: the no-shape rules have no valid rank at all; the bi-log-concave rules give
  k = 109. At small K and high q the shape assumption decides whether an interval exists.
- The bimodal law and the mixed designs behave like the log-concave laws and single noise laws.

## R03 findings (exact, extremal exponential-tail latent law, unit noise laws and scales i.i.d.)

- Theorem 2 bound checked: worst-case H never exceeds the class level; the worst uniform-only
  case reproduces Psi_SU(q) to 1e-16 and the centred-exponential case 0.9051755.
- Class rank: reliability >= 0.9502 in all 26 cases (the minimum is attained at the pure
  extremal noise, as it must be).
- Usual rank under mixed noise, q = 0.9, K = 1e5: 0.41 (pure uniform) to 0.92-0.94 (diluted or
  heterogeneous); mean-zero log-concave with the centred exponential: 0.0001 at K = 1e5.
  q = 0.8 mixed symmetric unimodal: 0.39-0.75 at K = 1e4 with equal scales, 0.56-0.76 at
  K = 1e5 with heterogeneous scales.
- Heterogeneous scales dilute the excess H - q a lot (one common c0 cannot put every unit at its
  worst scale): e.g. 0.0018 -> 0.00022 for uniform noise at q = 0.9. So mixing and
  heterogeneity delay the failure of the usual rank but do not remove it; the class rank is
  valid uniformly. State this honestly: the worst case is homogeneous extremal noise.

## Decisions

- Shift-tolerant corollary (pick the rank for latent q + rho, Supplementary Proposition S7):
  dropped. Under symmetric unimodal noise at K = 1000 it gives ranks 918, 927, 945, 962 for
  rho = 0, 0.01, 0.03, 0.05; rho = 0.05 already equals the shape-free rank 962, which undoes the
  paper's main message. The linear bound q' - rho is too coarse. Keep the shift result as a
  limitation, not a procedure.
- Gaussian exactness is framed as completing a row of Table 1, not as the headline.
- The Hoeffding condition k >= K p_k + 1 of the old `certified_rank` never changed a rank for
  29 <= K <= 1e5; the new interface uses the binomial form of Theorem 2 only.

## Reporting rules for R04 and R05 (from the external review, 2026-10-07)

- Every comparison table states, per rule, the information it uses and the guarantee it targets
  (the `information` and `guarantee` columns of R04). A rule is judged against its own target:
  LatentCP and plain conformal by mean coverage >= q (marginal), PAC rules by reliability >= 1 - delta.
  LatentCP's reliability below 0.95 is not a failure of LatentCP.
- R05: at K = 110 every class rank equals the usual rank (k = 105), so the intervals are the
  same; the point is that they need no variance estimates. The LatentCP there is an application
  variant (a new district's variance drawn from the calibration estimates D_c), to be said so.
- R01 wording: "reliability 0.713" is the share of calibration samples whose latent coverage is
  >= q, not a coverage of 71.3%; the usual rank's limiting latent coverage at that law is
  0.79534 (q = 0.8) and 0.89918 (q = 0.9), recomputed from the small-noise limit. Small coverage
  shortfalls, large loss of the PAC guarantee.
- Roles: R02 measures the cost of the guarantee (all rules >= 0.998); R01 and R03 show when the
  correction is needed. "Smallest valid rank" is within order-statistic rules |V|_(k).

## R04 findings (competitors, 300 / 200 data sets at K = 110 / 1000, q = 0.9, delta = 0.05)

6 latent laws (t3 outside the class) x noise Gaussian / Laplace / mixed symmetric unimodal, same
variances. Each rule judged against its own target (reporting rules above). Widths relative to
the usual rank, bi-log-concave latent laws.
- Ours (no noise information): reliability 1.000 in every setting, t3 included; +0% (K = 110),
  +0.3-0.9% (K = 1000) over the usual rank. The usual rank was also at 1.000: benign laws, as in R02.
- LatentCP (known D_i, marginal target): meets its target in every setting (mean coverage >=
  0.970), also under Laplace and mixed noise where its Gaussian forward model is wrong. Wider than
  ours by 4-7% (K = 110) and 14-21% (K = 1000); tuned / two-level variants wider still.
  Do not call it a failure; the point is that ours needs no variances and is not wider.
- Shape-free with known D_i: +19-25%. LatentCP at a PAC rank = median-zero level: +20-42%.
- Fay-Herriot (known D_i, normal model): 16-24% narrower, mean coverage >= 0.914, but PAC
  reliability down to 0.900-0.937 for Laplace latent laws and for normal latent laws with
  non-Gaussian noise (0.915-0.935 at K = 1000). Fine under its own model.
- HetLDC (known D_i, Gaussian noise, log-concave W; K = 110 Gaussian only): about 10% narrower,
  reliability >= 0.983 for every latent law. What known variances buy, under Gaussian noise.
- simple_shrink (known D_min): about 1% narrower at K = 110, same as ours at K = 1000.
- Cohen et al. deconvolution (our reimplementation, as in Biometrika E34): mean coverage 0.28
  (bin 0.01, K = 110) and 0.87-0.92 (bin 0.2) - below the nominal 0.9 in many settings.
  State that this is our reimplementation; the failure may partly reflect tuning (bin width, lam).
Message: without noise information the rule costs at most ~1% over the usual rank, is not wider
than LatentCP with known variances, and only rules that know the variances and assume Gaussian
noise (HetLDC) or a normal model without a PAC guarantee (Fay-Herriot) are narrower.
