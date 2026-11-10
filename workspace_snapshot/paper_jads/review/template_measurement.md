# Independent JADS template and measurement review

## Template findings and authoring recommendations

Source: `/workspace/attachments/2f82fc2f-7333-4b16-932a-c23db07d7717/JADS-template.docx`, inspected read-only with python-docx and WordprocessingML.

1. **Language and structure.** The template is written in English; English is the reasonable manuscript default. No explicit abstract word limit, keyword count, manuscript word/page limit, or reference minimum was found. Main headings: Introduction; Literature Review; Methodology; Results and Discussion; Conclusion; Declarations; References. Front matter: title, authors/affiliations, editorial dates, Abstract, Keywords. Declarations contain Author Contributions, Data Availability Statement, Funding, Institutional Review Board Statement, Informed Consent Statement, and Declaration of Competing Interest.
2. **Actual layout.** The supplied file has one A4 section, approximately 210×297 mm. Margins: top 16.0 mm; bottom 22.1 mm; left 13.0 mm; right 14.0 mm. Its actual `w:cols` omits `num=2`, meaning **single column**, although copied boilerplate mentions columns. Preserve actual document section/page settings rather than introducing two columns from that generic prose. Do not add manual pagination or heading numerals where template numbering already supplies them.
3. **Typography inconsistencies.** Visible instructions specify title Times New Roman 17 pt, authors 11 pt, affiliations italic 9 pt, main headings bold 11 pt, secondary headings 13 pt. Actual style definitions conflict in places: Heading 1 style is 10 pt but visible heading runs 11 pt; Author style is 13 pt but author runs 11 pt. Body runs explicitly use Times New Roman and inherit approximately 11 pt; document defaults are Calibri 11 pt. Preserve the intended visible template formatting through explicit runs/styles, then inspect rendered output. Abstract heading is 9 pt; keywords style is 8 pt. Caption styles use 10 pt Junicode in the actual file, while figure-label guidance asks Times New Roman 10 pt.
4. **Tables and figures.** Table titles belong above tables (`table head`); figure captions below images (`figure caption`). Refer to each table/figure before placement. The example table is a specimen, not study data; remove it. Equations are numbered consecutively at right if used. For readable content, use separate descriptive and measurement tables rather than an overwide combined table. Retain the 1–5 scale note and define all abbreviations.
5. **Citations and references.** Use consecutive bracketed numeric citations, such as [1], ordered by first appearance; punctuation follows the bracket. The template prefers published, accessible international journal articles and international books only if needed, with DOI/publisher links. Website links are limited to primary-data sources in its stricter rule; later boilerplate examples are looser. Prefer peer-reviewed journal sources for theory/methods and avoid copying example/fake DOI links. List all authors when fewer than six; do not use et al. for those references. No in-press-only references. Citation titles use sentence case. This is IEEE-like numbering, not author–date.
6. **Editorial metadata are placeholders.** The header hardcodes Vol. 5, No. 3, September 2024 and pp. 1449–1461 (first-page pp. X–X); front matter includes sample Received/Revised/Accepted dates. These are not facts about this paper. Retain journal name, ISSN and visual structure, but mark issue/date/page metadata as editorial placeholders/draft. Do not manufacture publication or acceptance status.
7. **Declarations require real evidence.** Template examples saying no funding, no conflicts, ethics Not applicable, informed consent Not applicable, author contributions, and data on request are example text, not evidence. Do not adopt them automatically. Author identities, affiliations, recruitment, ethics review/approval/exemption, consent procedures, funding and contributions remain author-supplied facts. The existing authorized GitHub backup can support a carefully scoped data/code-availability statement only after checking actual repository contents and access.

## Measurement and descriptive results ready for use

These are **M0 primary-model** measurement values. Means and SDs are computed from each respondent's **unweighted arithmetic average of four original 1–5 items**, then summarized across 271 respondents (sample SD, ddof=1). They are not standardized PLS score means/SDs. Reliability/AVE/loadings below are the **original-sample native SmartPLS M0** values retained in the independently checked measurement JSON; rho_A is native and had no original Python comparison. All 271×20 cells are complete; all item values are integer 1–5. Each raw four-item average spans observed 1.00–5.00.

### Suggested descriptive table

| Construct | Items | n | Mean | SD |
|---|---:|---:|---:|---:|
| AIR | 4 | 271 | 3.453 | 0.836 |
| EXP | 4 | 271 | 3.497 | 0.794 |
| PP | 4 | 271 | 3.444 | 0.875 |
| TR | 4 | 271 | 3.590 | 0.838 |
| AD | 4 | 271 | 3.562 | 0.812 |

Note: Summaries describe ratings of the presented KidSense concept, not evaluated prototype use or observed adoption. These descriptive values do not establish representativeness or significant differences between constructs. Item/construct abbreviations must be defined from the investigator's operational definitions.

### Suggested measurement table (M0)

| Construct | Standardized alpha | rho_A | rho_C | AVE | Outer-loading range |
|---|---:|---:|---:|---:|---:|
| AIR | 0.859 | 0.860 | 0.904 | 0.703 | 0.822–0.852 |
| EXP | 0.840 | 0.845 | 0.893 | 0.675 | 0.801–0.837 |
| PP | 0.879 | 0.880 | 0.917 | 0.734 | 0.851–0.859 |
| TR | 0.862 | 0.863 | 0.906 | 0.707 | 0.831–0.847 |
| AD | 0.847 | 0.848 | 0.897 | 0.685 | 0.820–0.840 |

Note: All constructs retain four reflective indicators; n=271. Alpha is standardized Cronbach alpha, not raw-covariance alpha. Measurement results are model-specific because PLS weights can change in M1; do not silently mix M0 and M1 loadings/rho_C/AVE. Favorable internal consistency/AVE/loading values do **not** establish complete discriminant validity: EXP–PP and EXP–AD remain the principal HTMT concerns documented in the native one-sided analysis.

## Claims to preserve or avoid

- The survey exposure was **descriptions/images of a proposed concept**. Do not describe deployment, hands-on use, an operational prototype evaluation, a longitudinal study, or child emotion-recognition accuracy/security testing.
- AIR is perceived AI reliability; PP is perceived privacy protection; EXP is investigator-operationalized perceived understanding of explanations. These are perceptions, not objective AI performance or a security/privacy audit.
- AD is hypothetical conditional adoption intention, including conditions on availability/safety/functionality and future expectations—not realized adoption, retention, or unconditional demand.
- Full AIR/TR item wording is not present in the confirmed instrument evidence. Do not invent those items, scale provenance or adaptation citations. Preserve available item labels AIR1–AIR4/TR1–TR4 and flag the instrument-completion requirement for authors.
- No respondent demographics, sampling frame, fieldwork dates, recruitment mode, geographical representativeness, ethics approval/exemption, or independently verified screening flow can be inferred from the 20-item CSV. The reported 323→271 selection remains unverified without raw source records.
- Positive path/indirect estimates are associations. Neither bootstrap significance nor exploratory M1 establishes causality or causal mediation.

## Traceable sources

- CSV: `/workspace/smartpls4_native/KidSense_SmartPLS4_Input_271.csv`.
- Measurement audit: `/workspace/validation/native_bootstrap/measurement/native_measurement_verification.json`.
- Native M0 source: `/workspace/attachments/881a3fc0-4752-40da-b923-58fd2e3add93/KidSense_Bootstrap_10000.xlsx`; original estimates checked in the measurement audit, 35 comparisons within 1e-8.
- Exact machine-readable table: `measurement_descriptives_M0.csv` beside this note.
- No source or authoring/template files were modified by this review.
