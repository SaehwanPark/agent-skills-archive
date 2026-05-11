# Review protocol for agents

When reviewing or modifying code:

1. Identify the pure core and impure edge.
2. Check whether state is explicit.
3. Check whether errors and absence are typed.
4. Check whether tests describe behavior.
5. Add or update unit tests as contracts before implementing new core behavior or refactoring internals.
6. Refactor toward small pure functions.
7. Keep adapters thin.
8. Run relevant unit tests, then type checks and broader tests where configured.
9. Report remaining violations clearly.

When proposing changes, prefer small diffs that improve one of:

- Explicit state.
- Purity.
- Type contracts.
- Error modeling.
- Testability.
- Portability.

Do not introduce clever abstractions unless they reduce hidden context.
