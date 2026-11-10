# Final independent scientific audit of the JADS draft

**Finding: no material statistical or scientific correction is required within the reviewed scope.** The document remains a draft requiring the author-supplied study and declaration details already marked in its text. No manuscript or DOCX output was modified by this review.

## Actual artifacts inspected

- `/workspace/paper_jads/manuscript.md`: complete body prose, discussion, limitations, declarations and appendices.
- `/workspace/paper_jads/output/KidSense_JADS_Draft_Paper.docx`: actual title/front matter, abstract, ten tables, table/figure captions, numbered citations and 17 reference entries.
- `/workspace/paper_jads/output/paper_tables_full_precision_sources.json`: displayed table mappings and source paths.
- Relevant authoritative native M0 structural/measurement/fit evidence, corrected native M1 JSON, one-sided native HTMT and M0 prediction/CVPAT results were consulted for interpretation and numeric cross-checks.

The machine-readable companion audit records the reviewed DOCX version’s checksum and table display checks. Subsequent layout-only regeneration by the root agent may change the binary checksum without changing these scientific findings. All ten DOCX tables match the saved display mappings; this consistency check supplements the upstream evidence checks, rather than substituting for them.

## Supported findings in the actual prose and tables

1. **Concept exposure is described consistently.** Respondents saw descriptions and images; the paper does not claim demo/prototype interaction, measured AI emotion-recognition accuracy, audited privacy protection, actual adoption, retention, or child outcomes. Conditional availability/security/functionality assumptions and AD4's prospective condition are retained.
2. **M0 and M1 remain distinct.** M0 is the initial model; corrected M1 contains five constructs, seven paths and 20 indicators and is labeled post hoc/exploratory in the abstract, methods, results and conclusion. The four-node/no-TR exports are explicitly excluded. No M1 findings are presented as preregistered confirmation.
3. **Structural numbers are consistent with the proper native sources.** M0's four paths and three indirect estimates, SE/t/percentile intervals, R² intervals and ancillary f²/VIF summaries are consistent at displayed precision. Corrected M1's seven paths and three indirect estimates, native p-values and percentile95% intervals also match. PP→AD is correctly given p=.027921, not p<.001. The M1 AIR direct path is correctly unsupported, while its positive indirect association and method-sensitive total association remain distinguished.
4. **Mediation claims are bounded.** M0's omitted direct paths are explained as model restrictions. Neither M0 nor M1 is claimed to prove full or causal mediation. The direct AIR interval includes zero; nonsignificance is not stated as proof that its population association is zero.
5. **HTMT remains a limitation.** The table uses the dedicated native one-sided BCa95% upper bounds, with EXP–PP=.908139 and EXP–AD=.912789 failing the selected<.90 criterion. Its caption and methods distinguish these from two-sided structural percentile intervals and prior PythonBC. Unchanged indicator blocks and added structural paths are correctly stated not to resolve HTMT. Other favorable measurement checks do not override it.
6. **Fit is not overstated.** M0's descriptive SRMR<.08 is not treated as sufficient when its estimated composite discrepancies exceed bootstrap bounds. M1 saturation is limited to structural covariance, not the entire measurement model. Favorable M1 composite comparisons are contrasted with mixed output and do not independently validate added paths.
7. **Predictive claims are scoped to M0.** Counts5/8RMSE and7/8MAE, positiveQ²predict, conditionalADprediction using observedTR, and OverallLM CVPATp=.122338 are correct. The paper claims neither equivalence with LM nor significant overall superiority over LM. It states no supplied native M1 prediction run exists. Repeated2710predictions per indicator are not counted as2710 independent people.
8. **Sensitivity and provenance are qualified.** The n261 sensitivity retains its Python-only point-estimate label, with no fabricated bootstrap inference. No response-pattern rule is treated as proof of invalid respondents. The CSV hash discrepancy is acknowledged. The stated Git backup commit exists in the local repository; remote/public access and permissions should not be inferred solely from that fact.
9. **Citations have traceable known metadata, not completed external verification.** Seventeen in-text citation keys resolve to17 numbered journal entries and no unresolved draft markers remain in DOCX citation/table/figure references. The bibliography does not claim the researcher-defined scales were taken from those articles. This pass did not resolve DOI URLs, inspect full texts or independently verify all metadata online. The author should verify full texts and relevance before submission. General privacy/acceptance publications are conceptual framing, not direct evidence of child-system validity.
10. **Missing facts are visibly marked.** Recruitment, anchors, exact AIR/TR items, ethics/consent, author roles, funding/conflicts and data-access terms are not invented as completed study facts. The manuscript does not substitute template example declarations for evidence.

## Corrections and residual completion items

- **Material numerical/scientific corrections:** none observed.
- **Affiliation/contact provenance:** the root agent confirmed that the author names, affiliations and corresponding-author email were explicitly provided in the user’s asynchronous reply this turn. No author metadata correction is required.
- **Submission readiness:** keep the existing author-to-complete fields until the relevant facts are supplied. Do not characterize a draft with unresolved ethics/instrument/sampling declarations and unverified external reference details as ready for submission.
- **Scope limit:** this is a scientific/prose/table audit, not a new broad computational rerun, external bibliography audit, or final visual/layout acceptance test. Figures were reviewed through their substantive captions and described intervals; the root authoring workflow owns image/render inspection.
