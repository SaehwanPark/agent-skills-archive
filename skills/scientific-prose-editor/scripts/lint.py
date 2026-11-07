#!/usr/bin/env python3
"""Conservative scientific-prose review cues. NOT an AI detector.

Example: python scripts/lint.py draft.md --genre manuscript --section auto
"""
from __future__ import annotations
import argparse
import re

from core import (GENRES, SECTIONS, char_position, content_tokens, jaccard,
                  masked_prose, read_text, section_at, section_ranges,
                  sentence_spans, write_json)

PATTERNS = {
  "D01": ("Redundant restatement", "P0", "Adjacent sentences may reiterate rather than add information.",
          "Check whether repetition aids orientation or preserves an essential distinction."),
  "D03": ("Generic significance framing", "P1", "The claim may lack a study-specific reason for importance.",
          "General context can be appropriate in interdisciplinary introductions."),
  "D04": ("Evaluative result instead of observation", "P1", "The sentence may emphasize significance rather than reported findings.",
          "Qualitative research may report themes rather than numbers."),
  "D06": ("Promotional stance", "P1", "An evaluative claim may need a specific evidentiary basis.",
          "Grants legitimately argue for significance; do not remove justified claims."),
  "D07": ("Generic future-work sentence", "P1", "The sentence does not identify the unresolved research question.",
          "Some journal conclusions require a concise future-work statement."),
  "D08": ("Repeated contrast template", "P2", "Multiple nonessential not-X-but-Y constructions may become mechanical.",
          "Contrast is a useful and legitimate device in scientific argument."),
  "D09": ("Non-substantive metacommentary", "P2", "The clause announces rather than conveys scientific content.",
          "Long technical documents may require a clear section roadmap."),
  "D10": ("Unspecified critique of prior work", "P1", "The comparison may need specific evidence and citations.",
          "A nearby citation or established literature summary may support it."),
  "L01": ("Cluster of conventional AI-associated terms and buzzwords", "P2", "Check whether repeated ornamental or buzzword wording improves precision.",
          "These words are never authorship evidence and may be entirely appropriate in technical contexts."),
  "L02": ("Unqualified superlative", "P2", "An exceptional-impact adjective may need substantiation.",
          "A grant innovation claim can be valid when grounded in specific preliminary evidence."),
  "L03": ("Dense explicit transition sequence", "P2", "Multiple sentence-opening transitions may be unnecessary.",
          "Transitions can encode meaningful logic, particularly in technical writing."),
  "L04": ("Uniform sentence construction and low burstiness", "P2", "Consecutive sentences have uniform length and structure, creating a flat cadence.",
          "Parallelism is essential in aims, hypotheses, and methods; explicit study design and reporting conventions override stylistic diversity objectives."),
  "L06": ("Decorative general recap", "P2", "Consider ending with the concrete finding rather than generalized importance.",
          "A conclusion is appropriate when it answers the specific question."),
  "L07": ("Punctuation habit or em-dash clustering", "P2", "Repetitive em dashes across sentences may disrupt reading cadence.",
          "Paired em-dash parentheticals are standard punctuation, even in two separate sentences; recommend an edit only with stronger evidence of a repeated habit or impaired reading."),
  "L08": ("Predictable list-like flow or repetitive conclusion", "P2", "Formulaic sequential enumeration or repetitive concluding recap reduces natural flow.",
          "Explicit study design, methodological sequencing, hypothesis enumeration, and reporting conventions override stylistic diversity objectives."),
  "R04": ("Potential design–claim mismatch", "P0", "A causal-sounding claim appears alongside observational-design cues.",
          "Causal inference can justify some causal claims; requires methodological review."),
}

