# Introduction

KidSense is a proposed system intended to help parents interpret early information about a child's emotional condition during digital play. Its design describes emotion-related notifications, explanatory information, and controls concerning camera and microphone access and data storage and deletion. Before such a system is implemented and evaluated in use, an acceptance study can examine how parents interpret the proposed design and whether they would consider using it. Such evidence addresses expectations about a concept; it cannot establish the accuracy of emotion recognition, the safety of a deployed system, or actual adoption.

Trust is relevant when people must judge an automated system whose underlying operations they cannot fully inspect. Research on automation distinguishes appropriate reliance from unconditional confidence {{lee2004}}, while AI trust research shows that trust depends on technological features, users, and context {{glikson2020}}. Explanations can shape how users interpret an AI output and its limitations {{shin2021}}. Privacy-related expectations also matter when a proposed service involves information about children, although perceived protection must be distinguished from demonstrated security or privacy compliance {{malhotra2004}}. These perspectives motivate examining perceived AI reliability, Explainability, Perceived Privacy Protection, Trust, and Adoption Intention together.

Adoption intention is a prospective assessment rather than observed use. Technology-acceptance research treats intention and use as related but distinct outcomes {{venkatesh2003}}. This distinction is especially consequential here: respondents viewed descriptions and images of the KidSense design, and the intention items asked them to imagine that the system was available, satisfied security requirements, and functioned as described. The results therefore concern conditional intentions formed during concept evaluation, rather than experience-based acceptance of a functioning prototype.

Statistical interpretation also requires more than significant path coefficients. PLS-SEM reporting guidance separates measurement assessment, structural relationships, and predictive performance {{hair2019}}. Strong internal consistency does not by itself establish discriminant validity {{henseler2015}}, and explanatory performance does not establish predictive superiority {{shmueli2016}}. A study of concept-based perceptions should therefore report contrary as well as favorable diagnostics and make its computational results traceable to the underlying data.

This study addresses three questions. RQ1 asks how perceived AI reliability, Explainability, and Perceived Privacy Protection are associated with Trust, and how Trust is associated with conditional Adoption Intention in the original model, M0. RQ2 asks whether the proposed constructs are sufficiently distinct and whether M0 predicts held-out responses better than simple benchmarks. RQ3 asks what changes when direct paths from the three design perceptions to Adoption Intention are added in a post hoc exploratory model, M1. The contribution is an integrated concept-evaluation analysis with native SmartPLS results and independent computational checks, including explicit treatment of measurement and prediction limitations.

# Literature Review

## Perceived reliability and Trust in a proposed AI system

Trust in automation involves expectations about an automated system under conditions of uncertainty {{lee2004}}. A review integrating empirical evidence identifies dispositional, situational, and learned influences on trust {{hoff2015}}. Research on trust in a specific technology further distinguishes beliefs about technological attributes from broader trusting responses {{mcknight2011}}. These distinctions support examining Perceived AI Reliability and Trust separately rather than treating reliable functioning and trust as interchangeable labels.

For KidSense, Perceived AI Reliability (AIR) concerns parents' expectations that emotion-related detections and notifications would be consistent, appropriate to the child's condition, and stable during digital play. Trust (TR) concerns confidence that the proposed system would serve the child's interests and provide initial emotion-related information responsibly. A positive AIR–TR association is plausible because perceived dependability can inform trust judgments. However, the present AIR measure captures anticipated functioning after concept exposure; no software reliability experiment or emotion-recognition benchmark was conducted as part of this analysis.

## Explainability and Perceived Privacy Protection

Explainability can be relevant to acceptance because users need to interpret the reasons and information supporting an AI output {{shin2021}}. The present Explainability construct (EXP), called Keterjelasan Penjelasan Sistem in the questionnaire, concerns self-reported understanding of described explanations. Its four items address emotion-category reasons, the information underlying warnings, prediction confidence and possible errors, and the interpretation of warnings. This operational scope concerns perceived understanding of information presented in the design. It does not establish explanation fidelity, technical interpretability, or objectively demonstrated comprehension.

