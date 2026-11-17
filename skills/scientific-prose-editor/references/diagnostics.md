# Local diagnostics

Run from the installed skill directory with Python 3.10 or later, or use absolute script paths. These scripts use only the Python standard library and read local text files.

```bash
python scripts/lint.py draft.md --genre manuscript --section auto --output review.json
python scripts/verify_revision.py draft.md edited.md --output fidelity_review.json
```

Run the linter when a long draft benefits from triage. Inspect relevant excerpts and discard candidates with a valid scientific function. Use `--genre` and `--section` to match the material. Use the revision screen when changes to protected tokens are plausible. Both commands print JSON if you omit `--output`. For long documents, write to a file and inspect relevant findings instead of loading the entire report.

The revision screen exits 0 for a clean token screen, 2 for blocked findings, and 3 for review warnings. Open its JSON report on any of these outcomes. Resolve blocked findings against the source. Check flagged changes in negation, uncertainty, causal language, and statistical terminology. A `screen_passed` result can miss dropped steps, changed actors, and invented conditions. It never replaces a claim-by-claim comparison.