RULES = [
  ("D03", re.compile(r"\b(?:plays? (?:a|an) (?:crucial|vital|pivotal) role|in (?:today'?s|the current) rapidly evolving|increasingly important (?:area|field))\b", re.I), None),
  ("D04", re.compile(r"\b(?:results? (?:were|was|are|is) (?:very )?(?:promising|remarkable)|findings? (?:were|was|are|is) (?:highly )?(?:promising|exciting))\b", re.I), {"abstract", "results"}),
  ("D06", re.compile(r"\b(?:transformative|unprecedented|game[- ]changing|remarkably|groundbreaking)\b", re.I), None),
  ("D07", re.compile(r"\b(?:future research (?:is|will be) needed|further (?:research|studies) (?:is|are) (?:needed|warranted))\b", re.I), None),
  ("D09", re.compile(r"\b(?:it is important to note that|it is worth noting that|this (?:section|paper) (?:will|aims to) (?:discuss|explore))\b", re.I), None),
  ("D10", re.compile(r"\b(?:previous (?:studies|research) (?:have|has) (?:failed|largely failed) to|existing methods (?:are|have been) inadequate)\b", re.I), None),
  ("L02", re.compile(r"\b(?:revolutionary|first[- ]ever|paradigm[- ]shifting|unparalleled)\b", re.I), None),
  ("L06", re.compile(r"\b(?:these findings underscore the importance of|this work highlights the critical need for)\b", re.I), None),
]

STRUCTURAL_LABEL = re.compile(
  r"(?i)^[\s*_\-•]*(?:\d+[.)]\s*)?"
  r"(?:specific\s+aim|sub-?aim|aim|objective|hypothesis|step|phase|endpoint)\s*(?:\d+[a-z]?|[IVX]+)\b"
)


