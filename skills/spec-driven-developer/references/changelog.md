# Changelog workflow

Use the repository's existing format. When creating a lightweight changelog, prefer an
`Unreleased` section and familiar categories such as Added, Changed, Fixed, Removed,
Deprecated, and Security.

Record meaningful features, user-visible behavior, compatibility changes, architectural
migrations, important fixes, and operational changes worth preserving. Skip formatting,
trivial refactors, and inconsequential internal edits.

Write entries in user- or contributor-facing language. Keep reverse chronological order
when the project follows that convention.

If the changelog is stale:

1. Compare it with the specification, implementation, tests, and recent relevant history.
2. Add only changes supported by evidence.
3. State uncertainty rather than reconstructing unsupported history.

Do not erase accurate historical entries after a rollback. Add a later entry that explains
the rollback when it is itself meaningful.
