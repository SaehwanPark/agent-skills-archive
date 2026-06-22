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
  deploy_operations,
  deploy_skill,
  discover_skills,
  plan_deployment,
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
      self.assertEqual(
        target_for("claude", "project", project).reference_path,
        project / ".claude" / "skills",
      )
      self.assertEqual(
        target_for("forge", "project", project).reference_path,
        project / ".forge" / "skills",
      )
      self.assertEqual(
        target_for("droid", "project", project).reference_path,
        project / ".factory" / "skills",
      )
      self.assertEqual(
        target_for("droid-compat", "project", project).reference_path,
        project / ".agent" / "skills",
      )
      self.assertIsNone(target_for("opencode", "project", project).reference_path)

  def test_native_personal_targets_do_not_create_references(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      project = Path(temp)

      self.assertIsNone(target_for("codex", "personal", project).reference_path)
      self.assertIsNone(target_for("forge", "personal", project).reference_path)
      self.assertIsNone(target_for("opencode", "personal", project).reference_path)

  def test_codex_legacy_uses_codex_home(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      with mock.patch.dict(os.environ, {"CODEX_HOME": temp}):
        target = target_for("codex-legacy", "personal", Path.cwd())

      self.assertEqual(target.reference_path, Path(temp) / "skills")

  def test_claude_deploys_canonical_copy_and_relative_reference(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      skill_path = write_skill(source, "example")
      (skill_path / "references").mkdir()
      (skill_path / "references" / "guide.md").write_text("guide", encoding="utf-8")
      skill = discover_skills(source)[0]
      target = target_for("claude", "project", root / "project")

      operations = plan_deployment([skill], [target])
      deploy_operations(operations, dry_run=False, force=False)

      canonical = target.path / "example"
      reference = target.reference_path / "example"  # type: ignore[operator]
      self.assertTrue(canonical.is_dir())
      self.assertTrue(reference.is_symlink())
      self.assertFalse(reference.readlink().is_absolute())
      self.assertEqual((reference / "references" / "guide.md").read_text(encoding="utf-8"), "guide")

  def test_all_targets_copy_canonical_skill_once(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      targets = [
        target_for(agent, "project", root / "project")
        for agent in ["codex", "claude", "forge", "droid", "opencode", "antigravity"]
      ]

      operations = plan_deployment([skill], targets)

      self.assertEqual(sum(operation.kind == "copy" for operation in operations), 1)
      self.assertEqual(sum(operation.kind == "link" for operation in operations), 3)

  def test_existing_correct_reference_is_idempotent(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("claude", "project", root / "project")
      operations = plan_deployment([skill], [target])
      deploy_operations(operations, dry_run=False, force=False)

      link_operation = next(operation for operation in operations if operation.kind == "link")
      messages = deploy_operations([link_operation], dry_run=False, force=False)

      self.assertIn("already linked", messages[0])

  def test_force_replaces_copied_compatibility_directory_with_reference(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("claude", "project", root / "project")
      reference = target.reference_path / "example"  # type: ignore[operator]
      reference.mkdir(parents=True)
      (reference / "old.txt").write_text("old", encoding="utf-8")

      operations = plan_deployment([skill], [target])
      deploy_operations(operations, dry_run=False, force=True)

      self.assertTrue(reference.is_symlink())
      self.assertFalse((reference / "old.txt").exists())

  def test_preflight_prevents_writes_when_later_operation_conflicts(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("claude", "project", root / "project")
      reference = target.reference_path / "example"  # type: ignore[operator]
      reference.mkdir(parents=True)
      operations = plan_deployment([skill], [target])

      with self.assertRaisesRegex(DeployError, "already exists"):
        deploy_operations(operations, dry_run=False, force=False)

      self.assertFalse((target.path / "example").exists())

  def test_dry_run_does_not_create_canonical_copy_or_reference(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")
      skill = discover_skills(source)[0]
      target = target_for("claude", "project", root / "project")

      messages = deploy_operations(
        plan_deployment([skill], [target]),
        dry_run=True,
        force=False,
      )

      self.assertEqual(len(messages), 2)
      self.assertIn("[dry-run] copy", messages[0])
      self.assertIn("[dry-run] link", messages[1])
      self.assertFalse(target.path.exists())
      self.assertFalse(target.reference_path.exists())  # type: ignore[union-attr]

  def test_force_replaces_wrong_and_broken_references(self) -> None:
    for existing_target in ["elsewhere", "missing"]:
      with self.subTest(existing_target=existing_target), tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        source = root / "source"
        source.mkdir()
        write_skill(source, "example")
        skill = discover_skills(source)[0]
        target = target_for("claude", "project", root / "project")
        reference = target.reference_path / "example"  # type: ignore[operator]
        reference.parent.mkdir(parents=True)
        reference.symlink_to(existing_target, target_is_directory=True)

        deploy_operations(plan_deployment([skill], [target]), dry_run=False, force=True)

        self.assertTrue(reference.is_symlink())
        self.assertEqual(reference.resolve(), (target.path / "example").resolve())

  def test_readme_skill_table_matches_archive(self) -> None:
    repo = Path(__file__).resolve().parents[1]
    expected = {skill.name for skill in discover_skills(repo / "skills")}
    readme = (repo / "README.md").read_text(encoding="utf-8")
    skills_section = readme.split("## Skills in this archive", 1)[1]
    section = skills_section.split("## What a skill looks like", 1)[0]
    documented = {
      line.split("`", 2)[1]
      for line in section.splitlines()
      if line.startswith("| `")
    }

    self.assertEqual(documented, expected)

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

  def test_run_lists_canonical_and_reference_targets(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
      root = Path(temp)
      source = root / "source"
      source.mkdir()
      write_skill(source, "example")

      with mock.patch("sys.stdout", new=StringIO()) as stdout:
        exit_code = run([
          "--source",
          str(source),
          "--agent",
          "claude",
          "--scope",
          "project",
          "--project",
          str(root / "project"),
          "--list-targets",
        ])

      output = stdout.getvalue()
      self.assertEqual(exit_code, 0)
      self.assertIn("canonical\tproject\tcopy", output)
      self.assertIn("claude\tproject\tlink", output)

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
