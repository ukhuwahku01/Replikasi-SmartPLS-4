# M1 exploratory supplement — Python only

M0, the prespecified AIR/EXP/PP→TR→AD model, remains the primary model. M1 adds
all three AIR/EXP/PP→AD paths simultaneously for a theory-motivated diagnostic;
no path was selected because its p value was favorable. All 271 observations and
all 20 indicators are retained. The user-supplied construct descriptions are
operational definitions; no theoretical citations or objective AI/security
measurements are supplied. AD describes hypothetical conditional adoption
intention, not observed adoption or behavioral continuation.

`fit_exploratory_M1.py` implements generic reflective Mode A PLS-PM with path
weighting. A meaningful control first reproduces M0 using the previous independent
implementation: maximum beta difference 2.22e-16, loading difference 3.33e-16,
R² difference 2.22e-16, below tolerance 1e-8. M1 uses the same convergence criterion
(maximum normalized weight difference <1e-12) and canonical positive block
orientation.

Bootstrap: 10,000 case resamples, four independent NumPy default_rng streams with
seeds 20261106–20261109, 2,500 draws each. Standard errors use ddof=1; two-sided
95% intervals use percentile 2.5% and 97.5%. All 15 stored outputs have 10,000
finite replicates. This is not a native SmartPLS M1 run. The sample generation is
not asserted identical to SmartPLS fixed-seed sampling.

Files:

- `M1_exploratory_results.json`: method, M0 control, all 7 paths, 3 indirect and
  3 total associations, 2 R² values, percentile intervals, loadings, VIF and caveats.
- `M1_exploratory_results.csv`: compact results table.
- `M1_bootstrap_10000.npy`: 10,000 rows in exact CSV-result column order: 7 paths,
  3 indirect, 3 total, then R² TR and R² AD.
- `M1_composite_correlations.csv`: estimated composite-score correlations.

The M1 structural covariance model is saturated. In unstandardized covariance
parameterization the three exogenous variables have 6 free covariance/variance
parameters; 7 path coefficients and 2 endogenous residual variances give 15 free
parameters for 15 covariance moments of five scores. On the standardized scale,
3 free exogenous correlations and 7 paths cover all 10 off-diagonal correlations.
The model-implied score covariance matches observed score covariance to 1.11e-16.
This saturation applies to the structural score covariance part; measurement
restrictions at item level can remain. Therefore better in-sample fit/R² does
not confirm the added paths or mediation theory. PLS weights also change between
M0 and M1, so R² increments are not pure fixed-score nested-regression increments.

Results support only model-conditional, same-sample exploratory associations.
They do not establish causality, remove construct-overlap/HTMT concerns, or
replace the prespecified analysis. Native M1, independent predictive validation,
and M1 CVPAT remain unrun.
