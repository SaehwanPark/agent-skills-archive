# Independent review loop

Use this procedure only when review is required by the user, repository, or default
workflow. Follow the available code-review skill for each pass.

1. Run three independent passes over the PR diff, relevant source context, canonical task
   or spec, and test output. Keep each pass's findings separate.
2. Merge and deduplicate findings, retaining severity and evidence.
3. Fix all blocking findings. Fix or explicitly defer non-blocking findings with rationale.
4. Rerun affected tests, commit, and push fixes on the same branch.
5. Reply to actionable PR threads and resolve them when the platform supports it.
6. After a blocking fix, run at least one follow-up pass on the updated diff.
7. Repeat until no unresolved blocking findings remain.

When no PR host is available, apply the same process to the base-to-HEAD diff and document
the limitation. Do not represent a local review as a hosted PR review.

Report pass count, findings by severity, resolution or deferral, follow-up validation, and
merge-readiness. Do not claim merge-readiness while required blocking findings or failing
checks remain.
