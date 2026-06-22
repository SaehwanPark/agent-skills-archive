# Simplicity checklist

Use this checklist as a pause, not as a reason to expand a small task.

## Before editing

- Is the requested behavior and scope observable and unambiguous?
- Can the requirement be eliminated, deferred, configured, or enforced at an existing
  boundary without changing agreed behavior?
- What public behavior, interfaces, data, and failure semantics must remain stable?
- What do existing tests and nearby code establish as the local convention?
- Does the standard library, platform, framework, or a domain-appropriate existing
  dependency already solve the problem?

## While implementing

- Is this the smallest coherent diff rather than merely the shortest code?
- Is control flow, state, mutation, ownership, error handling, and data movement obvious?
- Does each new helper, type, layer, option, or dependency solve a present problem?
- Can an existing sound pattern be reused without creating a competing abstraction?
- Are performance choices tied to an explicit constraint or evidence?
- Are comments limited to rationale, invariants, safety, and non-obvious constraints?

## For refactors

- Is behavior protected by contract or characterization tests?
- Is the change local, or has it become a redesign that needs separate approval?
- Does removed duplication represent one stable concept rather than accidental similarity?
- Does the result reduce cognitive load without hiding important effects or failure paths?

## Before finishing

- Does the implementation satisfy only the behavior required now?
- Are changed behavior and uncovered important contracts tested proportionally?
- Did the relevant focused checks pass?
- Did the diff avoid speculative extensibility, unrelated cleanup, and broad formatting?
- Are deviations, failures, and residual risks reported clearly?
