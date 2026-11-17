---
name: spec-driven-developer
description: Use when changing a project that tracks intended behavior, architecture, and meaningful history in SPEC.md, ARCHITECTURE.md, CHANGELOG.md, or equivalents.
---

# Spec-Driven Developer

Read the relevant project documents and update only those affected, following repository conventions.

- **Specification** — Capture changed intent and observable acceptance criteria in the existing active section. Mark work complete when evidence supports it. Keep deferred or rolled-back scope visible.
- **Architecture** — Update changed component ownership, interfaces, data flow, dependencies, and consequential invariants. Verify against the implementation.
- **Changelog** — Record meaningful user or contributor impact in the project's format. Preserve accurate historical entries and unrelated work.

Surface material disagreements between intended and actual behavior. Reconcile the affected docs with the final diff and verification. Use [starter templates](assets/project-doc-templates.md) when asked to adopt the workflow.