Privacy research links privacy-related concerns and judgments to information-disclosure and transaction decisions {{malhotra2004}} {{dinev2006}}. KidSense's Perceived Privacy Protection (PP) concerns parents' assessments of the proposed protection mechanisms, including permission to access cameras and microphones, data storage and deletion, and overall adequacy. This positive appraisal of proposed protection is conceptually different from privacy concern. The literature provides a rationale for examining PP; it is not evidence that the KidSense questionnaire was adapted from a particular published privacy scale.

Both understandable information and perceived safeguards could be associated with trust, but they address different domains. Explainability concerns interpreting system information; privacy protection concerns handling child-related data. Their empirical separation must therefore be assessed rather than assumed. If their indicators remain highly associated, theoretical distinctions alone do not remove the resulting uncertainty in structural interpretation.

## Trust, conditional intention, and the model specifications

Technology-acceptance studies examine prospective beliefs and intentions, while work integrating trust and acceptance provides a reason to consider trust in technology-use decisions {{venkatesh2003}} {{gefen2003}}. In this study, Adoption Intention (AD) spans willingness to try KidSense, plans to use it for supporting digital-play supervision, intention to use early-warning features, and interest in continued use if experience meets expectations. These items retain a conditional and prospective meaning. They provide no observations of installation, sustained use, willingness to pay, or improved child outcomes.

M0 specifies AIR → TR, EXP → TR, PP → TR, and TR → AD. Its three exogenous perceptions are permitted to covary. The specification examines a trust-based indirect route but does not estimate direct associations from AIR, EXP, or PP to AD. Consequently, finding significant indirect effects in M0 cannot by itself establish full mediation: the absence of a direct path is a model restriction, not an empirical finding that its effect is zero.

M1 retains the five constructs, all 20 indicators, and all four M0 paths, and adds AIR → AD, EXP → AD, and PP → AD simultaneously. It is an explicitly post hoc model-development analysis on the same respondents. Figure 1 distinguishes the original paths from the exploratory additions. Neither the availability of a more flexible model nor its higher in-sample R² provides independent confirmation of a causal mechanism.

[[FIG:model]]

# Methodology

## Study context, design, and available sample

The analysis uses a cross-sectional questionnaire dataset containing 271 response records and 20 numeric indicators. The researcher confirmed that respondents evaluated descriptions and images of the proposed KidSense design, rather than a demonstration or functional prototype. Thus, this is a study of parental perceptions formed during concept evaluation. The supplied files contain questionnaire responses and analysis outputs; they do not contain measurements of children's emotions, operational AI predictions, or observed application use.

[TO BE COMPLETED: recruitment location and dates; sampling and recruitment method; parental eligibility criteria; recruitment channels; and any incentives.] The available analysis dataset supports n = 271, but it does not independently establish the original recruitment denominator or the reasons for exclusions. Demographic variables and the raw screening and consent records were not supplied. Accordingly, this draft does not assert a representative population, a response rate, or an independently verified participant-exclusion flow.

## Constructs and measurement

Each of the five constructs was modeled reflectively using four indicators, as shown in Table 1. The supplied values are integers from 1 to 5. [TO BE COMPLETED: the original response-anchor wording, questionnaire administration procedure, instrument development or adaptation sources, translation procedure, and pretest/pilot details, where applicable.] Operational definitions were supplied by the researcher based on the coverage of the questionnaire items; they are not quotations from external theoretical publications.

[[TABLE:constructs]]

The exact Indonesian wording supplied for EXP1–EXP4, PP1–PP4, and AD1–AD4 is reproduced in Appendix A. [TO BE COMPLETED: the original wording of AIR1–AIR4 and TR1–TR4.] Before answering the AD items, respondents were asked to imagine that KidSense was available, met security requirements, and had the functions described in its design. AD4 additionally conditions prospective continued use on an experience that meets expectations. These conditions define the interpretation of the outcome throughout this paper.

Reflective measurement was retained to reproduce the specified model. Its conceptual suitability warrants further instrument-development work: privacy items cover several mechanisms, while intention items span trial, use, feature use, and conditional continuation. These differences are substantive questions about indicator coverage, not reasons to delete items merely to improve a statistical threshold. No indicator was removed or reassigned in M0 or M1.

