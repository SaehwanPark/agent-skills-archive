"""Shared, dependency-free helpers for the scientific prose editor.

These tools are editorial diagnostics, not an AI authorship classifier.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys

GENRES = ("manuscript", "grant", "proposal", "technical")
SECTIONS = ("auto", "abstract", "introduction", "methods", "results", "discussion",
            "conclusion", "significance", "innovation", "approach", "aims", "technical", "other")

# A modest list: used only for candidate duplicate detection, never for authorship attribution.
STOPWORDS = frozenset("the a an and or of for from to in on at by with which that these those we our their are is was were be been as it this study results research data among into than using used between compared across can may could show shows showed".split())


def read_text(path: str) -> str:
  if path == "-":
    return sys.stdin.read()
  return Path(path).read_text(encoding="utf-8")


def write_json(value: object, path: str | None = None) -> None:
  s = json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
  if path:
    Path(path).write_text(s, encoding="utf-8")
  else:
    print(s, end="")


def char_position(text: str, offset: int) -> dict:
  return {"line": text.count("\n", 0, offset) + 1,
          "column": offset - (text.rfind("\n", 0, offset) + 1) + 1}


def protected_spans(text: str) -> list[tuple[int, int]]:
  """Identify likely code, math, YAML frontmatter and reference-list sections.

  This is intentionally conservative. It is not a complete Markdown/LaTeX parser.
  """
  ranges = []
  for pattern in [
    r"(?ms)\A---\s*\n.*?\n---\s*(?=\n|\Z)",
    r"(?ms)^\s*(```|~~~)[^\n]*\n.*?^\s*\1\s*$",
    r"(?s)\$\$.*?\$\$",
    r"(?s)\\\[.*?\\\]",
    r"(?<!\$)\$(?!\$)[^\n$]+?\$(?!\$)",
    r"(?s)\\\(.*?\\\)",
    r"`[^`\n]+`",
    r"https?://[^\s<>]+",
  ]:
    ranges.extend((m.start(), m.end()) for m in re.finditer(pattern, text))
  ref_header = re.search(r"(?im)^\s*#{1,6}\s*(?:references|bibliography)\s*$", text)
  if ref_header:
    ranges.append((ref_header.start(), len(text)))
  return ranges


def masked_prose(text: str) -> str:
  out = list(text)
  for a, b in protected_spans(text):
    for i in range(a, b):
      if out[i] != "\n":
        out[i] = " "
  # Mask Markdown headings, which function as navigation rather than prose.
  for m in re.finditer(r"(?m)^\s{0,3}#{1,6}\s+[^\n]+", text):
    for i in range(m.start(), m.end()):
      if out[i] != "\n":
        out[i] = " "
  return "".join(out)


def section_ranges(text: str, fallback: str = "other") -> list[tuple[int, int, str]]:
  header_pattern = re.compile(r"(?im)^\s{0,3}#{1,6}\s+([^\n]+)")
  matches = list(header_pattern.finditer(text))
  if not matches:
    return [(0, len(text), fallback)]
  out = [(0, matches[0].start(), fallback)]
  for i, m in enumerate(matches):
    h = m.group(1).lower()
    aliases = [
      ("abstract", ["abstract", "summary"]),
      ("introduction", ["introduction", "background"]),
      ("methods", ["method", "design", "statistical analysis"]),
      ("results", ["result", "finding"]),
      ("discussion", ["discussion", "interpretation"]),
      ("conclusion", ["conclusion", "implication"]),
      ("significance", ["significance"]),
      ("innovation", ["innovation"]),
      ("approach", ["approach"]),
      ("aims", ["specific aim", "objectives"]),
    ]
    section = next((k for k, words in aliases if any(w in h for w in words)), fallback)
    out.append((m.end(), matches[i+1].start() if i+1 < len(matches) else len(text), section))
  return out


def section_at(ranges: list[tuple[int, int, str]], offset: int) -> str:
  for a, b, label in ranges:
    if a <= offset < b:
      return label
  return "other"


def sentence_spans(text: str, start: int = 0) -> list[tuple[int, int, str]]:
  # Lightweight segmentation; abbreviation and decimal edge cases remain possible.
  ends = list(re.finditer(r"(?<=[.!?])\s+(?=[A-Z(\"'])|\n{2,}", text))
  spans = []
  cursor = 0
  for m in ends:
    part = text[cursor:m.start()]
    if part.strip():
      a = cursor + (len(part) - len(part.lstrip()))
      spans.append((start+a, start + m.start(), text[a:m.start()]))
    cursor = m.end()
  part = text[cursor:]
  if part.strip():
    a = cursor + (len(part) - len(part.lstrip()))
    spans.append((start+a, start + len(text), text[a:]))
  return spans


def content_tokens(text: str) -> set[str]:
  return {x for x in re.findall(r"[a-z]+", text.lower()) if len(x) > 2 and x not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
  return len(a & b) / len(a | b) if a or b else 0.0


def validate_jsonl(path: str) -> list[dict]:
  rows = []
  ids = set()
  for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
      continue
    try:
      obj = json.loads(line)
    except json.JSONDecodeError as exc:
      raise ValueError(f"{path}:{n}: invalid JSON: {exc}") from exc
    if not isinstance(obj, dict):
      raise ValueError(f"{path}:{n}: expected a JSON object")
    if obj.get("item_id") in ids:
      raise ValueError(f"{path}:{n}: duplicate item_id {obj.get('item_id')!r}")
    ids.add(obj.get("item_id"))
    rows.append(obj)
  return rows
