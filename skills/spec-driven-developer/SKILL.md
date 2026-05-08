---
name: spec-driven-developer
description: Maintain SPEC.md, ARCHITECTURE.md, and CHANGELOG.md while implementing features so project intent, current design, and release history stay accurate and verifiable.
---

# spec-driven-developer

## Purpose

Use this skill when implementing, reviewing, or planning code changes in a small to mid-sized personal project that should keep repo-level documentation aligned with development.

This workflow is intentionally lightweight and optimized for:

* solo developers
* AI-assisted development
* long-running personal projects
* reducing context drift
* preserving architectural intent
* avoiding undocumented "vibe coding"

The goal is not to replace issue trackers, kanban systems, or formal enterprise SDLC processes.

Instead, this workflow provides a persistent markdown-based memory system that keeps project state understandable to both humans and coding agents.

---

# Core Principles

## Documentation Is Operational State

The markdown files in the repository are treated as operational context for both developers and agents.

They should reflect:

* what exists
* what is actively changing
* what is planned
* why the system is structured the way it is

## Lightweight Over Bureaucratic

This workflow intentionally avoids:

* heavyweight specification frameworks
* excessive process gating
* enterprise approval chains
* over-detailed task decomposition

Prefer concise, maintainable documentation over exhaustive process.

## Minimize Context Drift

When implementation changes but documentation does not, future contributors and agents lose trust in the repo.

This workflow exists primarily to reduce:

* stale architectural assumptions
* forgotten feature intent
* undocumented behavior changes
* invisible scope creep

## Preserve Architectural Stability

Agents should not introduce architectural drift simply because a shortcut appears convenient.

Documented constraints and invariants should be preserved unless explicitly changed.

---

# Required Project Files

Manage these files at the repository root when they exist or when the project adopts this workflow:

* `SPEC.md`
* `ARCHITECTURE.md`
* `CHANGELOG.md`

Optional:

* `TASKS.md`

---

# File Responsibilities

## SPEC.md

Purpose:

* feature inventory
* active development scope
* planned project evolution
* implementation verification criteria

`SPEC.md` is NOT:

* a kanban board
* a sprint tracker
* a replacement for GitHub Issues
* a detailed implementation task breakdown

## ARCHITECTURE.md

Purpose:

* explain high-level system structure
* preserve important constraints
* help new contributors orient quickly
* reduce accidental architectural drift

## CHANGELOG.md

Purpose:

* preserve meaningful project history
* summarize user-visible or contributor-visible changes
* track important fixes and milestones

## TASKS.md (Optional)

Purpose:

* short-lived execution planning
* implementation sequencing
* temporary decomposition of active work

Use `TASKS.md` only if implementation complexity justifies it.

Avoid turning it into permanent project management overhead.

---

# SPEC.md Workflow

`SPEC.md` should contain three primary categories:

* Past
* Present
* Future

## Category Definitions

### Past

Features or work already completed and verified.

### Present

Features actively being implemented or refined.

This section should remain intentionally small.

If a feature is paused or abandoned for now, move it back to Future.

### Future

Planned or desired work not currently being implemented.

---

# Present Item Format

Each Present item should include lightweight operational metadata.

Example:

```md
- Feature: Incremental indexing
  Status: Active
  Started: 2026-05-01
  Branch: feat/incremental-indexing

  Summary:
  Add partial re-index support for modified documents.

  Verification:
  - Incremental update integration test passes
  - Re-index operation completes under 30 seconds
  - Existing full rebuild flow still works

  Out of Scope:
  - Distributed indexing
  - Realtime synchronization
```

Metadata should remain concise.

Do not turn SPEC.md into a detailed issue tracker.

---

# SPEC.md Rules

## Before Implementation

1. Read `SPEC.md`.
2. Identify whether the feature already exists in Future.
3. Move or copy relevant work into Present.
4. Add concise verification criteria.
5. Explicitly define out-of-scope work.
6. Preserve unrelated entries.

If the feature does not exist:

* create a concise Present item
* describe intended behavior
* define minimal verification criteria

## During Implementation

Keep Present entries aligned with reality.

If scope changes significantly:

* update the summary
* update verification criteria
* explicitly document deferred work

## After Implementation

