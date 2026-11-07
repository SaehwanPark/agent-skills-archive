# Editing policy and release gates

## Hard requirements

1. No new or altered study design, population, inclusion/exclusion, treatment assignment, outcomes, results, effect estimates, uncertainty, or statistical method without author authorization and source evidence.
2. No fabricated citations, quotes, preliminary data, experimental details or claimed novelty.
3. Preserve DOI, PMID, registry identifiers, reference numbering, tables, code, equations and citation links; changes require verification.
4. No stronger causal or clinical-effectiveness claim than the design and source findings support. Do not substitute “effect” for “association” mechanically in a causal-inference manuscript; examine estimand and assumptions.
5. Retain mandatory reporting language and structured headings, especially CONSORT/STROBE/PRISMA where applicable. Terms such as *randomized*, *observational*, *confidence interval*, *hazard ratio*, and *robust standard errors* may be precise.
6. Never fabricate authorial experience or original research judgments. Do not conceal AI use when a venue requires disclosure. Editorial changes do not change provenance.
7. Never paste a confidential draft into an unapproved third-party tool. Local scripts only read local files.
8. If a scientifically accurate passage cannot be made appreciably better without increasing semantic risk, retain the original. An unchanged draft is a valid edit.

## Editorial priorities, not authenticity scores

- P0: integrity and argument continuity. Confirmed defects require resolution; most are not evidence of AI authorship.
- P1: high-impact discourse issues, section-function errors, argument specificity. Edit contextually.
- P2: surface/lexical tendencies. Require multiple contextual problems and a demonstrated reader benefit before editing.

## Anti-pattern resolution policies

1. **Word usage (buzzwords and rare choices)**: Eliminate synthetic, inflated, or buzzwordy vocabulary that human researchers rarely use (e.g., *testament*, *beacon*, *paramount*, *delve*, *pivotal*, *foster*, *elevate*, *intricate*, *tapestry*, *crucial nexus*). Replace them with plain, direct verbs and nouns. Strictly distinguish between buzzwords and authentic discipline-specific technical terms (e.g., *robust standard errors*, *heterogeneous treatment effects*, *pathway enrichment*).
2. **Predictability (structure and conclusions)**: Avoid monotonous, uniform paragraph lengths. Shape paragraph boundaries to reflect conceptual weight rather than arbitrary word quotas. Reject tidy list-like flows (rigid tripartite enumerations, "First... Second... Finally..." crutches) in narrative prose. Cut formulaic paragraph-final summary recaps (*"In summary..."*, *"Ultimately, these findings highlight..."*) that merely restate the paragraph's premise; let the finding itself lead into the next logical step. **Precedence rule:** Explicit study design, methodological sequencing, hypothesis enumeration (e.g., *“Aim 1 will establish feasibility. Aim 2 will evaluate effectiveness.”*), and standardized reporting conventions override stylistic diversity objectives; do not rewrite legitimate parallel scientific structures.
3. **Punctuation habits (em dashes and mechanical tics)**: Strictly limit em dashes (`—`). Distinguish legitimate paired parentheticals (e.g., *“The primary endpoint—the outcome specified before enrollment—was assessed at 30 days.”*) from repetitive rhetorical interruptions. Two well-formed parentheticals in separate sentences are a review candidate, not sufficient evidence to recommend an edit. Recommend a change only when dashes recur as a habit or demonstrably interrupt reading; then replace them with standard syntactic subordination, natural commas, parentheses for technical specifications, or clean sentence splits.
4. **Burstiness (rhythm and sentence variation)**: Review extended passages for repetitive sentence architecture, unnecessary parallelism, and monotonous progression. Vary sentence structure when doing so improves clarity, emphasis, or argument flow. Let scientific content determine sentence length; do not target particular word counts, rigid length ranges (e.g., forcing 6–12 or 25–40 word bins), or statistical distributions. Parallel sentences remain appropriate where scientific comparison or methodological sequencing requires them.

## Two depth modes

**Conservative**: preserve paragraph order, citations, technical terms, and most sentence architecture. Remove genuine redundancy, filler and unjustified rhetoric. Default.

**Substantive**: allow paragraph reordering, material restructuring, and clearer evidence–claim sequencing. Maintain a change log for argument moves and check all cross-references. Flag rather than supply any missing facts or scientific decisions.

## Decisions under uncertainty

If source evidence is missing, preserve a conservative scientifically plausible statement and add a separate author query; do not fill in missing values or references. If a linter flags a phrase but rewriting reduces precision, reject the suggestion. If a revision screen flags numerical differences, stop and compare with the source of truth. **A clean screen does not prove fidelity:** automated token checks cannot establish semantic equivalence or detect altered actors, unstated methods, or introduced study conditions. Mandatory claim-by-claim verification against the source is always required.
