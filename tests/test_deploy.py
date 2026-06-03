from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from agent_skills_archive.deploy import (
  DeployError,
  UserCancel,
  choose_skills,
  deploy_skill,
  discover_skills,
  run,
  select_skills,
  target_for,
)


def write_skill(root: Path, name: str = "example", description: str = "Example skill.") -> Path:
  skill = root / name
  skill.mkdir(parents=True)
  (skill / "SKILL.md").write_text(
    f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
    encoding="utf-8",
  )
  return skill


class DeployTests(unittest.TestCase):
  def test_discovers_valid_skills(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "example", "Reusable example.")

      skills = discover_skills(root)

      self.assertEqual(len(skills), 1)
      self.assertEqual(skills[0].name, "example")
      self.assertEqual(skills[0].description, "Reusable example.")

  def test_rejects_name_mismatch(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      skill = root / "directory-name"
      skill.mkdir()
      (skill / "SKILL.md").write_text(
        "---\nname: metadata-name\ndescription: mismatch\n---\n",
        encoding="utf-8",
      )

      with self.assertRaisesRegex(DeployError, "does not match directory"):
        discover_skills(root)

  def test_select_skills_rejects_unknown_name(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "example")
      skills = discover_skills(root)

      with self.assertRaisesRegex(DeployError, "unknown skill"):
        select_skills(skills, ["missing"])

  def test_target_resolution(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      project = Path(temp).resolve()

      self.assertEqual(target_for("codex", "project", project).path, project / ".agents" / "skills")
      self.assertEqual(target_for("claude", "project", project).path, project / ".claude" / "skills")
      self.assertEqual(target_for("forge", "project", project).path, project / ".forge" / "skills")
      self.assertEqual(target_for("droid", "project", project).path, project / ".factory" / "skills")
      self.assertEqual(target_for("droid-compat", "project", project).path, project / ".agent" / "skills")
      self.assertEqual(target_for("opencode", "project", project).path, project / ".opencode" / "skills")

  def test_codex_legacy_uses_codex_home(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      with mock.patch.dict(os.environ, {"CODEX_HOME": temp}):
        target = target_for("codex-legacy", "personal", Path.cwd())

      self.assertEqual(target.path, Path(temp) / "skills")

  def test_dry_run_does_not_copy(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("codex", "project", root / "project")

      message = deploy_skill(skill, target, dry_run=True, force=False)

      self.assertIn("[dry-run] copy", message)
      self.assertFalse((target.path / "example").exists())

  def test_existing_destination_requires_force(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("codex", "project", root / "project")
      (target.path / "example").mkdir(parents=True)

      with self.assertRaisesRegex(DeployError, "already exists"):
        deploy_skill(skill, target, dry_run=False, force=False)

  def test_run_lists_skills(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "example")

      with mock.patch("sys.stdout", new=StringIO()) as stdout:
        exit_code = run(["--source", str(root), "--list-skills"])

      self.assertEqual(exit_code, 0)
      self.assertIn("example\tExample skill.", stdout.getvalue())

  def test_choose_skills_selects_multiple(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "alpha", "Alpha skill.")
      write_skill(root, "beta", "Beta skill.")
      skills = discover_skills(root)

      with mock.patch("builtins.input", return_value="1,2"):
        selected = choose_skills(skills)

      self.assertEqual([skill.name for skill in selected], ["alpha", "beta"])

  def test_choose_skills_supports_all(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "alpha", "Alpha skill.")
      write_skill(root, "beta", "Beta skill.")
      skills = discover_skills(root)

      with mock.patch("builtins.input", return_value="all"):
        selected = choose_skills(skills)

      self.assertEqual([skill.name for skill in selected], ["alpha", "beta"])

  def test_choose_skills_cancel(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "alpha", "Alpha skill.")
      skills = discover_skills(root)

      with mock.patch("builtins.input", return_value=""):
        with self.assertRaises(UserCancel):
          choose_skills(skills)

  def test_run_all_flag_deploys_without_prompt(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      write_skill(root, "alpha", "Alpha skill.")
      write_skill(root, "beta", "Beta skill.")
      project = root / "project"

      with mock.patch("builtins.input") as input_mock:
        exit_code = run(["--source", str(root), "--project", str(project), "--all", "--dry-run"])

      self.assertEqual(exit_code, 0)
      input_mock.assert_not_called()

  def test_repo_launcher_resolves_uv_from_path(self) -> None:
    repo = Path(__file__).resolve().parents[1]

    with tempfile.TemporaryDirectory() as temp:
      bin_dir = Path(temp) / "bin"
      bin_dir.mkdir()
      fake_uv = bin_dir / "uv"
      fake_uv.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$*\"\n"
        "printf 'fp-developer\\tFake skill output.\\n'\n",
        encoding="utf-8",
      )
      fake_uv.chmod(0o755)

      result = subprocess.run(
        [str(repo / "bin" / "deploy-skills"), "--list-skills"],
        cwd=tempfile.gettempdir(),
        env={"PATH": f"{bin_dir}:/usr/bin:/bin"},
        check=True,
        capture_output=True,
        text=True,
      )

    self.assertIn("fp-developer\t", result.stdout)
    self.assertIn(f"run --project {repo} deploy-skills --list-skills", result.stdout)


if __name__ == "__main__":
  unittest.main()
