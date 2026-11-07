#!/usr/bin/env python3
"""Screen edited scientific prose for changed protected facts; requires human review.

Exit 0: no detected differences. Exit 2: blocked/high-risk changes.
Exit 3: review warnings only. This is NOT semantic equivalence verification.
"""
from __future__ import annotations
import argparse
from collections import Counter
import re

from core import read_text, write_json

NUMBER = re.compile(r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?%?(?![\w.])")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s,;<>]+", re.I)
PMID = re.compile(r"\b(?:PMID|NCT|ISRCTN)\s*[:#-]?\s*[A-Z0-9-]{4,}\b", re.I)
CITATION = re.compile(r"\[(?:\d+(?:\s*[,;–-]\s*\d+)*)\]")
MODAL = re.compile(r"\b(?:may|might|could|possibly|potentially)\b", re.I)
NEGATION = re.compile(r"\b(?:not|no|none|never|without|neither|nor)\b", re.I)
CAUSAL = re.compile(r"\b(?:caus(?:e|ed|es|ing)|proves?|guarantees?|resulted in|directly led to)\b", re.I)
METHOD_TERMS = ["randomized", "retrospective", "prospective", "observational", "propensity score",
                "cox proportional hazards", "logistic regression", "instrumental variable",
                "confidence interval", "credible interval", "hazard ratio", "odds ratio",
                "risk ratio", "sensitivity analysis", "intent-to-treat", "intention-to-treat"]


def tokens(pattern: re.Pattern, text: str) -> Counter:
  return Counter(m.group(0) for m in pattern.finditer(text))


def delta(a: Counter, b: Counter) -> dict:
  return {"removed": dict(sorted((a-b).items())), "added": dict(sorted((b-a).items()))}


def verify(original: str, edited: str) -> dict:
  findings = []
  def record(check: str, level: str, message: str, detail: dict):
    findings.append({"check": check, "level": level, "message": message, **detail})

  for name, pattern in [("numerical_tokens", NUMBER), ("doi_identifiers", DOI),
                        ("trial_and_record_identifiers", PMID), ("numeric_citations", CITATION)]:
    changes = delta(tokens(pattern, original), tokens(pattern, edited))
    if changes["removed"] or changes["added"]:
      record(name, "block", "Protected tokens changed; resolve against sources before release.", changes)

  # Statistical terms and modal strength are review cues, not sufficient proof of meaning change.
  for name, pattern in [("negation", NEGATION), ("uncertainty_modal", MODAL), ("causal_language", CAUSAL)]:
    changes = delta(tokens(pattern, original.lower()), tokens(pattern, edited.lower()))
    if changes["removed"] or changes["added"]:
      record(name, "review", "Potential change in scope, negation, certainty, or causal implication.", changes)

  old, new = original.lower(), edited.lower()
  missing = [term for term in METHOD_TERMS if term in old and term not in new]
  new_terms = [term for term in METHOD_TERMS if term not in old and term in new]
  if missing or new_terms:
    record("method_terms", "review", "Methodological terminology changed; verify technical equivalence.",
           {"removed": missing, "added": new_terms})

  # Preserve literal code/math fences; editing inside these must be separately authorized.
  fenced = re.compile(r"(?ms)^\s*(```|~~~)[^\n]*\n.*?^\s*\1\s*$")
  changes = delta(tokens(fenced, original), tokens(fenced, edited))
  if changes["removed"] or changes["added"]:
    record("fenced_content", "block", "Code or fenced technical content changed.",
           {"removed_count": sum(changes["removed"].values()),
            "added_count": sum(changes["added"].values())})

  status = "blocked" if any(x["level"] == "block" for x in findings) else (
    "needs_manual_review" if findings else "screen_passed")
  return {"tool": "scientific-prose-editor/verify_revision", "version": "1.0.0",
          "status": status, "findings": findings,
          "limitations": [
            "A clean screen is NOT proof of semantic fidelity; reading against original scientific sources is mandatory.",
            "Formatting, numeric paraphrases, narrative fact edits, citation systems, negation scope and cross-section inconsistencies require human review.",
            "Token-based comparison may flag harmless changes or miss harmful changes."
          ]}


def main():
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("original", help="Original UTF-8 file")
  ap.add_argument("edited", help="Edited UTF-8 file")
  ap.add_argument("--output", help="Optional JSON output file")
  args = ap.parse_args()
  r = verify(read_text(args.original), read_text(args.edited))
  write_json(r, args.output)
  raise SystemExit({"screen_passed": 0, "blocked": 2, "needs_manual_review": 3}[r["status"]])


if __name__ == "__main__":
  main()