## Data integrity and computational replication

The input CSV was checked for dimensions, numeric ranges, missingness, and response-pattern repetition. All 5,420 item values in the native exports were compared with the CSV, including respondent order and indicator assignment. A byte-order-mark prefix in the exported AIR1 header was normalized only for matching variable names. This did not alter any response value. Source files and derived calculations were retained separately, with SHA-256 checksums for traceability.

Native SmartPLS exports supply the primary inferential results. Independent Python computations checked the reflective path-weighted PLS solution, reliability summaries where implemented, HTMT point estimates, path-product arithmetic, prediction errors, and cross-validation outputs. Numerical agreement establishes computational consistency for the supplied data and specifications; it does not establish population representativeness, construct validity, or freedom from response bias. Native rho_A values are reported as software outputs and were not independently recalculated.

Ten records had the same answer across all 20 indicators. They were retained in the primary analysis because uniform responding alone does not prove invalid participation. A previously computed analysis excluding these records was treated as a sensitivity exercise only. Repeated complete response patterns likewise were not interpreted as evidence of duplicate people, because respondent identifiers and original collection records were unavailable. The analysis did not reconstruct unprovided consent flags or collection timestamps from questionnaire responses.

## PLS estimation, bootstrap inference, and measurement assessment

Analyses were performed in SmartPLS 4.1.2.1 using path weighting, standardized results, initial weights of 1.0, a maximum of 3,000 iterations, and a stopping criterion of 10⁻⁷. The native export records automatic outer weighting for the reflective blocks; an independent reflective Mode A implementation reproduced their numerical solution. The settings and outputs were checked against the original M0 and corrected five-construct M1 export, rather than inferred from filenames alone.

Structural inference used 10,000 bootstrap resamples, complete results, two-tailed tests at α = 0.05, and 95% percentile confidence intervals. Native p-values were retained and very small values are reported as p < 0.001. A fixed seed was selected in SmartPLS, but its numeric value and the individual bootstrap draws were not included in the exports. The independent resampling check therefore supports robustness of reported decisions, rather than identity of the native bootstrap draws. M1 inference is exploratory and its nominal p-values were not corrected for searching across alternative models.

Internal consistency was summarized by standardized Cronbach's alpha, rho_A, and composite reliability (rho_C); convergent evidence was summarized by loadings and average variance extracted (AVE) {{hair2019}} {{fornell1981}}. Discriminant validity was assessed separately using HTMT {{henseler2015}}. A dedicated native bootstrap run used the bias-corrected and accelerated (BCa) method, 10,000 resamples, and a one-tailed 0.05 setting. The one-sided 95% upper bound was compared with the adopted 0.90 threshold. This bound is distinct from the two-sided path confidence intervals and from the earlier Python bias-corrected calculation without acceleration.

Structural reporting includes standardized path coefficients, bootstrap uncertainty, indirect effects as products of constituent paths, and R². Global discrepancies were examined using SRMR, d_ULS, and d_G alongside their native bootstrap reference bounds. Descriptive cutoffs were not used to override unfavorable bootstrap comparisons. M0 and M1 retained identical respondents and indicator blocks; their weight-dependent PLS scores were nevertheless re-estimated for each specification.

## Held-out prediction and benchmark comparison

M0 predictive performance was evaluated using native PLSpredict with 10 folds and 10 repetitions {{shmueli2016}} {{shmueli2019}}. The recorded prediction option was Direct antecedents. Thus, TR predictions used AIR, EXP, and PP, while AD predictions used the observed TR indicators. AD prediction is consequently conditional on observed Trust and is not an end-to-end forecast from AIR, EXP, and PP alone. A fixed-seed option was selected; the numeric seed was not exported.

Each respondent was held out once per repetition, yielding 2,710 predictions per endogenous indicator from 271 people. These repeated predictions do not enlarge the independent respondent sample. Root mean squared error (RMSE) was the primary error comparison; mean absolute error (MAE) provided a complementary measure. Both were computed in the original item units. Q²predict = 1 − SSE_PLS/SSE_IA compared PLS with an indicator-average (IA) benchmark. A linear-model (LM) benchmark provided a stronger comparison using the corresponding predictor information.

