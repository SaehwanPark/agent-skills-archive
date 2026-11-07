#!/usr/bin/env python3
"""Prepare blinded A/B preference packets from rights-cleared scientific text pairs.

Produces public reviewer packets and analyst-only key. Never uploads data.
Only use documented rights-cleared text; the script cannot authenticate legal permissions.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import random
import re

from core import GENRES, validate_jsonl, write_json


def prepare(rows: list[dict], reviewers: list[str], seed: int = 37,
            allow_family_repeats: bool = False) -> tuple[dict, dict]:
  if not reviewers or len(set(reviewers)) != len(reviewers):
    raise ValueError("Supply unique, nonempty reviewer IDs")
  if not all(re.fullmatch(r"[A-Za-z0-9_-]{1,32}", x) for x in reviewers):
    raise ValueError("Reviewer IDs must be 1-32 alphanumeric characters, hyphens or underscores")
  if not rows:
    raise ValueError("No input passages")
  ids, text_hashes, family_ids, original_hashes = set(), set(), set(), set()
  for row in rows:
    for key in ("item_id", "source_family", "original", "edited", "genre", "section", "fact_sheet", "rights_status", "provenance_documented"):
      if key not in row:
        raise ValueError(f"Missing {key} in {row.get('item_id', '?')}")
    if row["item_id"] in ids:
      raise ValueError("Duplicate item_id")
    ids.add(row["item_id"])
    family = str(row["source_family"])
    if not family.strip():
      raise ValueError("Missing source_family identifier")
    if family in family_ids and not allow_family_repeats:
      raise ValueError("Repeated source_family: use independent families or explicitly --allow-family-repeats")
    family_ids.add(family)
    if not isinstance(row["fact_sheet"], str) or not row["fact_sheet"].strip():
      raise ValueError("A neutral, verified fact_sheet is required for fidelity judgments")
    if row["genre"] not in GENRES:
      raise ValueError("Unsupported genre")
    if row["rights_status"] != "approved" or row["provenance_documented"] is not True:
      raise ValueError(f"{row['item_id']}: rights or provenance not approved")
    if not row["original"].strip() or not row["edited"].strip():
      raise ValueError("Blank passage")
    if row["original"] == row["edited"]:
      raise ValueError("Original and edited passages are identical")
    h = hashlib.sha256((row["original"] + "\x00" + row["edited"]).encode()).hexdigest()
    if h in text_hashes:
      raise ValueError("Repeated passage pair")
    text_hashes.add(h)
    original_hash = hashlib.sha256(row["original"].encode()).hexdigest()
    if original_hash in original_hashes:
      raise ValueError("Repeated original text across passage pairs")
    original_hashes.add(original_hash)
  rng = random.Random(seed)
  key = {"version": "1.0", "seed": seed, "study": "blinded_paired_preference",
         "pairs": {}, "reviewers": reviewers}
  packets = {r: [] for r in reviewers}
  for row in sorted(rows, key=lambda x: x["item_id"]):
    item_id = str(row["item_id"])
    # Nonsemantic, opaque ID. Human annotation must not expose source identifiers.
    pair_id = "P" + hashlib.sha256((str(seed) + ":" + item_id).encode()).hexdigest()[:12]
    edited_side = rng.choice(("A", "B"))
    key["pairs"][pair_id] = {"item_id": item_id, "source_family": row["source_family"],
                              "edited_side": edited_side, "genre": row["genre"],
                              "section": row["section"]}
    sample = {"pair_id": pair_id, "genre": row["genre"], "section": row["section"],
              "fact_sheet": row["fact_sheet"],
              "text_A": row["edited"] if edited_side == "A" else row["original"],
              "text_B": row["original"] if edited_side == "A" else row["edited"],
              "instructions": "Compare clarity, naturalness, scientific precision and fidelity. Do not infer authorship from presentation."}
    for reviewer in reviewers:
      packets[reviewer].append(sample)
  for reviewer in reviewers:
    rng.shuffle(packets[reviewer])
  return packets, key


def emit(packets: dict, key: dict, out: Path):
  if out.exists() and any(out.iterdir()):
    raise ValueError("Output directory must be empty; do not overwrite existing assignments")
  (out / "REVIEWERS").mkdir(parents=True, exist_ok=True)
  (out / "PRIVATE_ANALYST").mkdir(parents=True, exist_ok=True)
  for reviewer, samples in packets.items():
    folder = out / "REVIEWERS" / reviewer
    folder.mkdir()
    with (folder / "pairs.jsonl").open("w", encoding="utf-8") as f:
      for obj in samples:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    with (folder / "ratings.csv").open("w", encoding="utf-8", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(["reviewer_id", "pair_id", "preferred", "quality_A", "quality_B",
                       "naturalness_A", "naturalness_B", "fidelity_A", "fidelity_B", "comment"])
      for obj in samples:
        writer.writerow([reviewer, obj["pair_id"], "", "", "", "", "", "", "", ""])
  write_json(key, str(out / "PRIVATE_ANALYST" / "assignment_key.json"))


def main():
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("manifest", help="JSONL: item_id/source_family/original/edited/genre/section/fact_sheet/rights_status/provenance_documented")
  ap.add_argument("--reviewers", default="R1,R2,R3", help="Comma-delimited reviewer identifiers")
  ap.add_argument("--seed", type=int, default=37)
  ap.add_argument("--allow-family-repeats", action="store_true", help="Allow correlated source-family pairs; report dependence in analysis")
  ap.add_argument("--out", required=True, help="A NEW / empty output directory")
  args = ap.parse_args()
  try:
    packets, key = prepare(validate_jsonl(args.manifest), args.reviewers.split(","), args.seed, args.allow_family_repeats)
    emit(packets, key, Path(args.out))
  except (ValueError, OSError) as exc:
    ap.error(str(exc))


if __name__ == "__main__":
  main()
