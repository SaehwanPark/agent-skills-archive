# Public Repository Release Workflow

Use this reference for repository cleanup, public documentation, and private-to-public
repo generation. Pair it with the relevant package ecosystem reference.

## Release Surface

Define what belongs in the public repo and what remains development-only. Prefer a
single source of truth such as `deployment/release.yaml` that describes:

- files and directories to include
- files and directories to exclude
- public documentation replacements
- generated artifacts
- rename rules
- package build rules
- public repository name and local output directory defaults
- validation commands

The curation spec should completely explain how the public repository is derived from
the development repository.

## Legacy Isolation

Move deprecated, experimental, superseded, or historical code into a documented legacy
area such as `legacy/` only when doing so is within scope and safe for imports/tests.

Document:

- why the code is legacy
- whether it remains supported
- when contributors or agents should consult it
- that routine development should ignore it

Update contributor and agent-facing docs such as `README.md`, `AGENTS.md`, or existing
developer docs so legacy code is out of scope except for comparative analysis,
historical behavior, migration work, or regression investigation.

## Public Documentation

Create or update public-specific documentation under a dedicated development-repo
directory such as `deployment/public_docs/`.

Typical public docs include:

- `README.md`
- installation guide
- quickstart
- user manual or API reference when applicable
- contributing guide
- release notes template

Keep public docs friendly to the expected end user. Document exactly which public docs
replace or supplement development docs during publication.

## Public Repository Publishing

Create a project-local script, usually under `deployment/`, that:

- derives the public repo name by removing `-dev` or `_dev` when applicable
- creates or updates a local public repo checkout
- applies the curation spec idempotently
- copies, replaces, renames, and excludes files exactly as configured
- builds required public/package artifacts before sync when the project requires it
- initializes Git when needed
- creates the GitHub repo with `gh` only after approval and only if missing
- commits and pushes only after approval
- validates that public repo contents match the curation spec
- logs actions clearly and fails fast when required tools or config are missing

Prefer structured file operations and explicit validation over ad hoc shell globbing.
The script must be safe to run repeatedly for initial publication and later updates.

## Validation and Handoff

Before finalizing, run the narrowest useful validation:

- existing test suite
- package build command from the ecosystem reference
- public repo generation in dry-run or local-only mode
- curation-spec verification
- documentation replacement checks

Summarize:

- legacy moves and documentation updates
- canonical version and package metadata changes
- public docs created
- curation spec location
- scripts added and how to run them
- validations run and results
- approval-gated steps still pending