def analyze(text: str, genre: str = "manuscript", section: str = "auto") -> dict:
  if genre not in GENRES:
    raise ValueError(f"Unsupported genre: {genre}")
  if section not in SECTIONS:
    raise ValueError(f"Unsupported section: {section}")
  masked = masked_prose(text)
  fallback = "other" if section == "auto" else section
  sections = section_ranges(text, fallback)
  issues = []
  def add(pid: str, a: int, b: int, match: str):
    label, priority, rationale, exception = PATTERNS[pid]
    issues.append({"pattern_id": pid, "label": label, "priority": priority,
                   "start": a, "end": b, "position": char_position(text, a),
                   "section": section_at(sections, a), "excerpt": match.strip()[:220],
                   "rationale": rationale, "false_positive_guard": exception,
                   "decision": "manual_review_required"})

  for pid, regex, only_sections in RULES:
    for m in regex.finditer(masked):
      if only_sections and section_at(sections, m.start()) not in only_sections:
        continue
      add(pid, m.start(), m.end(), text[m.start():m.end()])

  # Paragraph analysis; no count is interpreted as a probability or AI-authorship score.
  for m in re.finditer(r"(?m)(?:^|\n\s*\n)([^\n].*?)(?=\n\s*\n|\Z)", masked, re.S):
    block = m.group(1)
    start = m.start(1)
    if not block.strip() or len(block.split()) < 20:
      continue
    sentences = sentence_spans(block, start)
    for (a1, b1, s1), (a2, b2, s2) in zip(sentences, sentences[1:]):
      tok1, tok2 = content_tokens(s1), content_tokens(s2)
      if min(len(tok1), len(tok2)) >= 6 and len(tok1 & tok2) >= 6 and jaccard(tok1, tok2) >= 0.68:
        add("D01", a2, b2, text[a2:b2])
    block_section = section_at(sections, start)
    # Exempt only blocks where labels lead sentences (aims, protocol steps), not incidental mentions.
    structural_labels = [s for _a, _b, s in sentences if STRUCTURAL_LABEL.match(s)]
    has_aims_or_steps = len(structural_labels) >= 2
    # Count at sentence starts instead of using variable-width lookbehind.
    beginnings = [(a, s) for a, _b, s in sentences if re.match(r"(?i)^(?:moreover|furthermore|additionally|in addition|notably|importantly)\s*[,;]", s.strip())]
    if len(beginnings) >= 3 and len(sentences) >= 3:
      a = beginnings[0][0]
      add("L03", a, min(a+180, start+len(block)), text[a:min(a+180, start+len(block))])
    # Check for low burstiness / uniform sentence lengths in substantive paragraphs
    if len(sentences) >= 4 and block_section not in {"methods", "aims", "approach"} and not has_aims_or_steps:
      lengths = [len(re.findall(r"\b\w+\b", s)) for _, _, s in sentences]
      mean_len = sum(lengths) / len(lengths)
      if mean_len >= 14:
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        if std_dev < 3.2:
          add("L04", sentences[0][0], sentences[-1][1], f"Uniform sentence lengths (mean={mean_len:.1f}, std={std_dev:.1f} words)")

    # Punctuation habit: clustered em dashes across sentences or multiple interruptions
    dashes = list(re.finditer(r"—|--", block))
    if len(dashes) >= 2:
      sentences_with_dashes = [s for s in sentences if re.search(r"—|--", s[2])]
      flag_l07 = False
      if len(sentences_with_dashes) >= 2:
        flag_l07 = True
      elif len(sentences_with_dashes) == 1:
        s_dashes = list(re.finditer(r"—|--", sentences_with_dashes[0][2]))
        if len(s_dashes) >= 3:
          flag_l07 = True
        elif len(s_dashes) == 2:
          d1, d2 = s_dashes[0], s_dashes[1]
          s_text = sentences_with_dashes[0][2]
          is_paired = bool(s_text[:d1.start()].strip() and s_text[d1.end():d2.start()].strip() and s_text[d2.end():].strip())
          if not is_paired:
            flag_l07 = True
      if flag_l07:
        add("L07", start + dashes[0].start(), start + dashes[-1].end(), text[start + dashes[0].start():start + dashes[-1].end()])

    # Predictability: formulaic sequential enumerations (exempting methods, aims, approach, or explicit aims/steps)
    if block_section not in {"methods", "aims", "approach"} and not has_aims_or_steps:
      enums = list(re.finditer(r"(?i)\b(?:first(?:ly)?|second(?:ly)?|third(?:ly)?|finally|lastly)\s*[,;]", block))
      if len(enums) >= 3:
        add("L08", start + enums[0].start(), start + enums[-1].end(), text[start + enums[0].start():start + enums[-1].end()])

    contrasts = list(re.finditer(r"\bnot (?:only|merely)\b.{0,120}?\bbut (?:also|rather)\b", block, re.I | re.S))
    if len(contrasts) >= 2:
      a = start + contrasts[0].start()
      add("D08", a, start + contrasts[-1].end(), text[a:start+contrasts[-1].end()])
    if re.search(r"\b(?:retrospective|observational|cross[- ]sectional|case[- ]control)\b", block, re.I):
      causal = re.search(r"\b(?:proves? that|caused|causes|resulted in|directly led to)\b", block, re.I)
      if causal:
        add("R04", start+causal.start(), start+causal.end(), causal.group(0))

  lex = list(re.finditer(r"\b(?:delve|delves|pivotal|intricate|tapestry|underscores?|multifaceted|testament|beacon|paramount|crucial nexus|foster(?:s|ed|ing)?|elevate(?:s|ed|ing)?|garner(?:s|ed|ing)?)\b", masked, re.I))
  # Require several occurrences AND more than one distinct term, not a blacklist.
  if len(lex) >= 3 and len({m.group(0).lower() for m in lex}) >= 2:
    add("L01", lex[0].start(), lex[-1].end(), ", ".join(m.group(0) for m in lex))

  issues.sort(key=lambda v: (v["start"], v["pattern_id"]))
  return {"tool": "scientific-prose-editor/lint", "version": "1.0.0",
          "genre": genre, "section": section,
          "interpretation": "Review candidates only. Not an AI detector or quality score.",
          "issue_count": len(issues), "issues": issues}


def main():
  ap = argparse.ArgumentParser(description=__doc__)
  ap.add_argument("input", help="UTF-8 text/Markdown file or '-' for stdin")
  ap.add_argument("--genre", choices=GENRES, default="manuscript")
  ap.add_argument("--section", choices=SECTIONS, default="auto")
  ap.add_argument("--output", help="Optional JSON output path")
  args = ap.parse_args()
  write_json(analyze(read_text(args.input), args.genre, args.section), args.output)


if __name__ == "__main__":
  main()
