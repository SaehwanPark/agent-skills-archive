# Minimal, scientific-context editing examples

All examples are synthetic teaching material. They're not evidence that any detector would accept or reject the wording. Parenthetical notes describe editorial quality, not authorship.

| Draft | Conservative edit | Why |
|---|---|---|
| “This groundbreaking study provides transformative insights into risk prediction.” | “This study evaluates whether the additional features improve risk prediction beyond routine variables.” | Replaces vague praise with an already established comparison; only if the draft actually evaluates that question |
| “The results were highly promising, illustrating the potential impact of the model.” | “The model improved discrimination in the validation cohort.” | Leads with a result; use **only if verified** and report the available estimate/CI when provided |
| “We used robust standard errors.” | **No change.** | “Robust” is a technical term here, not a word to ban |
| “We first estimated the hazard ratio. We then estimated the hazard ratio for the primary endpoint.” | “We estimated the hazard ratio for the primary endpoint.” | Redundancy can be removed without changing the estimand |
| “It is important to note that the association was not statistically significant.” | “The association was not statistically significant.” | Removes staging, preserves qualification |
| “The exposure caused mortality in our retrospective cohort.” | **[AUTHOR VERIFY]** “The exposure was associated with mortality…” | Requires methods/results audit; do not silently weaken a justified causal-inference claim |
| “Existing studies failed to address the problem.” | **[AUTHOR VERIFY]** Specify which design, population, outcome or measurement gap is actually supported. | Avoids invented literature criticism |
| “Specific Aim 1: Estimate prevalence. Specific Aim 2: Validate estimates.” | **No change.** | Parallel aim formatting is purposeful |
| “We implemented the algorithm using a randomized initialization.” | **No change unless the implementation specification differs.** | Exact algorithm terminology is an invariant |
| “Future research is needed.” | “External validation in other health systems remains an open question.” | Acceptable only if external validation is genuinely absent and relevant |
| “Our findings serve as a testament to the pivotal role of epigenetic regulation, fostering an intricate understanding of cellular plasticity.” | “Our findings show that epigenetic regulation contributes to cellular plasticity.” | Replaces uncharacteristic buzzwords (*testament*, *pivotal*, *fostering*, *intricate*) with clear, direct scientific statement |
| “First, we evaluated efficacy. Second, we assessed safety. Finally, we analyzed pharmacokinetics. In summary, these findings underscore the potential of the drug.” | “We evaluated efficacy, safety, and pharmacokinetics.” | Replaces rigid tripartite list-like flow and eliminates predictable, redundant paragraph-final summary without introducing unsupported study details (e.g., dosing cohorts) |
| “The intervention—which was administered twice daily—yielded significant improvements in mobility—demonstrating therapeutic promise.” | “Administered twice daily, the intervention significantly improved mobility.” | Replaces repetitive em-dash parentheticals with natural participial subordination |
| “The algorithm processed all genomic sequences. The software identified variant candidates. The pipeline filtered out low confidence calls. The team verified the remaining variants.” | “The pipeline filtered candidate variants after processing all genomic sequences, and the team verified the remaining variants.” | Resolves flat cadence by varying sentence length and structure while strictly preserving the actor (“the team”), terminology (“variants”), and unstated verification method (avoids adding “manually”) |

In actual editing, do not add unverified differences such as “beyond routine variables,” “validation cohort,” “dosing cohorts,” or “manually.” The examples show what to do **given the necessary source information**. Even when an automated screen reports `screen_passed`, claim-by-claim verification by the editor is mandatory to ensure semantic equivalence and avoid inventing details.
