from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "scientific-prose-editor"
SCRIPTS_DIR = SKILL_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
  sys.path.insert(0, str(SCRIPTS_DIR))

from lint import analyze  # noqa: E402
from verify_revision import verify  # noqa: E402


class ScientificProseEditorBehavioralTests(unittest.TestCase):
  """Behavioral regression tests for scientific-prose-editor linting and verification."""

  def test_l07_paired_em_dashes_not_flagged(self) -> None:
    """Grammatically valid paired em dashes forming a single parenthetical must not trigger L07."""
    text = (
      "The primary endpoint—the outcome specified before enrollment—was assessed at 30 days "
      "across all clinical trial sites in the multicenter study."
    )
    res = analyze(text)
    l07_issues = [i for i in res["issues"] if i["pattern_id"] == "L07"]
    self.assertEqual(l07_issues, [], "A single paired em-dash parenthetical should not trigger L07")

  def test_l07_clustered_em_dashes_across_sentences_flagged(self) -> None:
    """Em dashes appearing across multiple distinct sentences indicate a repetitive habit."""
    text = (
      "The primary endpoint—the outcome specified before enrollment—was assessed at 30 days. "
      "The secondary endpoint—overall survival at one year—was also evaluated across all study participants."
    )
    res = analyze(text)
    l07_issues = [i for i in res["issues"] if i["pattern_id"] == "L07"]
    self.assertEqual(len(l07_issues), 1)

  def test_l07_multiple_interruptions_single_sentence_flagged(self) -> None:
    """Three or more em dashes in a single sentence indicate stacked rhetorical pauses."""
    text = (
      "The experimental intervention—which was administered twice daily—yielded significant improvements "
      "in mobility—demonstrating therapeutic promise across the evaluated patient population in this clinical trial."
    )
    res = analyze(text)
    l07_issues = [i for i in res["issues"] if i["pattern_id"] == "L07"]
    self.assertEqual(len(l07_issues), 1)

  def test_l08_specific_aims_convention_exempt(self) -> None:
    """Specific Aims enumeration and parallel structure must not be flagged by L08 or L04."""
    text = (
      "## Specific Aims\n\n"
      "Aim 1 will establish feasibility and assess protocol adherence across cohorts. "
      "Aim 2 will evaluate clinical effectiveness using prespecified comparative metrics. "
      "Aim 3 will assess implementation fidelity throughout the target community clinics. "
      "Aim 4 will determine long-term sustainability across all participating health systems."
    )
    res = analyze(text, genre="grant", section="aims")
    flagged = [i["pattern_id"] for i in res["issues"] if i["pattern_id"] in ("L04", "L08")]
    self.assertEqual(flagged, [], "Specific Aims conventions must override stylistic diversity rules")

  def test_l08_methods_sequential_steps_exempt(self) -> None:
    """Sequential protocol descriptions in Methods must not be flagged by L08."""
    text = (
      "## Methods\n\n"
      "First, cell cultures were lysed in chilled buffer. "
      "Second, total protein concentration was quantified by bicinchoninic acid assay. "
      "Finally, equivalent protein aliquots were resolved by sodium dodecyl sulfate-polyacrylamide gel electrophoresis."
    )
    res = analyze(text, genre="manuscript", section="methods")
    l08_issues = [i for i in res["issues"] if i["pattern_id"] == "L08"]
    self.assertEqual(l08_issues, [], "Methods protocol steps should not be flagged as formulaic list flow")

  def test_l08_narrative_formulaic_enumeration_flagged(self) -> None:
    """Formulaic 'First... Second... Finally...' list flow in narrative prose should be flagged."""
    text = (
      "## Discussion\n\n"
      "First, we evaluated efficacy. Second, we assessed safety. Finally, we analyzed pharmacokinetics. "
      "In summary, these findings underscore the potential of the drug in clinical practice."
    )
    res = analyze(text, genre="manuscript", section="discussion")
    l08_issues = [i for i in res["issues"] if i["pattern_id"] == "L08"]
    self.assertEqual(len(l08_issues), 1)

  def test_l04_burstiness_narrative_uniformity_flagged_as_advisory(self) -> None:
    """Consecutive sentences of identical length in narrative prose are flagged for cadence review."""
    # 4 sentences, each 16 words, std dev 0.0
    text = (
      "## Discussion\n\n"
      "The initial findings demonstrated clear improvements across each prespecified secondary outcome in the entire cohort. "
      "The subsequent analyses revealed similar patterns across every evaluated subgroup during the complete observation timeline. "
      "The biological mechanisms underlying these observations remain consistent with previously reported translational laboratory studies. "
      "The overall evidence supports further clinical investigation within carefully monitored randomized multicenter collaborative trials."
    )
    res = analyze(text, genre="manuscript", section="discussion")
    l04_issues = [i for i in res["issues"] if i["pattern_id"] == "L04"]
    self.assertEqual(len(l04_issues), 1)
    self.assertEqual(l04_issues[0]["priority"], "P2")

  def test_negative_regression_example_a_token_screen_blindness(self) -> None:
    """Negative regression test: token screen passes despite introduced semantic errors.

    Example A demonstrates that verify_revision.py returns screen_passed even when
    the edit changes the actor ('The team' -> 'We'), adds an unstated method ('manually'),
    and alters terminology ('variants' -> 'calls'). This proves why mandatory claim-by-claim
    verification by the editor is required.
    """
    orig = (
      "The algorithm processed all genomic sequences. The software identified variant candidates. "
      "The pipeline filtered out low confidence calls. The team verified the remaining variants."
    )
    flawed_edit = (
      "The pipeline filtered candidate variants after processing all genomic sequences. "
      "We manually verified the remaining calls."
    )
    result = verify(orig, flawed_edit)
    # The token screen passes (exit code 0), showing screen blindness to semantic changes
    self.assertEqual(result["status"], "screen_passed")
    self.assertEqual(result["findings"], [])

  def test_negative_regression_example_b_token_screen_blindness(self) -> None:
    """Negative regression test: token screen passes despite invented study details.

    Example B demonstrates that verify_revision.py returns screen_passed even when
    the edit introduces unestablished facts ('across dosing cohorts'). This proves why
    automated screening alone cannot establish semantic fidelity.
    """
    orig = (
      "First, we evaluated efficacy. Second, we assessed safety. Finally, we analyzed pharmacokinetics. "
      "In summary, these findings underscore the potential of the drug."
    )
    flawed_edit = (
      "We evaluated efficacy and safety, and characterized pharmacokinetics across dosing cohorts."
    )
    result = verify(orig, flawed_edit)
    self.assertEqual(result["status"], "screen_passed")
    self.assertEqual(result["findings"], [])

  def test_corrected_examples_pass_token_screen(self) -> None:
    """Corrected examples preserve meaning and also pass token screening."""
    orig_a = (
      "The algorithm processed all genomic sequences. The software identified variant candidates. "
      "The pipeline filtered out low confidence calls. The team verified the remaining variants."
    )
    corrected_a = (
      "The pipeline filtered candidate variants after processing all genomic sequences, "
      "and the team verified the remaining variants."
    )
    res_a = verify(orig_a, corrected_a)
    self.assertEqual(res_a["status"], "screen_passed")

    orig_b = (
      "First, we evaluated efficacy. Second, we assessed safety. Finally, we analyzed pharmacokinetics. "
      "In summary, these findings underscore the potential of the drug."
    )
    corrected_b = "We evaluated efficacy, safety, and pharmacokinetics."
    res_b = verify(orig_b, corrected_b)
    self.assertEqual(res_b["status"], "screen_passed")

  def test_pattern_catalog_metadata_and_consistency(self) -> None:
    """Pattern catalog must be incremented to 0.2.0 and document 26 patterns matching taxonomy."""
    catalog_path = SKILL_ROOT / "references" / "pattern_catalog.json"
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    self.assertEqual(data["version"], "0.2.0")
    self.assertIn("changelog", data)
    self.assertEqual(len(data["patterns"]), 26)

    pattern_map = {p["id"]: p for p in data["patterns"]}
    self.assertIn("L07", pattern_map)
    self.assertIn("L08", pattern_map)
    self.assertEqual(pattern_map["L04"]["evidence_level"], "research_informed_hypothesis")


if __name__ == "__main__":
  unittest.main()