The cross-validated predictive ability test (CVPAT) compared average squared losses at construct and overall levels {{liengaard2021}} {{sharma2023}}. Negative PLS-minus-benchmark differences favor PLS. Native loss differences and p-values are reported rather than treating every repeated prediction as an independent respondent. M1 did not have a corresponding native PLSpredict/CVPAT run in the supplied evidence, so M0's predictive results are not attributed to M1.

# Results and Discussion

## Data characteristics and measurement results

The analysis dataset contained 271 records, 20 indicators, and no missing item values. Each item had observed values within 1–5. Table 2 reports means and sample standard deviations of the unweighted four-item construct averages, together with M0's native measurement summaries. These descriptive averages are distinct from standardized, weighted PLS scores. Means ranged from 3.444 for PP to 3.590 for TR; the analysis makes no claim about subgroup differences because demographic data were unavailable.

[[TABLE:measurement]]

All 20 M0 outer loadings were between 0.801 and 0.859. Standardized alpha ranged from 0.840 to 0.879, rho_A from 0.845 to 0.880, and rho_C from 0.893 to 0.917. AVE ranged from 0.675 to 0.734. These results support internal consistency and convergent evidence under the specified reflective models. They do not establish that every pair of constructs is empirically distinct.

Table 3 shows the HTMT results. All point estimates were below 0.90, but the one-sided BCa upper bounds exceeded 0.90 for EXP–PP (HTMT = 0.860; upper bound = 0.908) and EXP–AD (HTMT = 0.828; upper bound = 0.913). Eight of ten pairs satisfied the upper-bound criterion; the other two did not establish discriminant validity under that criterion. This uncertainty remains relevant when interpreting paths involving Explainability, Privacy Protection, and Adoption Intention.

[[TABLE:htmt]]

All indicators had their highest loading on their assigned construct, and the Fornell–Larcker comparisons were descriptively favorable. These checks do not supersede the unfavorable HTMT bounds {{henseler2015}}. Adding structural paths in M1 also does not resolve this issue: HTMT is based on the same indicator correlations, and the unchanged data and indicator blocks retain the same point estimates. The findings motivate closer content and measurement evaluation, rather than automatic deletion or merging of substantively different constructs.

## Original model M0: paths and indirect associations

Table 4 presents the four M0 paths and three specific indirect effects. AIR (β = 0.260), EXP (β = 0.294), and PP (β = 0.315) were positively associated with TR; all three percentile intervals excluded zero. TR was positively associated with AD (β = 0.688, 95% CI [0.603, 0.764]). All seven reported path or indirect-effect p-values were below 0.001. The numerical ordering of the AIR, EXP, and PP coefficients is descriptive; no test of their pairwise differences was supplied.

[[TABLE:m0]]

M0 explained 61.64% of the variance in its TR score (R² = 0.616, 95% CI [0.533, 0.702]) and 47.33% in its AD score (R² = 0.473, 95% CI [0.364, 0.584]). The specific indirect associations through TR were 0.179 for AIR, 0.202 for EXP, and 0.217 for PP. These products are compatible with a trust-related indirect route within the specified model. They do not establish a temporal or causal mediation process, and M0 cannot demonstrate full mediation because it omits the corresponding direct paths.

Native inner VIF values were 2.393, 2.589, and 2.613 for AIR, EXP, and PP as predictors of TR; the single TR predictor of AD had VIF = 1.000. The corresponding f² values were 0.074, 0.087, 0.099, and 0.899. These structural diagnostics do not replace the separate assessment of discriminant validity.

The positive associations are consistent with the relevance of perceived dependability, understandable information, and safeguards to trust judgments {{lee2004}} {{shin2021}} {{dinev2006}}. Nevertheless, their interpretation concerns evaluations of an illustrated proposal. In particular, a high AIR response cannot be read as evidence that KidSense recognizes children's emotions accurately, and a high PP response cannot be read as evidence of tested privacy protection.

## Global discrepancies and exploratory model M1

