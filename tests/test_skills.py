from __future__ import annotations

import re
import unittest
from pathlib import Path

from agent_skills_archive.deploy import discover_skills, parse_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
MAX_SKILL_LINES = 200


def local_markdown_targets(markdown_file: Path) -> set[Path]:
  targets: set[Path] = set()
  text = markdown_file.read_text(encoding="utf-8")
  for raw_target in MARKDOWN_LINK.findall(text):
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
      continue
    targets.add((markdown_file.parent / target.split("#", 1)[0]).resolve())
  return targets


class SkillArchiveTests(unittest.TestCase):
  def test_all_skill_packages_have_canonical_frontmatter(self) -> None:
    skills = discover_skills(SKILLS_ROOT)

    self.assertTrue(skills)
    for skill in skills:
      with self.subTest(skill=skill.name):
        self.assertRegex(skill.name, SKILL_NAME)
        metadata = parse_frontmatter(skill.path / "SKILL.md")
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertTrue(metadata["description"].startswith("Use when "))

  def test_skill_entrypoints_stay_within_context_budget(self) -> None:
    for skill in discover_skills(SKILLS_ROOT):
      with self.subTest(skill=skill.name):
        lines = (skill.path / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(
          len(lines),
          MAX_SKILL_LINES,
          f"{skill.name}/SKILL.md has {len(lines)} lines; move optional detail to a resource",
        )

  def test_local_markdown_links_resolve_inside_the_skill(self) -> None:
    for skill in discover_skills(SKILLS_ROOT):
      for markdown_file in skill.path.rglob("*.md"):
        for target in local_markdown_targets(markdown_file):
          with self.subTest(skill=skill.name, source=markdown_file, target=target):
            self.assertTrue(target.is_relative_to(skill.path.resolve()))
            self.assertTrue(target.exists(), f"broken local link in {markdown_file}: {target}")

  def test_bundled_markdown_resources_are_linked_from_entrypoint(self) -> None:
    for skill in discover_skills(SKILLS_ROOT):
      entrypoint = skill.path / "SKILL.md"
      linked = local_markdown_targets(entrypoint)
      resources = {path.resolve() for path in skill.path.rglob("*.md") if path != entrypoint}
      with self.subTest(skill=skill.name):
        self.assertEqual(resources - linked, set(), "link every Markdown resource from SKILL.md")


if __name__ == "__main__":
  unittest.main()
