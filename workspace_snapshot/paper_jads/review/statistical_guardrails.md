# Statistical and scientific guardrails for the JADS manuscript

Scope: independent interpretation review using the verified native M0 outputs, corrected five-construct/seven-path M1 native bootstrap (`/workspace/validation/native_M1_corrected/native_M1_verified.json`), native one-sided BCa HTMT, and M0 PLSpredict/CVPAT. This note does not modify any manuscript output or introduce new hypothesis tests.

## Decisions that must remain visible in the paper

1. **Study identity:** a conceptual survey of parental perceptions after descriptions and design images only. Participants did not use a demo/prototype. It is not a technical emotion-recognition validation, security/privacy audit, usability trial, field deployment, adoption experiment, or validation of actual use/retention. Do not imply random assignment, causal identification, or representative sampling unless those facts are documented separately.
2. **Constructs:** AIR = Perceived AI Reliability, EXP = Explainability, PP = Perceived Privacy Protection, TR = Trust, AD = Adoption Intention. These are investigator operational definitions; exact EXP/PP/AD items are known. Exact AIR/TR items and scale-adaptation sources must not be invented. AD's prompt assumes KidSense is available, meets safety requirements, and functions as designed; AD4 is additionally conditional on future experience meeting expectations. Use “hypothetical, conditional adoption intention,” not “actual adoption.”
3. **Model status:** retain initial M0 and label added-direct-path M1 explicitly **post hoc/exploratory** wherever central findings are summarized, including abstract/conclusion. M0 is the initial specification; no evidence of preregistration was supplied, so do not call it preregistered or automatically confirmatory.
4. **Measurement limitations remain:** the native BCa one-sided 95% upper bounds exceed .90 for EXP–PP (.908139) and EXP–AD (.912789). Adding direct paths did not alter the item correlation-based HTMT results. Do not say “all constructs demonstrated discriminant validity,” “measurement model fully validated,” or “M1 resolved validity.”
5. **M1 fit interpretation:** M1 is saturated **at the structural covariance level**, not a perfectly fitting/fully saturated 20-indicator measurement model. Its estimated-versus-saturated composite-fit equality is expected once the original structural restrictions are removed and is not independent validation of the added paths. Mixed-model fit is a separate representation and must not be omitted merely because it is less favorable.
6. **Predictive evidence belongs to M0:** overall CVPAT favors PLS over IA, but not significantly over LM (p=.122338). M1 has not been subjected to the supplied PLSpredict/CVPAT run. Never transfer the M0 predictive metrics to M1 or claim M1's higher in-sample R² proves better out-of-sample prediction.

## Numeric cross-check: corrected native M1

Native SmartPLS 4.1.2.1, path weighting, standardized, 10,000 bootstrap samples, Complete, percentile, two-tailed alpha .05. These structural intervals use 2.5%/97.5% endpoints. A separate HTMT run uses selected BCa, one-tailed alpha .05 and exported upper95. Do not label all bootstraps BCa or all confidence intervals one-sided.

| M1 effect | Standardized estimate | Native p | Percentile 95% CI |
|---|---:|---:|---|
| AIR → AD direct | .045605 | .505143 | [−.087686, .180170] |
| AIR → TR | .262996 | <.001 | [.141933, .383128] |
| EXP → AD direct | .337191 | .000771 | [.127204, .517708] |
| EXP → TR | .292923 | <.001 | [.156110, .425043] |
| PP → AD direct | .156463 | .027921 | [.017163, .296779] |
| PP → TR | .313463 | <.001 | [.162077, .464231] |
| TR → AD | .304012 | <.001 | [.156881, .459000] |
| AIR → TR → AD | .079954 | .005153 | [.032983, .143367] |
| EXP → TR → AD | .089052 | .005141 | [.035225, .158803] |
| PP → TR → AD | .095297 | .004813 | [.037491, .168760] |

All p-values above are native nominal values. No familywise/FDR adjustment of these model paths is supplied; preserve the exploratory status rather than implying prespecified confirmatory testing. PP's direct p=.027921 is not <.001.

M1 R²(TR)=.6156559031 and R²(AD)=.5759044465. M0 R²(TR)=.6163994035 and R²(AD)=.4732948182. The AD increase is an in-sample difference across revised PLS specifications; do not present it as a tested predictive improvement or statistically significant R² difference. Scores are re-estimated under the altered PLS structural neighborhood, so even the otherwise unchanged TR equation has slightly different numerical coefficients/R².

