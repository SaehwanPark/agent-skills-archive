# Editing policy and release gates

## Hard requirements

1. No new or altered study design, population, inclusion/exclusion, treatment assignment, outcomes, results, effect estimates, uncertainty, or statistical method without author authorization and source evidence.
2. No fabricated citations, quotes, preliminary data, experimental details or claimed novelty.
3. Preserve DOI, PMID, registry identifiers, reference numbering, tables, code, equations and citation links; changes require verification.
4. No stronger causal or clinical-effectiveness claim than the design and source findings support. Do not substitute “effect” for “association” mechanically in a causal-inference manuscript; examine estimand and assumptions.
5. Retain mandatory reporting language and structured headings, especially CONSORT/STROBE/PRISMA where applicable. Terms such as *randomized*, *observational*, *confidence interval*, *hazard ratio*, and *robust standard errors* may be precise.
6. Never fabricate authorial experience or original research judgments. Do not conceal AI use when a venue requires disclosure. Editorial changes do not change provenance.
7. Never paste a confidential draft into an unapproved third-party tool. Local scripts only read local files.

## Editorial priorities, not authenticity scores

- P0: integrity and argument continuity. Confirmed defects require resolution; most are not evidence of AI authorship.
- P1: high-impact discourse issues, section-function errors, argument specificity. Edit contextually.
- P2: surface/lexical tendencies. Require multiple contextual problems and a demonstrated reader benefit before editing.

## Anti-pattern resolution policies

1. **Word usage (buzzwords and rare choices)**: Eliminate synthetic, inflated, or buzzwordy vocabulary that human researchers rarely use (e.g., *testament*, *beacon*, *paramount*, *delve*, *pivotal*, *foster*, *elevate*, *intricate*, *tapestry*, *crucial nexus*). Replace them with plain, direct verbs and nouns. Strictly distinguish between buzzwords and authentic discipline-specific technical terms (e.g., *robust standard errors*, *heterogeneous treatment effects*, *pathway enrichment*).
2. **Predictability (structure and conclusions)**: Avoid monotonous, uniform paragraph lengths. Shape paragraph boundaries to reflect conceptual weight rather than arbitrary word quotas. Reject tidy list-like flows (rigid tripartite enumerations, "First... Second... Finally..." crutches) in narrative prose unless presenting explicit sequential protocol steps. Cut formulaic paragraph-final summary recaps (*"In summary..."*, *"Ultimately, these findings highlight..."*) that merely restate the paragraph's premise; let the finding itself lead into the next logical step.
3. **Punctuation habits (em dashes and mechanical tics)**: Strictly limit em dashes (`—`). When em dashes appear repeatedly as parenthetical crutches or dramatic pauses, replace them with standard syntactic subordination, natural commas, parentheses for technical specifications, or clean sentence splits. Ensure punctuation clarifies logical relations rather than creating theatrical pauses.
4. **Burstiness (rhythm and sentence variation)**: Remedy low burstiness (steady, metronomic 18–24 word sentences with uniform Subject-Verb-Object openings) by deliberately varying sentence lengths and syntactic structures. Pair short, crisp assertions (6–12 words) with compound, evidence-dense sentences (25–40 words), and vary opening clauses to restore natural cadence and reading momentum.

## Two depth modes

**Conservative**: preserve paragraph order, citations, technical terms, and most sentence architecture. Remove genuine redundancy, filler and unjustified rhetoric. Default.

**Substantive**: allow paragraph reordering, material restructuring, and clearer evidence–claim sequencing. Maintain a change log for argument moves and check all cross-references. Flag rather than supply any missing facts or scientific decisions.

## Decisions under uncertainty

If source evidence is missing, preserve a conservative scientifically plausible statement and add a separate author query; do not fill in missing values or references. If a linter flags a phrase but rewriting reduces precision, reject the suggestion. If a revision screen flags numerical differences, stop and compare with the source of truth. A clean screen does not prove fidelity.
