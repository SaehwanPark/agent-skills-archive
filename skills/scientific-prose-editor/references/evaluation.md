# Evaluation design and quality gate

**Primary target:** blinded scientific-editor preference and calibrated scientific quality, never an AI-detector pass rate. **Hard gate:** scientific meaning preserved and policy requirements satisfied. **Secondary diagnostics:** exploratory stylistic patterns without assigned directionality, and, only where approved, independent detector outcomes with false-positive controls.

## Metric hierarchy

Evaluation metrics follow a strict hierarchy to prevent optimizing proxies:

| Metric | Role |
| --- | --- |
| Scientific fidelity | Mandatory acceptance criterion |
| Expert-rated clarity and naturalness | Primary quality outcomes |
| Specificity and argument coherence | Primary editorial outcomes |
| Sentence-length variation | Exploratory diagnostic |
| Punctuation and vocabulary patterns | Exploratory diagnostic |
| Detector results | Independent research outcome |

Avoid assigning directionality to exploratory diagnostics before reviewer evidence supports it. For example, a higher sentence-length standard deviation is not intrinsically superior—it can be artificially inflated by arbitrary sentence splitting. Exploratory diagnostics describe prose characteristics but are not optimization targets.

## Design

1. Collect permissioned, provenance-documented scientific passages. Stratify across manuscripts (abstract, Methods, Results, Discussion), grants (aims, significance, approach), proposals and technical documentation. Avoid source-family leakage between development and held-out evaluation.
2. For each passage, produce a conservative edited variant and optionally a substantive variant. Include human-only, human+AI-polished, AI-drafted+human-revised and fully AI-drafted provenance strata if legitimately documented; do not infer provenance from style, publication dates or detector outputs.
3. Conduct two complementary independent experiments:
   - **Blinded paired preference:** scientific reviewers compare A/B with concealed treatment order. Score clarity, naturalness, fidelity (1–5), preference and qualitative reasons. `prepare_eval.py` and `score_eval.py` implement this design. Keep the evaluation rubric independent of internal editorial heuristics: reviewers must judge writing quality on unprimed criteria without being prompted by the four anti-pattern categories to prevent circular evaluation.
   - **Unpaired authorship-perception:** distinct reviewers rate one version per source family, before a pattern checklist, and freeze ratings. Use the prior Phase 1 v0.3 reviewer workflow if needed. Do not mix this with the paired arm or reveal multiple versions to one unpaired reviewer.
4. Independently adjudicate scientific fidelity against protocol, tables and citations. Record critical violations with provenance; a clean regex screen is insufficient.
5. Track exploratory diagnostics across the four stylistic dimensions (descriptive diagnostics, not optimization scores):
   - **Word usage**: descriptive incidence of uncharacteristic non-human vocabulary and promotional buzzwords (*testament, beacon, paramount, delve, pivotal, foster, elevate, intricate, tapestry, crucial nexus*).
   - **Predictability**: descriptive distributions of paragraph lengths, presence of list-like flows in narrative prose, and paragraph-final summary recaps.
   - **Punctuation habits**: descriptive em-dash frequency and clustering, distinguishing single paired parentheticals from repetitive interruptions across sentences.
   - **Burstiness**: descriptive sentence-length variation and syntactic variety; cadence is evaluated qualitatively rather than targeting statistical cutoffs.
6. For detector audits, reserve a held-out cohort and preregister tools, versions, data-sharing permissions, thresholds and outcomes. Report per-class confusion matrices, FPR on documented human texts, uncertainty and length/genre stratification. Do not tune the editor against that held-out set or call scores proof of human authorship.

## Suggested operational thresholds (design goals, NOT measured success)

- 0 unresolved critical scientific-fidelity violations in shipped edits.
- 100% of changed numerical/citation tokens manually cleared and documented.
- >50% of paired preference votes favor the edited version **on held-out reviewer data**, with uncertainty reported; threshold does not alone establish success.
- Nonnegative average change in fidelity ratings, with concerns adjudicated.
- Report patterns that reviewers reliably agree are defects; do not assign universal AI-feel weights based on heuristics.

## Evaluation manifest

JSONL, one object per passage pair, required keys:

```json
{"item_id":"docA-intro-1","source_family":"docA","genre":"manuscript","section":"introduction","fact_sheet":"Verified: population, design, aims, results and citations used to assess fidelity.","original":"...","edited":"...","rights_status":"approved","provenance_documented":true}
```

`fact_sheet` is required, must be curator-verified and is shown to reviewers as neutral source-of-truth context. It must not expose which text is edited. `rights_status=approved` and `provenance_documented=true` are **attestations by the dataset curator**, not proof provided by the program. Do not mark hypothetical or synthetic passages as externally validated; use synthetic data only for software unit tests and walkthroughs. `prepare_eval.py` refuses unapproved text and duplicate pairs.

Ratings CSV columns are emitted by `prepare_eval.py`. `preferred` is A/B/TIE; `quality_A`, `quality_B`, `naturalness_A`, `naturalness_B`, `fidelity_A`, `fidelity_B` are integers 1–5. A reviewer should rate scientific fidelity only when supplied enough source context to judge it; otherwise the curator must collect fidelity separately and not misrepresent the resulting ratings.

## Analysis

- Unit of resampling: **source family**; paired reviewer ratings are correlated. `score_eval.py` reports family-level cluster-bootstrap intervals with <3 families withheld; it is descriptive, not a publication-grade inferential engine.
- Inspect worst cases and false positives before changing style policies.
- Treat reviewer disagreement as uncertainty, not as grounds for coercing consensus.
- Freeze the rubric and benchmark split before comparing alternative skills or detector readings.
