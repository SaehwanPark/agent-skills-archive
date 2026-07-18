---
name: end-user-xp-improver
description: Use when planning, implementing, or reviewing a user-facing UI, CLI, API, onboarding, error, or documentation change that needs explicit audience, workflow, low-friction defaults, accessibility, and recovery-path decisions.
---

# End-User Experience Improver

Optimize the common user journey without inventing unsupported product requirements.

## Workflow

1. Read product documentation, existing interfaces, examples, tests, and support signals to
   identify the target users and their job to be done.
2. Map the current path from entry to success, including setup, decisions, waiting, errors,
   recovery, and repeated use.
3. Identify concrete friction supported by evidence or label it as an assumption.
4. Choose defaults that serve the common case while keeping advanced controls discoverable.
5. Preserve established workflows and compatibility unless change is intentional.
6. Verify the revised path with representative success, invalid input, empty state,
   permission failure, retry/recovery, and accessibility scenarios where applicable.

## Design rules

- Minimize setup and required decisions before first value.
- Use familiar project conventions and stable, predictable behavior.
- Make errors specific, actionable, and safe; preserve user input when recovery permits.
- Show progress, success, empty, loading, disabled, and failure states when relevant.
- Keep advanced configuration optional and progressively disclosed.
- Use clear labels, keyboard/focus behavior, contrast, and assistive semantics for UI work.
- Do not require users to understand implementation details.

Document target users or assumptions in an existing appropriate location only when the
task authorizes documentation changes or the implementation already requires that doc to
change. Do not create a new documentation system.

## Stop conditions

Stop when audience or product intent has multiple high-impact interpretations, a proposed
default changes security/privacy/data behavior, accessibility cannot be evaluated with
available context, or reducing friction would break an established contract.

## Expected output

Report the target user and task, friction addressed, defaults and recovery paths chosen,
scenarios verified, assumptions, and deliberately deferred experience improvements.
