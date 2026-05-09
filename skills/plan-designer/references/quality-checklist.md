# Plan quality checklist

Use this checklist before returning a coding plan.

## Scope

- The plan describes the smallest useful change.
- The plan avoids opportunistic cleanup.
- The plan avoids new dependencies unless required.
- The plan avoids public API changes unless required.
- The plan explicitly names non-goals.

## Operational clarity

- The likely files and functions are named.
- Unknown files are handled through a bounded discovery step.
- The first three implementation actions are obvious.
- The plan uses concrete verbs such as inspect, change, add, update, run, verify, and stop.
- The plan avoids vague verbs such as improve, enhance, robustify, rework, modernize, or clean up.

## Assumptions and uncertainty

- Assumptions are listed explicitly.
- The plan says what to do if assumptions are false.
- The plan does not hide uncertainty behind confident wording.
- The plan includes stop conditions for unexpected structure or broader scope.

## Tests and validation

- The test command is named when it can be known.
- The test cases are concrete inputs, states, or behaviors.
- Acceptance criteria are observable.
- Existing behavior that must not change is listed.
- Unrelated test failures are handled separately.

## Reviewability

- A reviewer can tell why each file changed.
- The plan checks semantic correctness, not only test passing.
- The plan guards against overfitting to fixtures.
- The plan requires reporting files changed, tests run, deviations, and unresolved risks.

## Risk

- The plan has one risk label.
- The risk reason is specific.
- High-risk plans require review before implementation.
