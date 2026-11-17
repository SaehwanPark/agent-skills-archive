---
name: code-reviewer
description: Use when reviewing a diff, branch, or pull request for actionable correctness, security, performance, and compatibility risks.
---

# Code Reviewer

1. Establish intended behavior from the request and repository guidance. Read the diff, relevant callers, and available tests or results.
2. Trace changed behavior through representative success and failure paths. Look at boundaries affected by the change, including permissions, data, concurrency, cleanup, and compatibility.
3. Check each candidate against surrounding safeguards. Report issues introduced or exposed by the diff with a concrete trigger, impact, and smallest practical correction.

Return findings first, ordered by severity with precise file locations. Use Critical or High for demonstrated severe impact or a credible path to it. If there are no actionable findings, say so. Mention material gaps in review or verification.