M0's composite estimated-model SRMR was 0.064, below the commonly used descriptive 0.08 reference but above its native HI95 bound of 0.042 and HI99 bound of 0.048. Its estimated composite d_ULS and d_G likewise exceeded their bootstrap bounds. Therefore, significant paths and a moderate descriptive SRMR did not establish uniformly adequate fit. Table 5 contrasts the estimated-model diagnostics for M0 and M1 without treating their different measurement interpretations as interchangeable.

[[TABLE:fit]]

The exploratory M1 results are reported in Table 6. AIR, EXP, and PP retained positive associations with TR. After adding all three direct paths to AD, EXP → AD was positive (β = 0.337, p = 0.000771, 95% CI [0.127, 0.518]) and PP → AD was positive (β = 0.156, p = 0.027921, 95% CI [0.017, 0.297]). AIR → AD was not statistically supported (β = 0.046, p = 0.505143, 95% CI [−0.088, 0.180]). The TR → AD coefficient was 0.304 (p < 0.001). All three indirect associations through TR remained positive, with nominal p-values between 0.0048 and 0.0052.

[[TABLE:m1]]

Figure 2 displays the uncertainty in the four M1 paths into AD. The AIR interval spans zero; the other three percentile intervals exclude zero under the stated nominal inference procedure.

[[FIG:forest]]

M1's AD R² was 0.576, compared with M0's 0.473, an in-sample increase of 0.103. Its TR R² was 0.616 after rounding, with a small full-precision change because PLS scores were re-estimated. These results suggest that restricting every association with intention to a route through Trust may be too restrictive for this sample. However, Explainability's associations with PP and AD have unresolved HTMT uncertainty; the added paths should not be treated as definitive distinct mechanisms.

M1 has a saturated structural covariance specification: three covarying exogenous constructs predict TR, and all four preceding constructs predict AD. This saturation concerns the five-construct structural covariance part, not the entire 20-indicator measurement model. Its composite estimated-model SRMR was 0.031 and its composite discrepancies were below HI95, but the mixed-model SRMR and d_ULS remained above HI95 and HI99. The reduced composite discrepancies therefore do not independently validate the added paths or confirm the theory.

The nonsignificant AIR direct path also does not imply that AIR has no association with intention. Its M1 indirect estimate remained positive. The total AIR association was sensitive to interval method: the native percentile interval narrowly excluded zero, whereas the additional bias-corrected interval included zero. This reinforces the need for cautious interpretation of the AIR result, rather than a categorical claim of irrelevance or full mediation.

## Out-of-sample prediction in M0

All eight endogenous indicators had positive Q²predict values, ranging from 0.295 for AD3 to 0.474 for TR4 (Table 7). PLS had lower RMSE than LM for TR1, TR2, TR4, AD1, and AD2, but higher RMSE for TR3, AD3, and AD4. Using MAE, PLS performed better for seven of eight indicators, with AD4 the exception. The different counts reflect different loss functions and are not contradictory results.

[[TABLE:predict]]

CVPAT confirmed lower overall prediction loss than IA: the loss difference was −0.365179 (t = 6.497330, p < 0.001). The overall comparison with LM was smaller and not significant, with a difference of −0.009950 (t = 1.549895, p = 0.122338). Construct-level comparisons with LM were also not significant for TR or AD (Table 8). Thus, the study establishes improvement over the IA baseline but does not establish overall superiority over LM. Failure to reject the LM comparison is not evidence of predictive equivalence.

[[TABLE:cvpat]]

These findings illustrate why positive Q²predict and selected indicator-level error advantages should not be presented as comprehensive predictive validation {{shmueli2019}} {{sharma2023}}. Furthermore, AD predictions relied on observed TR indicators. The results support conditional response prediction under M0's recorded settings; they do not establish deployment performance, prediction from the three exogenous perceptions alone, or superior prediction by M1.

## Numerical verification and response-pattern sensitivity

Every native original-data cell matched the supplied CSV, preserving all 5,420 values and their order. Independently fitted M0 and M1 point results agreed with native coefficients and other checked point summaries within 5 × 10⁻¹⁰ and approximately 1.1 × 10⁻¹⁰, respectively. These tolerances describe the checked quantities, not every possible software output. The native rho_A values and native bootstrap draws were not independently reproduced.