1. Update Present with actual implemented behavior.
2. Run or describe verification.
3. Move completed work into Past.
4. Leave unfinished follow-up work in Present or Future.
5. Ensure SPEC.md matches:

   * implementation
   * tests
   * architecture
   * changelog entries

---

# Verification Requirements

Before moving work from Present to Past:

* define explicit verification criteria
* confirm behavior matches implementation
* run relevant tests when available
* document known limitations
* document intentionally deferred work

Verification may include:

* unit tests
* integration tests
* manual validation steps
* performance checks
* migration validation
* API compatibility checks

Agents should avoid claiming work is complete without evidence.

---

# ARCHITECTURE.md Workflow

Update `ARCHITECTURE.md` whenever changes affect:

* module structure
* control flow
* data flow
* storage
* APIs
* dependency boundaries
* operational behavior
* deployment assumptions
* concurrency assumptions

The document should help a new contributor answer:

* What are the major modules?
* What does each module own?
* How does data move through the system?
* What are the important boundaries?
* Which files are likely entry points?
* What assumptions must future work preserve?

Keep the document high-level.

Prefer:

* concise explanations
* short ordered flows
* lightweight diagrams
* architectural constraints

Avoid:

* excessive implementation details
* line-by-line code explanations
* redundant API documentation

---

# Architecture Freshness Rules

Each major section should include:

```md
Last Reviewed: YYYY-MM-DD
Status: Verified
```

Allowed status values:

* Verified
* Needs Review
* Partially Stale

If architecture accuracy is uncertain:

* mark it explicitly
* do not silently imply correctness

---

# Constraints and Invariants

`ARCHITECTURE.md` should document important constraints such as:

* forbidden dependencies
* required abstractions
* persistence guarantees
* API compatibility rules
* performance boundaries
* concurrency assumptions
* security constraints
* directory ownership boundaries

Agents should preserve these invariants unless explicitly instructed otherwise.

---

# CHANGELOG.md Workflow

`CHANGELOG.md` should follow a simplified Keep a Changelog structure.

Recommended categories:

* Added
* Changed
* Fixed
* Removed
* Deprecated
* Security

Use reverse chronological ordering.

Maintain an `Unreleased` section.

---

# CHANGELOG.md Rules

Update the changelog when completing:

* meaningful features
* user-visible behavior changes
* architectural migrations
* compatibility changes
* important fixes
* operational changes worth preserving

Avoid noisy entries for:

* trivial refactors
* formatting changes
* inconsequential internal edits

If the changelog is stale:

1. Review SPEC.md.
2. Review recent implementation changes.
3. Summarize missing completed work.
4. Prefer contributor-facing language.

---

# Concurrent Work Rules

When multiple features are active simultaneously:

* never overwrite unrelated Present items
* preserve metadata from other contributors
* prefer additive edits over restructuring
* avoid silently resolving conflicting assumptions

If inconsistencies appear between:

* implementation
* architecture
* specification

then:

1. document the inconsistency
2. leave follow-up notes
3. avoid pretending alignment exists

---

# Rollback and Partial Completion Rules

If work is partially reverted:

* move the feature back into Present
* document rollback reasons
* preserve historical changelog entries
* document remaining known issues

Do not erase project history simply because implementation direction changed.

---

# Bootstrapping Missing Files

If required files do not exist, create minimal useful versions.

## Minimal SPEC.md

```md
# SPEC

## Past
- Initial project scaffolding

## Present
- Current active work

## Future
- Planned improvements
```

## Minimal ARCHITECTURE.md

```md
# ARCHITECTURE

## Overview
Short system summary.

Last Reviewed: YYYY-MM-DD
Status: Verified

## Main Modules
- module_a: responsibility
- module_b: responsibility

## Data Flow
1. Input
2. Processing
3. Output
```

## Minimal CHANGELOG.md

```md
# CHANGELOG

## Unreleased

### Added
- Initial setup
```

---

# Final Check

Before finishing work:

* confirm SPEC.md reflects actual feature state
* confirm Present items remain accurate
* confirm verification criteria were addressed
* confirm ARCHITECTURE.md reflects structural changes
* confirm architectural constraints still hold
* confirm CHANGELOG.md includes meaningful updates
* mention documentation updates in the final response

The repository should remain understandable to a future contributor or agent with no prior session context.