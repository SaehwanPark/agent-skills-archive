# Taxonomy: 26 candidate scientific-editing patterns

**Status:** Literature-informed, not empirically validated as an AI-authorship classifier or weighted scoring rubric. Many are universal scientific-writing defects or preservation constraints, not AI-specific signals.

P0 is an *editorial/integrity* priority (not evidence of authorship); P1 is discourse quality; P2 is a lower-priority stylistic hypothesis. Read individual false-positive guards before suggesting changes.

## Scientific integrity and authorial judgment

### R01 · Unsupported claims and references (P0)

- **Description:** Background or discussion asserts findings without a verifiable source or with fabricated bibliographic details.
- **Evidence:** direct_empirical / scientific_risk_not_specific_authorship_cue; research status does not establish authorship.
- **Check before changing:** General domain definitions may not require citation; journal conventions differ.
- **Proposed intervention:** Verify every substantive referenced claim; mark unverifiable references for author review.
- **Evidence references:** S09, S11

### R02 · Overstatement of evidence or clinical utility (P0)

- **Description:** Wording asserts definitive effects, causal implications, or clinical benefit beyond underlying analysis.
- **Evidence:** research_informed_hypothesis / not_established; research status does not establish authorship.
- **Check before changing:** Strong claims are appropriate when design and evidence justify them.
- **Proposed intervention:** Constrain claim to supplied estimand, population, study design, and measurements.
- **Evidence references:** S11, S12, S13

### R03 · Changed quantitative or methodological facts (P0)

- **Description:** Editing changes n, effect size, confidence interval, p-value, comparator, endpoint, method, eligibility, or code identifier.
- **Evidence:** policy_invariant / not_an_ai_cue; research status does not establish authorship.
- **Check before changing:** Formatting normalization is acceptable only if numeric meaning and notation remain equivalent.
- **Proposed intervention:** Block output until source text, tables, and methods match; raise discrepancy.
- **Evidence references:** S11, S12, S13

### R04 · Causality versus association conflation (P0)

- **Description:** Observational associations are rewritten as interventions causing changes or as demonstrated mechanisms.
- **Evidence:** policy_invariant / not_an_ai_cue; research status does not establish authorship.
- **Check before changing:** Causal inference designs can support causal language if assumptions and estimand warrant it.
- **Proposed intervention:** Keep causal scope aligned with research design and source claims.
- **Evidence references:** S12

### R05 · Fabricated specificity (P0)

- **Description:** Editor fills in absent sample size, measurement details, computational implementation, references, or preliminary data.
- **Evidence:** policy_invariant / not_an_ai_cue; research status does not establish authorship.
- **Check before changing:** None: unsupported facts must never be supplied as though known.
- **Proposed intervention:** Flag missing information explicitly; do not supply plausible values.
- **Evidence references:** S09, S11

### R06 · Inconsistent cross-section claims (P0)

- **Description:** Abstract, Results, and Discussion describe different populations, endpoints, or effect directions.
- **Evidence:** research_informed_hypothesis / scientific_risk_not_specific_authorship_cue; research status does not establish authorship.
- **Check before changing:** Changes may reflect clearly labeled prespecified sensitivity analyses; compare like with like.
- **Proposed intervention:** Check against source-of-truth result tables and primary analysis specification.
- **Evidence references:** S11, S12, S13

### R07 · Altered authorial scientific judgment (P0)

- **Description:** Editing invents research gaps, hypotheses, mechanism claims, aims, or strategic priorities that were not authorized by the author.
- **Evidence:** policy_invariant / not_an_ai_cue; research status does not establish authorship.
- **Check before changing:** Explicit author-approved revisions to substantive plans are permissible outside polishing mode.
- **Proposed intervention:** Preserve the author’s scientific decisions and mark suggestions as questions rather than inserting them.
- **Evidence references:** S10, S11

## Discourse and scientific argument

### D01 · Redundant restatement (P0)

- **Description:** Adjacent sentences repeat the same claim without new evidence, distinction, or implication.
- **Evidence:** direct_empirical / associated_in_study; research status does not establish authorship.
- **Check before changing:** Repetition may aid orientation in abstracts or long technical documents; check communicative role.
- **Proposed intervention:** Merge repeated claims; retain the most precise statement and necessary link.
- **Evidence references:** S01, S02

### D02 · Broken logical thread (P0)

- **Description:** Claim-to-evidence progression jumps, or key qualifiers disappear between sentences.
- **Evidence:** direct_empirical / associated_in_study; research status does not establish authorship.
- **Check before changing:** Dense mathematical prose may use separately defined terminology; consult equations and cross-references.
- **Proposed intervention:** Identify premises and evidence; request missing support rather than invent bridges.
- **Evidence references:** S01, S02

### D03 · Generic significance without study-specific stakes (P1)