All 21,680 exported held-out indicator errors matched observed minus predicted values. Recomputed RMSE and MAE agreed with native summaries within 2 × 10⁻¹⁵. Reconstructing the native folds and independently refitting the model reproduced individual predictions within 3 × 10⁻⁹ and PLS RMSE within 5.5 × 10⁻¹¹. CVPAT losses and test statistics were reproduced within 3.8 × 10⁻¹⁴; native p-values were retained. These checks provide an auditable numerical basis for the reported results without removing the substantive design limitations.

The response-pattern sensitivity analysis removed the ten all-item-uniform records, leaving 261 records. This exercise is reported in Appendix B as a change of analysis sample, not as a validated correction to participant eligibility. Earlier JSON calculations and alternative resampling implementations were retained as replication evidence; the manuscript's principal inferential tables use the corresponding native SmartPLS exports. Files with similar M1 filenames but a four-construct model without TR were excluded from the M1 evidence, which instead uses the corrected five-construct, seven-path export.

## Implications, limitations, and further research

For concept development, the results suggest examining reliability communication, comprehensible alert explanations, and perceived child-data safeguards together with trust. They do not justify maximizing trust irrespective of actual capability. Appropriate reliance requires that expectations remain calibrated to system performance and limitations {{lee2004}} {{hoff2015}}. The findings therefore support priorities for design research and evaluation, rather than a recommendation to deploy an untested emotion-detection system or a claim that parents will adopt it.

The content review identifies specific opportunities for instrument refinement. EXP3 combines understanding of confidence and possible error; PP spans specific controls and an overall appraisal; AD covers trial and conditional continuation. Cognitive interviews and pilot testing could examine whether parents interpret these items as intended. The elevated EXP–PP and EXP–AD HTMT bounds also motivate testing whether a general positive evaluation of the illustrated concept partly overlaps these domains. This is a plausible question for future work, not a demonstrated explanation of the current correlations.

Several limitations constrain inference. First, the cross-sectional design does not establish temporal ordering or causal effects. Second, descriptions and images may elicit expectations that differ from experience with a functioning system, and the favorable conditions stated in the intention prompt limit generalization to less favorable conditions. Third, same-source, same-occasion self-reports may reflect common method influences {{pods2003}}; no available diagnostic establishes their absence. Fourth, missing recruitment, demographic, and collection documentation prevents assessing coverage and representativeness from these files. Fifth, instrument provenance and the full AIR/TR wording remain to be documented, and discriminant validity is unresolved for two pairs.

Sixth, M1 was developed and estimated on the same sample, with nominal inference and no independent validation. Its higher R² and lower composite discrepancy do not establish better out-of-sample performance. Seventh, native prediction used repeated internal cross-validation rather than a prospectively collected external sample. A fair M0–M1 predictive comparison would require matched folds and the same predictor information, for example a deliberately specified early-antecedent comparison for both models. Finally, no evidence here establishes emotion-detection accuracy, child benefit, audited safeguards, or actual adoption. Subsequent research should separately test the implemented system and prospectively examine use after deployment under appropriate documented research procedures.

# Conclusion

Using 271 concept-evaluation responses, the original PLS-SEM model showed positive associations of Perceived AI Reliability, Explainability, and Perceived Privacy Protection with Trust, and a positive association of Trust with conditional Adoption Intention. M0 explained approximately 61.6% of Trust-score variance and 47.3% of intention-score variance. Independent computations reproduced the checked native results, supporting their numerical traceability.

The substantive interpretation remains qualified. The BCa upper-bound HTMT criterion was not satisfied for EXP–PP and EXP–AD, M0's estimated-model bootstrap discrepancy comparisons were unfavorable, and predictive superiority over the LM benchmark was not established. M1 increased in-sample intention R² and identified exploratory direct associations for EXP and PP, while the AIR direct association was not supported. These findings require independent model and measurement validation.