### Two frequently confused AIR statements

- AIR **direct** association with AD in M1 is not statistically supported at .05. This does not demonstrate a zero population association, equivalence, absence of relevance, or that trust is the only possible mechanism.
- AIR **total** association in M1 is .125558, p=.047521; percentile95% CI [.002081,.253714] excludes zero, while the separately exported bias-corrected95% CI [−.002360,.249998] includes zero. If total AIR is mentioned, note this near-boundary method sensitivity. Do not replace its p with the direct-effect p or quietly select whichever interval favors a stronger conclusion.
- The earlier four-node/no-TR report's AIR→AD=.128194, p=.042186 does not belong to corrected M1. It must not be used in the paper's five-node M1 table.

## Mediation and causal interpretation

M0 omits all AIR/EXP/PP→AD direct paths; those paths are constrained to zero, not tested as nonsignificant. M0 alone therefore cannot classify full versus partial mediation. VAF=100% from that restricted model would be an arithmetic consequence of its specification.

M1 estimates positive indirect associations for all three antecedents and direct associations for EXP and PP; AIR's direct CI crosses zero. Describe this pattern directly. Do not elevate it to proven full mediation for AIR or a demonstrated causal pathway. Even a nonsignificant estimated direct path does not prove the true direct association is zero. The study does not establish temporal ordering or control all possible common causes. Measurement overlap for EXP–AD and EXP–PP also makes a definitive separation of their unique associations premature.

It is legitimate to say “a positive indirect association through trust was observed within the fitted model.” Avoid “trust causes adoption,” “trust completely transmits reliability,” “explainability increases real adoption,” or “privacy safeguards have been shown effective.” The data concern parents' impressions of a proposed design, not properties established in the working system.

## Measurement discussion and item editing

- All ten point HTMT values are <.90. Only EXP–PP=.859510 exceeds the stricter point threshold .85. These point-threshold statements do not override the selected upper-confidence-bound criterion.
- Upper95≥.90 means the .90 criterion was **not established**; it does not prove the population HTMT is ≥.90 or that the two constructs are the same.
- All ten upper95 bounds <1 satisfy a weaker criterion and do not justify switching from .90 after inspecting results.
- The 12 exact EXP/PP/AD items do not provide a clear automatic deletion/merger remedy. EXP concerns understanding explanations, PP concerns proposed privacy arrangements, and AD concerns intended behavior. Statistical overlap could reflect correlated perceptions, content breadth, response style, or other mechanisms, but none has been causally identified.
- EXP3 combines confidence and possible error; PP mixes global and specific privacy facets; AD spans trial, use and conditional continuance. Discuss operational breadth and review item understanding/content. Do not state these features are proven sources of the observed HTMT.
- No items were deleted to attain thresholds. If a future revision is made, base it on theory/content and respondent interpretation, retain initial results and label post-data changes exploratory. Assess the revised instrument on independent data. A higher alpha/AVE does not establish discriminant validity or all reflective assumptions.
- “Common-method bias was absent” is unsupported. Single-source self-report could contribute shared variance; the available checks do not diagnose or exclude that explanation. Do not invent Harman, marker-variable, procedural-control or multigroup-invariance results.

## Fit discussion

M0 estimated composite SRMR=.064091 is below the heuristic .08 yet exceeds its bootstrap HI95=.041905. Its d_ULS=.862615 exceeds HI95=.368764, and d_G=.190185 exceeds HI95=.168519; all also exceed corresponding HI99. Thus small descriptive SRMR and significant paths do not establish adequate overall fit.

M1 estimated composite SRMR=.031026, d_ULS=.202144 and d_G=.145440 are below their native HI95/HI99, but estimated and saturated composite statistics coincide. Report this as descriptive evidence under the expanded, structurally saturated specification, alongside the retained measurement overlap and the more restrictive M0 results. Do not say the comparison proves the added direct paths are true, optimal, generalizable, or theoretically validated. M1 mixed SRMR/d_ULS still exceed HI95 and HI99; mixed d_G exceeds HI95 but not HI99. Choosing composite versus mixed requires a substantive measurement interpretation, not selection by favorable fit.

## Predictive discussion