- **Description:** Introduction or grant significance states broad importance without concrete population, gap, or decision relevance.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** A general opening can be justified for interdisciplinary audiences.
- **Proposed intervention:** Anchor to supplied burden, gap, mechanism, or research question; do not invent numbers.
- **Evidence references:** S02

### D04 · Results replaced by evaluative commentary (P1)

- **Description:** Abstract or Results paragraphs say findings are promising/important without the measurable result.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Some qualitative research appropriately reports themes rather than effect sizes.
- **Proposed intervention:** Lead with measured results already present in source material; reserve interpretation for Discussion.
- **Evidence references:** S06, S07, S12, S13

### D05 · Inappropriate rhetorical-move balance (P1)

- **Description:** Abstract overweights interpretation, omits context/method or organizes discourse moves unnaturally for target journal.
- **Evidence:** direct_empirical / associated_in_abstract_corpora; research status does not establish authorship.
- **Check before changing:** Structured abstract rules and journal formats override any learned frequencies.
- **Proposed intervention:** Check section function against journal and reporting guidelines; preserve required headings.
- **Evidence references:** S06, S15

### D06 · Affective/promotional stance imbalance (P1)

- **Description:** Positive evaluative language dominates evidence reporting; hedges/boosters lack an evidentiary basis.
- **Evidence:** direct_empirical / associated_in_abstract_corpora; research status does not establish authorship.
- **Check before changing:** Strong recommendations can be justified; standards differ between grants and manuscripts.
- **Proposed intervention:** Replace emotive judgments with evidence-tied interpretation and justified uncertainty.
- **Evidence references:** S07, S06

### D07 · Generic future work or implications (P1)

- **Description:** Conclusion prescribes more research or broad adoption without explaining which uncertainty remains.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** A concise future-work statement may be required by a journal or grant.
- **Proposed intervention:** Specify the actual limitation, unanswered question, and relevant next step only if supplied.
- **Evidence references:** S02

### D08 · Overly symmetric rhetorical framing (P2)

- **Description:** Repeated balancing constructions force two-sided treatment where evidence is asymmetric.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Balanced discussion is essential when true uncertainty or conflicting evidence exists.
- **Proposed intervention:** Represent evidentiary balance faithfully, not rhetorically.
- **Evidence references:** S02

### D09 · Unnecessary metacommentary (P2)

- **Description:** Sentences announce what the manuscript will discuss instead of advancing its argument.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Roadmaps are useful in long technical documents; aims and objectives often require explicit signposting.
- **Proposed intervention:** Retain navigation when functional; otherwise replace with the substantive claim.
- **Evidence references:** S06

### D10 · Overgeneralized comparison with prior work (P1)

- **Description:** Prior studies are summarized as uniformly inadequate without concrete contrast in population, design, outcome, or methods.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** A synthesis of heterogeneous studies may require broad framing supported by citations.
- **Proposed intervention:** Specify verified comparative dimensions and soften claims unsupported by supplied sources.
- **Evidence references:** S09, S11

### D11 · Ill-fitting authorial presence (P2)

- **Description:** Self-mentions, framing statements, or attitude markers do not fit genre and local reporting style.
- **Evidence:** direct_empirical / associated_in_abstract_corpora; research status does not establish authorship.
- **Check before changing:** First person is often recommended and not an AI cue; discipline-specific conventions vary.
- **Proposed intervention:** Adapt only to target journal/discipline; never systematically ban “we”.
- **Evidence references:** S06, S07, S15

## Surface patterns

### L01 · LLM-associated lexical clustering and buzzwords (P2)

- **Description:** Disproportionate repeated clusters of words reported as LLM-associated or synthetic buzzwords that humans rarely choose in scientific prose (e.g., delve, underscore, pivotal, intricate, testament, beacon, elevate, foster, paramount, tapestry, crucial nexus).
- **Evidence:** direct_corpus_observational / aggregate_corpus_marker_only; research status does not establish authorship.
- **Check before changing:** Single words are common legitimate English; prevalence varies by year, discipline, and authorship. Never ban or classify from lexical hits.
- **Proposed intervention:** Check whether terms contribute precision; remove ornamental repetition and replace hollow buzzwords with plain, precise scientific language.
- **Evidence references:** S04, S05, S14

### L02 · Stock emphasis and intensifiers (P2)

- **Description:** Terms such as groundbreaking or transformative appear without evidentiary basis.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Innovation sections in grants necessarily argue significance; evaluative terms may be supported.
- **Proposed intervention:** Convert to specific evidence-supported scope or outcome.
- **Evidence references:** S07

### L03 · Mechanical transition stacking (P2)

- **Description:** Successive sentences rely on formulaic transitions despite obvious logical relation.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Transitions can genuinely help complex multi-step reasoning, accessibility, and technical prose.
- **Proposed intervention:** Keep transitions where they encode actual causation/contrast; remove redundant ones.
- **Evidence references:** S02

