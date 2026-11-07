#!/usr/bin/env python3
"""Summarize genuine blinded-review data; no synthetic ratings are treated as evidence.

Accepts the analyst key created by prepare_eval and reviewer CSVs. Cluster
bootstrap CIs use source family as the resampling unit (descriptive only).
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import random
import statistics

from core import write_json

FIELDS = ["quality", "naturalness", "fidelity"]


def load_ratings(paths: list[str]) -> list[dict]:
  rows = []
  for path in paths:
    with open(path, newline="", encoding="utf-8") as f:
      for row in csv.DictReader(f):
        if row.get("preferred", "").strip():
          rows.append(row)
  return rows


def cluster_ci(values: list[tuple[str, float]], iterations: int = 2500, seed: int = 37) -> dict:
  fam = defaultdict(list)
  for source_family, value in values:
    fam[source_family].append(value)
  means = [statistics.mean(v) for k, v in sorted(fam.items())]
  if len(means) < 3:
    return {"mean": statistics.mean(means) if means else None,
            "ci_95": None, "note": "<3 source families; interval withheld"}
  rng = random.Random(seed)
  results = sorted(statistics.mean(rng.choices(means, k=len(means))) for _ in range(iterations))
  return {"mean": statistics.mean(means),
          "ci_95": [results[int(0.025*iterations)], results[int(0.975*iterations)-1]],
          "unit": "equal-weight source-family means; cluster bootstrap"}


def score(key: dict, rows: list[dict], require_complete: bool = False) -> dict:
  pair_key = key["pairs"]
  expected = {(rev, pair) for rev in key["reviewers"] for pair in pair_key}
  received = set()
  records = []
  for row in rows:
    reviewer = row.get("reviewer_id", "")
    pair = row.get("pair_id", "")
    ident = (reviewer, pair)
    if ident not in expected:
      raise ValueError(f"Unknown reviewer/pair: {ident}")
    if ident in received:
      raise ValueError(f"Duplicate reviewer/pair: {ident}")
    received.add(ident)
    preference = row["preferred"].strip().upper()
    if preference not in ("A", "B", "TIE"):
      raise ValueError(f"Invalid preference for {ident}: {preference!r}")
    values = {}
    for field in FIELDS:
      for side in ("A", "B"):
        raw = row.get(f"{field}_{side}", "").strip()
        try:
          v = int(raw)
        except (TypeError, ValueError):
          raise ValueError(f"Missing/invalid {field}_{side} in {ident}")
        if v not in (1, 2, 3, 4, 5):
          raise ValueError(f"{field}_{side} out of range in {ident}")
        values[f"{field}_{side}"] = v
    edited = pair_key[pair]["edited_side"]
    source_family = pair_key[pair]["source_family"]
    records.append({"reviewer_id": reviewer, "pair_id": pair, "source_family": source_family,
                    "genre": pair_key[pair]["genre"], "section": pair_key[pair]["section"],
                    "edited_wins": 1 if preference == edited else (0.5 if preference == "TIE" else 0),
                    "prefers_edited": preference == edited,
                    "tie": preference == "TIE",
                    "deltas": {field: values[f"{field}_{edited}"] - values[f"{field}_{'B' if edited == 'A' else 'A'}"]
                               for field in FIELDS},
                    "edited_fidelity": values[f"fidelity_{edited}"]})
  if require_complete and received != expected:
    raise ValueError(f"Incomplete ratings: {len(received)}/{len(expected)}")
  win = Counter("edited" if r["prefers_edited"] else ("tie" if r["tie"] else "original") for r in records)
  scores = {field: cluster_ci([(r["source_family"], r["deltas"][field]) for r in records]) for field in FIELDS}
  estimates = {"preferences": {k: win[k] for k in ("edited", "original", "tie")},
               "quality_delta": scores["quality"], "naturalness_delta": scores["naturalness"],
               "fidelity_delta": scores["fidelity"],
               "fidelity_concerns": sum(r["edited_fidelity"] <= 2 for r in records)}
  by_genre = {}
  for genre in sorted({r["genre"] for r in records}):
    subset = [r for r in records if r["genre"] == genre]
    by_genre[genre] = {"ratings": len(subset),
                       "edited_preferred": sum(r["prefers_edited"] for r in subset),
                       "ties": sum(r["tie"] for r in subset),
                       "quality_delta_mean": statistics.mean(r["deltas"]["quality"] for r in subset)}
  return {"tool": "scientific-prose-editor/score_eval", "status": "descriptive_only",
          "coverage": {"ratings_received": len(received), "ratings_expected": len(expected),
                       "distinct_pairs": len({r["pair_id"] for r in records}),
                       "distinct_source_families": len({r["source_family"] for r in records}),
                       "reviewers": len({r["reviewer_id"] for r in records}),
                       "is_complete": received == expected},
          "estimates": estimates, "by_genre": by_genre,
          "interpretation_limits": [
            "Preference is not provenance detection and cannot verify AI authorship.",
            "Small panels and dependent ratings limit generalization; intervals are descriptive.",
            "Provenance, rights, reviewer independence and randomization must be verified outside this script.",
            "No detector calls or invented reviewer ratings are made by this software."]}


def main():
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("--key", required=True, help="PRIVATE_ANALYST/assignment_key.json")
  ap.add_argument("--ratings", required=True, nargs="+", help="One or more reviewer CSVs")
  ap.add_argument("--require-complete", action="store_true")
  ap.add_argument("--output", help="JSON report path")
  args = ap.parse_args()
  try:
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))
    results = score(key, load_ratings(args.ratings), args.require_complete)
  except (KeyError, ValueError, OSError, json.JSONDecodeError) as exc:
    ap.error(str(exc))
  write_json(results, args.output)


if __name__ == "__main__":
  main()
