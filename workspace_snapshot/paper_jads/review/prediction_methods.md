# Prediction methods and results — English manuscript material

## Copy-ready methods: out-of-sample predictive assessment

Out-of-sample predictive performance was assessed using the native SmartPLS 4 PLSpredict procedure with 10-fold cross-validation repeated 10 times. The analysis used 271 respondents and 20 indicators assigned to AIR, EXP, PP, TR, and AD. The structural model specified AIR, EXP, and PP as antecedents of TR, and TR as the antecedent of AD. The exported settings specified path weighting, initial weights of 1.0, a maximum of 3,000 iterations, and a stopping criterion of 10⁻⁷. A fixed seed was selected; its numerical value was not included in the export and therefore is not reported here. The prediction option was **Direct antecedents**: TR predictions used AIR, EXP, and PP, while AD predictions used the observed indicators of TR. Consequently, predictive results for AD are conditional on observed TR and do not assess AD prediction from AIR, EXP, and PP alone.

Each respondent was held out once per repetition, yielding 2,710 predictions for each endogenous indicator. These predictions represent repeated assessments of the same 271 respondents, rather than 2,710 independent respondents. Prediction error was defined as the observed minus predicted indicator value. Root mean squared error (RMSE) and mean absolute error (MAE) were computed over the pooled held-out predictions in the original item units. Performance was compared with the indicator-average (IA) and linear-model (LM) benchmarks. Q²predict was computed as 1 − SSE_PLS/SSE_IA; positive values indicate lower squared prediction error than the IA benchmark. RMSE served as the primary error comparison and MAE as a complementary measure. The native cross-validated predictive ability test (CVPAT) was used to compare average squared prediction losses at the construct and overall levels. Negative loss differences favour PLS-SEM; statistical decisions below use the p-values reported in the native export and a significance threshold of 0.05.

## Copy-ready results: predictive performance

All eight endogenous indicators had positive Q²predict values, ranging from 0.294689 for AD3 to 0.474015 for TR4, indicating lower squared prediction error than the IA benchmark. PLS-SEM had a lower RMSE than LM for five of eight indicators: TR1, TR2, TR4, AD1, and AD2. LM had a lower RMSE for TR3, AD3, and AD4. Under MAE, PLS-SEM performed better for seven of eight indicators, with AD4 the sole exception. The different counts reflect the different loss functions; they should not be presented as identical findings.

The overall CVPAT loss difference against IA was −0.365179 (t = 6.497330, p = 3.925038 × 10⁻¹⁰), providing evidence of lower predictive loss than the indicator-average benchmark. The corresponding construct-level comparisons were also significant for TR and AD (both p < 0.001). Against LM, the overall loss difference was smaller, −0.009950 (t = 1.549895, p = 0.122338). Thus, the analysis did not establish an overall predictive advantage over the linear benchmark at the 0.05 level. The TR- and AD-level comparisons with LM were likewise not significant (p = 0.159017 and p = 0.456418, respectively). Together, the results support predictive performance relative to the IA baseline, while the advantage over LM remains statistically unestablished. These findings concern prediction under the specified direct-antecedent model and do not establish causal effects.

## Table P1. Native PLSpredict indicator-level RMSE and Q²predict

| Indicator | Q²predict | PLS-SEM RMSE | LM RMSE | IA RMSE | PLS RMSE < LM |
|---|---:|---:|---:|---:|:---:|
| TR1 | 0.429694 | 0.741261 | 0.747146 | 0.981562 | Yes |
| TR2 | 0.393986 | 0.793983 | 0.809530 | 1.019929 | Yes |
| TR3 | 0.395881 | 0.770705 | 0.764487 | 0.991578 | No |
| TR4 | 0.474015 | 0.725451 | 0.749010 | 1.000280 | Yes |
| AD1 | 0.307984 | 0.818698 | 0.828709 | 0.984160 | Yes |
| AD2 | 0.363914 | 0.794019 | 0.800830 | 0.995573 | Yes |
| AD3 | 0.294689 | 0.819193 | 0.818321 | 0.975429 | No |
| AD4 | 0.310104 | 0.809679 | 0.806461 | 0.974812 | No |

Note. Native SmartPLS 4 PLSpredict, 10 folds × 10 repetitions, n = 271; 2,710 held-out predictions per indicator. RMSE is expressed in the original item units. Positive Q²predict indicates improvement over IA, not proof of improvement over LM. Values are rounded to six decimals; comparisons use unrounded values.

## Table P2. Complementary MAE comparison

| Indicator | PLS-SEM MAE | LM MAE | PLS MAE < LM |
|---|---:|---:|:---:|
| TR1 | 0.587936 | 0.588965 | Yes |
| TR2 | 0.630813 | 0.646309 | Yes |
| TR3 | 0.599977 | 0.605974 | Yes |
| TR4 | 0.571607 | 0.579348 | Yes |
| AD1 | 0.642311 | 0.650807 | Yes |
| AD2 | 0.632534 | 0.634905 | Yes |
| AD3 | 0.643313 | 0.643931 | Yes |
| AD4 | 0.641848 | 0.634013 | No |

Note. MAE complements the primary RMSE comparison. The small AD3 MAE advantage does not reverse its RMSE disadvantage.

## Table P3. Native CVPAT at construct and overall levels

