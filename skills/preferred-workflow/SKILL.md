---
name: preferred-workflow
description: Use when continuing development, implementing a feature or fix, or refactoring in a Git repository with branch, verification, and PR handoff requirements.
---

# Preferred Workflow

1. Read repository guidance and inspect the working tree, base branch, and relevant PR or checkpoint. Resume the matching branch or create one from the prescribed base. Preserve unrelated edits.
2. Define the requested behavior and how to verify it. For fixes, reproduce the failure when practical. For refactors, identify the existing behavior callers rely on. Add a focused regression test when existing coverage misses a meaningful risk.
3. Implement the complete requested slice. Run relevant checks and update project documentation when the change affects it.
4. Follow the requested handoff order, including draft PRs or incremental pushes. Use the repository's branch and PR conventions, and act on the authorization already given.
5. Follow repository review requirements. Use the [review loop](references/review-loop.md) for requested independent reviews or changes with significant failure impact.
6. Report outcomes, verification, and any unresolved blocker. Include the PR link when applicable.