M0 uses Direct antecedents: TR indicators are observed inputs when AD is predicted. It is therefore conditional prediction, not early prediction of AD only from AIR/EXP/PP. Native 10-fold CV ×10 repetitions yields positive Q²_predict for 8/8 indicators, lower RMSE than LM for 5/8 and lower MAE for 7/8. Q²_predict is not blindfolding Q².

Overall squared loss: PLS=.6159416116, LM=.6258920076, a descriptive reduction of approximately1.59%, CVPAT p=.122338. This is not evidence of equivalence and not significant overall superiority at .05. Against IA, overall loss difference=−.3651788435, p<.001. Per-indicator advantages do not replace the overall comparison. Additional Holm adjustment across eight LM indicator tests retains only AD1, not both AD1 and TR4.

The 2,710 predictions per indicator represent 271 participants tested ten times, not 2,710 independent participants. Reproducing exported errors and CVPAT statistics verifies computation; it does not prove external validation, independent replication with new participants, or unbiased generalization beyond the sample.

## Suggested English discussion text

### Main interpretation

> The findings support a differentiated account of parental evaluations of the proposed KidSense design. In the initial specification, perceived AI reliability, explainability, and perceived privacy protection were positively associated with trust, which was positively associated with conditional adoption intention. The post hoc expanded model retained positive indirect associations through trust and additionally estimated direct associations from explainability and perceived privacy protection to adoption intention. The direct association for perceived AI reliability was not statistically supported. These patterns concern associations among perceptions elicited by descriptions and design images; they do not establish causal mechanisms or actual adoption.

### Expanded model

> Adding the three direct paths increased in-sample explained variance in adoption intention from .473 to .576. This comparison should be interpreted cautiously: the expanded model was specified after the initial results and was saturated at the structural covariance level. Consequently, the equality of estimated and saturated composite-fit statistics does not independently validate the added paths. Moreover, the expansion did not resolve the two HTMT confidence-bound limitations. The expanded results are therefore presented as exploratory rather than as a replacement for a fully validated initial model.

### Design implications

> The associations motivate further evaluation of how parents understand explanations and assess proposed privacy arrangements. They do not demonstrate that modifying either feature will increase adoption. Future work should test a functioning system, assess objective reliability and privacy safeguards separately, examine the clarity and coverage of the measurement items, and evaluate whether the proposed relationships persist in independent samples and during actual use. Because adoption intention was elicited under favorable availability, safety, and functionality assumptions, deployment claims require evidence beyond the present survey.

### Limitations

> Several limitations restrict interpretation. Participants evaluated descriptions and design images rather than interacting with a demo or prototype; the measures capture reported perceptions and hypothetical, conditional intentions. The single-source survey does not establish temporal or causal ordering, and shared measurement influences cannot be ruled out. Although reliability and convergent-validity summaries were favorable, the one-sided BCa upper confidence bounds for EXP–PP and EXP–AD exceeded the selected .90 criterion. The initial model also did not satisfy all bootstrap-based fit criteria. The expanded model was post hoc and structurally saturated, and its additional explanatory capacity was evaluated in the same sample. Predictive performance was assessed only for the initial model and did not show significant overall superiority over the linear-model benchmark. Independent data, documented sampling and eligibility procedures, and evaluation during actual use are needed before drawing broader claims about system performance or adoption.

Adjust sampling/eligibility wording only when new documentary evidence is available. The draft must not claim facts about recruitment, geography, respondent ages, ethics approval, consent, scale sources, data-collection dates, or stimulus duration that have not been supplied.

## Publication-critical evidence gaps (do not fill with invented facts)

- Actual sampling/recruitment frame, setting, dates, questionnaire order and stimulus materials/protocol.
- Participant profile and eligibility/exclusion decision records: 323→271 and D1/D2 have been reported but not verified from source rows.
- Ethics review/approval/exemption and documented consent procedure where applicable; absence of records here is not a finding that approval was absent.
- Source/adaptation/translation details for scales, including exact AIR/TR item text.
- Authors, affiliations, correspondence, funding, conflicts, data/code availability permissions.
- Literature-supported framing and verified citations: operational definitions provided by the investigator are not external theoretical quotations.

These gaps limit a submission-ready claim, not the ability to prepare a complete analytical draft with explicitly marked author-supplied fields. Keep author-to-complete facts out of apparently factual prose.
