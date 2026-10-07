# Manuscript plan (Statistica Sinica)

Constraints (author instructions, checked 2026-10-07): main text at most 40 double-spaced pages in
the SS template; numbered sections, subsections allowed, no sub-subsections; no formulas in the
abstract; key words in alphabetical order; running title under 45 characters; one supplementary
PDF, reviewed with the paper; numerical results reproducible with code and data available.
Templates: SS-template.zip and supp-temp_20240820.tex from the journal site.

## What makes it a strong Sinica paper

One problem, answered completely: what latent coverage a noisy-calibrated threshold guarantees,
and the smallest correction that keeps it when the noise is unknown and heterogeneous.
1. A sharp answer: necessary and sufficient levels, exact for Gaussian and symmetric unimodal
   noise, and a valid rank that cannot be lowered (reliability tends to exactly 1 - delta at the
   extremal law).
2. A boundary: unimodality gives nothing over no shape assumption; bi-log-concavity recovers
   almost everything.
3. A usable procedure: one rank from a table or one function call, no noise variances needed.
4. Honest evidence in three roles: when the correction is needed (R01, R03), what it costs
   (R02, R04), how it behaves on data (R05).
The paper must not oversell: existing methods do not collapse in benign settings (R04). The
claim is less information, the same guarantee, essentially the same width.

## Title, running title, key words

- Title: Latent coverage from noisy calibration (kept; matches the repository and the
  Biometrika version; the editor will see a revised, extended paper).
- Running title (< 45 characters): LATENT COVERAGE FROM NOISY CALIBRATION (38).
- Key words: Bi-log-concavity; Conformal prediction; Measurement error; Small area estimation;
  Tolerance interval.

## Structure and page budget (double spaced)

| § | content | source | pages |
|---|---|---|---|
| 1 | Introduction: problem, two known answers, contributions, Table 1 (methods by information used and guarantee targeted) | main §1 rewritten | 4 |
| 2 | Setting: latent reliability, classes B and E, Psi_E, p_E | main §2-3 | 2 |
| 3 | Coverage transfer: Prop 1 with proof; both ends; Theorem 1 (symmetric unimodal exact, log-concave certified, mean-zero unimodal none); **Theorem 2 Gaussian exact** with proof sketch (first-order condition s = m(b), envelope derivative, Sampford); threshold 1/e; Prop 2 unimodality insufficient; Table 2 (map) | main §2, notes/gaussian_exact.md | 7 |
| 4 | Calibration with unknown heterogeneous noise: Theorem 3 (valid rank, converse, sharpness); Prop 3 failure of the usual rank, quantified at q = 0.8; Corollary 1 heterogeneous latent laws + remark that a link is necessary; normalized scores; one-sided intervals; Algorithm 1 | main §3, notes/heterogeneous_latent.md | 6 |
| 5 | What a known noise variance buys (short): sharp radius, order D vs D^{1/2} by the location of the mean, slack; link to HetLDC (about 10% narrower in R04) | main §4, supplement S3 | 3 |
| 6 | Numerical studies: 6.1 when the correction is needed (Fig 1 reliability curves, R03 mixed noise); 6.2 cost with the same information (R02); 6.3 existing methods (R04 table with information and target columns) | R01-R04, R06 | 7 |
| 7 | Application: school districts (R05), honest framing (same k = 105, no variance estimates; LatentCP application variant) | R05 | 2 |
| 8 | Discussion: link condition between units, checking bi-log-concavity, log-concave noise open, shifts | main §5 | 2 |
| | References, Supplementary Material paragraph | | 3 |
| | **Total** | | **36** |

## Supplement (single PDF)

S1 Preliminaries; S2 proofs for §3 (both ends, one end not enough, Theorem 1 (i)-(iii), full
Gaussian proof, Prop 2); S3 proofs for §4 (Theorem 3, Prop 3, Corollary 1, Lemmas A and B on
Bernoulli sums); S4 known variance (reduction, one-sided constant, mean location, transition,
centred laws, slack); S5 certificates in ball arithmetic; S6 heterogeneous/estimated variances,
Markov rule, shifted residual; S7 further simulations (R02, R03, R04 full tables, R06); S8
application details; S9 reproducibility (Makefile targets).

## Numbering map (new, used throughout)

- Proposition 1 one-end transfer; Theorem 1 classes; Theorem 2 Gaussian exact; Proposition 2
  unimodality insufficient; Theorem 3 valid rank (was Theorem 2); Proposition 3 failure of the
  usual rank; Corollary 1 heterogeneous latent laws; Theorem 4 small-noise widening (was
  Theorem 3); Corollary 2 slack.

## Before drafting: literature check

Search 2025-2026 work on conformal prediction with noisy or proxy labels, latent targets,
measurement error, small-area prediction intervals, to update §1 and Table 1.

## Disclosure

The author handles the AI-use declaration (Biometrika version: grammar only; must be updated to
the actual use before submission). Not drafted here.

## Status (2026-10-07, evening)

- Main text drafted in `paper/main.tex` (SS template, compiles, 32 pages double spaced).
  Every number checked against `results/`.
- To do in the supplement (labels already cited from the main text): S-sec:s-gauss-exact (full
  Gaussian proof), S-lem:bernoulli (Lemmas A, B), S-sec:s-hetero-sim (R06), S-sec:s-mixed (R03),
  S-sec:s-app (R05 details), plus the sections carried over from the Biometrika supplement.
- Check in the supplement: §5 claims R_{p,0.9}(x) > 1 for all small x whenever p < Psi_N(0.9)
  (was stated for p <= 0.90079); needs c_{p,q} > 0 for p < Psi(q) and the lower-bound argument.