The study provides evidence about parental perceptions of an illustrated KidSense proposal and intentions conditioned on its assumed availability and functioning. It does not establish a causal mediation process, actual adoption, or the technical and privacy performance of an implemented system. The next empirical priority is to refine the instrument, document the original study procedures, and evaluate both the functioning design and prospective use with independent data.

# Declarations

## Author Contributions

[TO BE COMPLETED: confirm the CRediT roles of Ratih Titi Komala Sari, Widowati, and Adi Wibowo, and each author's approval of the final manuscript.] Computational and drafting assistance supported the current replication and manuscript preparation; all scientific claims, references, and journal disclosure requirements remain subject to author review.

## Data Availability Statement

The supplied analysis data, native SmartPLS exports, and computational verification materials have been archived in the researcher's GitHub repository: https://github.com/ukhuwahku01/Replikasi-SmartPLS-4 (backup commit 3bfed3738b5bd6198e8f11abd6756dc1d54dbadf). The archive includes checksums and distinguishes source files from derived checks. This statement concerns the files supplied for analysis; original recruitment and screening records, demographic data, and a numerical native random seed are not part of the available evidence. [TO BE COMPLETED: author-confirmed data-access terms and any required restrictions or consent conditions for sharing.] The current manuscript is a draft and has no assigned journal DOI.

## Funding

[TO BE COMPLETED: confirm the funding source and grant number, or confirm that no specific funding was received.] No funding claim has been inferred from the template's example text.

## Institutional Review Board Statement

[TO BE COMPLETED: identify the reviewing institution, approval or exemption decision, reference number, and date as applicable to the original respondent study.] Ethics approval or exemption cannot be established from the supplied analysis files and is not assumed to be inapplicable.

## Informed Consent Statement

[TO BE COMPLETED: describe how informed consent was obtained, including study information and any consent relevant to sharing research data.] A consent procedure cannot be verified from the indicator-only analysis dataset.

## Declaration of Competing Interest

[TO BE COMPLETED: each author must confirm relevant competing interests or confirm that none exist.] The template's example declaration has not been treated as an author-confirmed statement.

## Generative AI Assistance Disclosure

Generative AI assistance was used to support computational revalidation, organization of evidence, and preparation of this draft. [TO BE COMPLETED: authors should review and finalize this disclosure in accordance with the journal's current policy, verify the manuscript and references, and take responsibility for the submitted work.] The named human authors and their roles have not been inferred from software assistance.

# References

[[REFERENCES]]

# Appendix A. Available original questionnaire wording

The statements below reproduce the wording supplied by the researcher. The questionnaire names were Keterjelasan Penjelasan Sistem (EXP), Persepsi Perlindungan Privasi (PP), and Niat Menggunakan KidSense (AD). Before the AD block, respondents were instructed to imagine that KidSense was available, met security requirements, and functioned according to the design. The exact source wording of that introductory instruction was not supplied. The English operational definitions in Table 1 are explanatory descriptions rather than validated translations of an established external scale.

[[TABLE:items]]

[TO BE COMPLETED: insert the original AIR1–AIR4 and TR1–TR4 items and confirm response anchors before submission.] No item wording has been reconstructed from its code or statistical loading.

# Appendix B. Reproducibility and supplementary checks

The analysis archive preserves the original CSV, initial JSON and validation-workbook calculations, native M0 bootstrap and one-sided HTMT exports, native M0 PLSpredict/CVPAT export, M1 algorithm exports, and the corrected M1 bootstrap containing TR. Its integrity manifests permit source-file identification without relying on filenames alone. The input CSV SHA-256 is ab7e5333f80e50f89dcf90d885556f5b60bb30848052153e77325500af216624. A source-hash label in earlier JSON files did not match that CSV, so it was not treated as proof of a common raw-file lineage. Matching the native exports against all item values directly supplied the stronger analysis-data consistency check.

[[TABLE:sensitivity]]

The sensitivity estimates use the independent reflective path-weighted PLS implementation and the 261-record subset. They are not native SmartPLS bootstrap estimates and do not replace the primary n = 271 results. Differences show that response-pattern exclusions can alter estimates; without the original collection records, they do not identify which records should be excluded. Claims about initial response totals, timestamp duplicates, or consent/eligibility exclusions require verification against the original survey records.