### L04 · Uniform sentence construction and low burstiness (P2)

- **Description:** Closely repeated syntactic frames, steady metronomic sentence lengths (e.g., constant 18–24 words), or uniform clause openings reduce rhythm variation and create a flat, low-burstiness cadence.
- **Evidence:** cross_domain_empirical / conditional; research status does not establish authorship.
- **Check before changing:** Parallelism is essential in aims, hypotheses, and methods; uniformity alone is not a problem.
- **Proposed intervention:** Vary construction and inject burstiness by alternating concise, punchy assertions (6–12 words) with compound, evidence-rich explanatory sentences (25–40 words), and varying opening structures.
- **Evidence references:** S02

### L05 · Unnecessarily abstract nominalizations (P2)

- **Description:** Abstract nouns obscure who performed an action or what was measured.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Established statistical and biomedical terms should not be replaced with casual synonyms.
- **Proposed intervention:** Use direct technical verbs when precise, while retaining necessary formal terminology.
- **Evidence references:** S02

### L06 · Decorative concluding recap (P2)

- **Description:** Paragraph ends with a polished but non-informative restatement of broad significance.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** A conclusion is legitimately required in most abstracts and papers.
- **Proposed intervention:** Make the concluding sentence answer the specific study question.
- **Evidence references:** S02

### L07 · Mechanical punctuation habits and em-dash overuse (P2)

- **Description:** Heavy, repetitive reliance on em dashes (—) to insert parenthetical commentary, create dramatic pauses, or stitch clauses together; mechanical colon/semicolon stacking.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Em dashes and colons have legitimate technical uses; evaluate whether they form a repetitive parenthetical crutch that breaks prose cadence.
- **Proposed intervention:** Replace overused em dashes with standard syntactic subordination, natural commas, parentheses for technical qualifiers, or clean sentence splits.
- **Evidence references:** S02

### L08 · Predictable paragraph architecture and list-like flows (P2)

- **Description:** Monotonously uniform paragraph lengths across a section, rigid list-like flows (cataloging points with formulaic enumerations), and predictable summary conclusions ending every paragraph with a redundant recap.
- **Evidence:** research_informed_hypothesis / unvalidated_hypothesis; research status does not establish authorship.
- **Check before changing:** Specific aims and sequential protocols legitimately use parallel list structures.
- **Proposed intervention:** Vary paragraph length based on argument complexity; replace tidy list-like enumerations with substantive logical transitions; remove predictable concluding sentences that merely rephrase previous statements.
- **Evidence references:** S02, S06

## Reference key

- **S01:** Doru et al. (2025), Medical student essays and expert AI judgments — https://mededu.jmir.org/2025/1/e62779
- **S02:** Russell, Karpinska & Iyyer (ACL 2025), Human identification of AI-written nonfiction — https://aclanthology.org/2025.acl-long.267/
- **S03:** Khera et al. (2025), Scientific writing in the era of LLMs — https://pubmed.ncbi.nlm.nih.gov/40814778/
- **S04:** Kobak et al. (Science Advances 2025), Excess vocabulary in biomedical abstracts — https://doi.org/10.1126/sciadv.adt3813
- **S05:** Kousha & Thelwall (Scientometrics 2026), LLM-associated words in full scientific articles — https://doi.org/10.1007/s11192-026-05601-5
- **S06:** Deng, Li & Gao (JEAP 2026), Rhetorical moves and metadiscourse in abstracts — https://doi.org/10.1016/j.jeap.2026.101731
- **S07:** Human-written vs ChatGPT-generated texts: Stance in English research article abstracts (System 2025) — https://doi.org/10.1016/j.system.2025.103842
- **S08:** Park, Jeong & Kim (EMNLP Industry 2026), Style as a Confound — https://aclanthology.org/2026.emnlp-industry.109/
- **S09:** Davis & Mahmoud (PMLR 2026), Reference hallucinations — https://proceedings.mlr.press/v318/davis26a.html
- **S10:** NIH (2025), Supporting Fairness and Originality in NIH Research Applications — https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html
- **S11:** ICMJE (January 2026), AI use by authors — https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html
- **S12:** EQUATOR Network, STROBE reporting guideline — https://equator-network.org/reporting-guidelines/strobe/index.html
- **S13:** EQUATOR Network, CONSORT 2025 reporting guideline — https://equator-network.org/reporting-guidelines/consort/
- **S14:** Geng & Trotta (Findings ACL 2025), Human-LLM coevolution in academic writing — https://aclanthology.org/2025.findings-acl.657/
- **S15:** Zhang & Zhang (JEAP 2025), Disciplinary variation of metadiscourse — https://doi.org/10.1016/j.jeap.2025.101540

The reference summaries were assembled in Phase 1 and carry source-specific limitations; see the research baseline.