| Benchmark | Target | PLS loss | Benchmark loss | Difference (PLS − benchmark) | t | p |
|---|---|---:|---:|---:|---:|---:|
| IA | TR | 0.575036 | 0.996876 | -0.421841 | 6.764604 | 8.270717e-11 |
| IA | AD | 0.656847 | 0.965364 | -0.308517 | 5.450360 | 1.133805e-07 |
| IA | Overall | 0.615942 | 0.981120 | -0.365179 | 6.497330 | 3.925038e-10 |
| LM | TR | 0.575036 | 0.589755 | -0.014719 | 1.412287 | 0.159017 |
| LM | AD | 0.656847 | 0.662029 | -0.005181 | 0.745831 | 0.456418 |
| LM | Overall | 0.615942 | 0.625892 | -0.009950 | 1.549895 | 0.122338 |

Note. Loss is squared prediction error, averaged over indicators within each reported target. Negative differences favour PLS-SEM. These are native SmartPLS CVPAT p-values; they are not p-values calculated by treating all repeated predictions as independent respondents.

## Optional reproducibility paragraph for supplement or appendix

The native export was independently checked against the supplied 271-row input. Every exported manifest-variable error equalled the corresponding observed item value minus the exported prediction, covering 21,680 indicator errors. Recomputed pooled RMSE and MAE agreed with the native summaries to within 2 × 10⁻¹⁵. Native fold membership was recovered from the exported zero-based case-index sequence; each repetition contained one test fold of 28 cases and nine test folds of 27 cases. Refitting the model independently with those partitions reproduced individual native predictions to within 3 × 10⁻⁹ and native PLS RMSE to within 5.5 × 10⁻¹¹. Recomputed benchmark RMSE agreed within 4 × 10⁻¹⁵. CVPAT average losses, differences, and test statistics agreed within 3.8 × 10⁻¹⁴; the native p-values were retained. Minor differences from an earlier exploratory Python cross-validation are attributable to the different partitions used; the native export supplies the manuscript's primary prediction evidence.

## Editorial guardrails (not manuscript prose)

- Do not describe 2,710 predictions as 2,710 participants, independent observations, or an enlarged sample.
- Do not say the model outperforms LM overall, or that all prediction comparisons are significant. Overall LM p = 0.12233805542672371.
- Do not claim an end-to-end AD forecast using only AIR/EXP/PP. The native setting uses observed TR as AD's direct antecedent.
- Do not substitute the earlier exploratory JSON for the native SmartPLS export. The native MAE count is 7/8; the earlier exploratory result was 6/8 because AD3 changed.
- Do not manufacture the numerical fixed seed, external validation, prospective data, or unprovided sampling/eligibility information.
- Indicator-specific LM tests, if discussed, require a multiplicity caveat. Unadjusted p-values identify AD1 (p = 0.000887427) and TR4 (p = 0.008412658); Holm adjustment over eight LM indicator comparisons retains AD1 (p = 0.007099412), whereas TR4 is no longer below 0.05 (p = 0.058888609). Avoid using these two unadjusted findings to override the nonsignificant overall LM comparison.
- The p-values here are copied from SmartPLS. Independent SciPy t-distribution checks have tiny numerical differences (maximum absolute difference approximately 3.5 × 10⁻⁸) that do not change any reported decision; do not claim bit-for-bit p-value reproduction.
- This section establishes numerical reproduction within the supplied data, not causal identification, population representativeness, or universal model validity.
- Add verified methodological citations for PLSpredict, CVPAT, and SmartPLS from the lead's reference review; no bibliographic details have been fabricated here.

## Authoritative source map and full-precision evidence

1. Primary native export: `/workspace/attachments/c7ccdeb6-0e70-4b07-a755-212a824125ff/KidSense_PLSpredict_10x10.xlsx`, sheet `Complete data set`.
   - PLSpredict MV summary: rows 11–19; indicator names and Q²predict, RMSE, MAE in columns B–I.
   - CVPAT construct/overall vs IA: rows 69–72; vs LM: rows 76–79.
   - CVPAT indicator vs IA: rows 85–93; vs LM: rows 97–105.
   - Manifest-variable prediction errors: rows 112–2821; manifest-variable predictions: rows 2826–5535.
   - Settings: rows 10979–10993; prediction type `Direct antecedents`, 10 folds, 10 repetitions, `Fixed seed`.
   - SHA-256: `9e7986e732964003978f57f19362d29c5b9731690e44f51537c8d75bc1f68dd9`.
2. Input: `/workspace/attachments/db7f5ebd-93ee-4498-9458-e1ec5c77d40b/KidSense_SmartPLS4_Input_271.csv`.
3. Full-precision prediction audit: `/workspace/validation/native_prediction/prediction/native_prediction_validation.json` and `/workspace/validation/native_prediction/prediction/native_prediction_comparison.csv`.
4. Full-precision CVPAT audit and native p-values: `/workspace/validation/native_prediction/native_cvpat_verification.json` and `/workspace/validation/native_prediction/native_cvpat_comparison.csv`.
5. Reproducible computations: `/workspace/validation/native_prediction/prediction/reconstruct_folds.py`, `/workspace/validation/native_prediction/prediction/verify_native_prediction.py`, `/workspace/validation/native_prediction/verify_cvpat.py`, and shared fit function `/workspace/validation/verify_pls.py`.
6. Exact exported row evidence: `/workspace/validation/native_prediction/prediction/native_exported_PLS_errors.npz`; independently reconstructed model/benchmark errors: `/workspace/validation/native_prediction/prediction/native_reconstructed_errors.npz`; fold memberships: `/workspace/validation/native_prediction/prediction/native_reconstructed_folds.json`.
7. Integrated reviewed workbook: `/workspace/validation/native_prediction/output/KidSense_Replikasi_SmartPLS4_Final.xlsx`, particularly sheets `Ringkasan_Final`, `PLSpredict_native`, `CVPAT_Konstruk`, and `CVPAT_hitung_ulang`. This is a compilation, not an original SmartPLS export.
