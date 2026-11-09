# HTMT independent recomputation

Input: the supplied CSV with 271 rows and 20 indicators, grouped as AIR1–4, EXP1–4, PP1–4, TR1–4 and AD1–4.

Run `OPENBLAS_NUM_THREADS=1 python3 /workspace/validation/htmt/verify_htmt.py`.
The script accepts `--csv`, `--reference` and `--output` overrides for use elsewhere.

## Results

- Every one of 10 HTMT+ estimates and 50 reported percentile/BC interval endpoints matches the supplied JSON exactly, including unrounded floating-point values (largest absolute difference: 0.0).
- The 10,000 bootstrap draws use NumPy `default_rng(20261105)`, sampling 271 rows with replacement for each draw.
- Bias correction is BC, not BCa: z0 = Phi^-1[P(theta_boot < theta)], and the upper bound is the empirical quantile at Phi(2*z0 + z_alpha). There is no acceleration term.
- All 10 point estimates are below 0.90. EXP–PP = 0.8595095756 exceeds the stricter point-estimate threshold 0.85.
- For one-sided 95% inference at threshold 0.90, EXP–PP (BC upper = 0.9098775164) and EXP–AD (BC upper = 0.9136988925) do not meet an upper-bound-below-0.90 requirement. The same two pairs fail under percentile upper bounds.
- For one-sided BC 95% inference at threshold 0.85, only AIR–AD and PP–AD have upper bounds below 0.85.
- Two-sided 95% percentile upper bounds above 0.90 additionally include AIR–EXP (0.9004560235) and EXP–TR (0.9000711118). Do not conflate two-sided and one-sided upper bounds.

## Provenance and limits

The supplied CSV's SHA-256 is `ab7e5333f80e50f89dcf90d885556f5b60bb30848052153e77325500af216624`; the JSON declares `5c517d0bcc99f0ce5e909af11da5a4fca1f0c23bb8c4e9060f7cf620def83fcc`. The exact numerical reproduction strongly supports compatibility of the uploaded numerical values with this 271-row CSV, but does not resolve the hash discrepancy. The declared hash may identify an absent source or a different serialization; its identity cannot be established from these inputs.

There are no missing cells and all supplied indicators are integers in 1–5. Seven rows repeat prior complete answer patterns; these are response-vector duplicates and do not establish duplicate respondents. No respondent IDs are supplied. The original 323 respondents and 52 exclusions cannot be verified without the raw source and exclusion rules.

These outputs are Python/NumPy recomputations; they do not establish native SmartPLS provenance or certify all validity criteria.
