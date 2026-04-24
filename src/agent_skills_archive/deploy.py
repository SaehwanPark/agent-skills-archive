from __future__ import annotations

import argparse
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_AGENT = "codex"
IGNORED_NAMES = {".DS_Store", "__pycache__", ".git", ".venv"}


@dataclass(frozen=True)
class Skill:
  name: str
  path: Path
  description: str


@dataclass(frozen=True)
class Target:
  agent: str
  scope: str
  path: Path


class DeployError(RuntimeError):
  """Raised when deployment cannot continue safely."""


class UserCancel(RuntimeError):
  """Raised when the user exits chooser mode without selecting skills."""


def repo_root() -> Path:
  return Path(__file__).resolve().parents[2]


def default_source() -> Path:
  return repo_root() / "skills"


def _home() -> Path:
  return Path.home()


def target_for(agent: str, scope: str, project: Path) -> Target:
  project = project.expanduser().resolve()
  home = _home()

  if agent == "codex":
    path = home / ".agents" / "skills" if scope == "personal" else project / ".agents" / "skills"
  elif agent == "codex-legacy":
    if scope != "personal":
      raise DeployError("codex-legacy only supports --scope personal")
    path = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser() / "skills"
  elif agent == "claude":
    path = home / ".claude" / "skills" if scope == "personal" else project / ".claude" / "skills"
  elif agent == "forge":
    path = home / "forge" / "skills" if scope == "personal" else project / ".forge" / "skills"
  elif agent == "droid":
    path = home / ".factory" / "skills" if scope == "personal" else project / ".factory" / "skills"
  elif agent == "droid-compat":
    if scope != "project":
      raise DeployError("droid-compat only supports --scope project")
    path = project / ".agent" / "skills"
  elif agent == "opencode":
    path = (
      home / ".config" / "opencode" / "skills"
      if scope == "personal"
      else project / ".opencode" / "skills"
    )
  else:
    raise DeployError(f"unknown agent: {agent}")

  return Target(agent=agent, scope=scope, path=path)


def agents_for(agent: str) -> list[str]:
  if agent == "all":
    return ["codex", "claude", "forge", "droid", "opencode"]
  return [agent]


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
  lines = skill_file.read_text(encoding="utf-8").splitlines()
  if not lines or lines[0].strip() != "---":
    raise DeployError(f"{skill_file} is missing YAML frontmatter")

  data: dict[str, str] = {}
  for line in lines[1:]:
    if line.strip() == "---":
      return data
    if ":" not in line:
      continue
    key, value = line.split(":", 1)
    data[key.strip()] = value.strip().strip('"').strip("'")

  raise DeployError(f"{skill_file} has unterminated YAML frontmatter")


def discover_skills(source: Path) -> list[Skill]:
  source = source.expanduser().resolve()
  if not source.exists():
    raise DeployError(f"source directory does not exist: {source}")
  if not source.is_dir():
    raise DeployError(f"source is not a directory: {source}")

  skills: list[Skill] = []
  for path in sorted(source.iterdir(), key=lambda item: item.name):
    if not path.is_dir() or path.name in IGNORED_NAMES:
      continue
    skill_file = path / "SKILL.md"
    if not skill_file.exists():
      raise DeployError(f"{path} is missing SKILL.md")
    metadata = parse_frontmatter(skill_file)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not name:
      raise DeployError(f"{skill_file} frontmatter is missing name")
    if not description:
      raise DeployError(f"{skill_file} frontmatter is missing description")
    if name != path.name:
      raise DeployError(f"{skill_file} name {name!r} does not match directory {path.name!r}")
    skills.append(Skill(name=name, path=path, description=description))
  return skills


def select_skills(skills: Sequence[Skill], selected_names: Sequence[str]) -> list[Skill]:
  if not selected_names:
    return list(skills)

  by_name = {skill.name: skill for skill in skills}
  missing = sorted(set(selected_names) - set(by_name))
  if missing:
    raise DeployError(f"unknown skill(s): {', '.join(missing)}")
  return [by_name[name] for name in selected_names]


def choose_skills(skills: Sequence[Skill], input_fn=None) -> list[Skill]:
  if not skills:
    raise DeployError("no skills found")

  if input_fn is None:
    input_fn = input

  print("Choose skills to deploy:")
  print("  0) all skills")
  for index, skill in enumerate(skills, start=1):
    print(f"  {index}) {skill.name} - {skill.description}")
  response = input_fn("Select one or more numbers separated by commas, or press Enter to cancel: ").strip()
  if not response:
    raise UserCancel("no skills selected")
  if response.lower() == "all" or response == "0":
    return list(skills)

  selected_indexes: list[int] = []
  for part in response.split(","):
    token = part.strip()
    if not token:
      continue
    if not token.isdigit():
      raise DeployError(f"invalid selection: {token}")
    selected_indexes.append(int(token))

  if not selected_indexes:
    raise UserCancel("no skills selected")

  selected: list[Skill] = []
  for index in selected_indexes:
    if index < 1 or index > len(skills):
      raise DeployError(f"selection out of range: {index}")
    selected.append(skills[index - 1])
  return selected


def ignore_patterns(_directory: str, names: list[str]) -> set[str]:
  return {name for name in names if name in IGNORED_NAMES}


def deploy_skill(skill: Skill, target: Target, *, dry_run: bool, force: bool) -> str:
  destination = target.path / skill.name
  if destination.exists() and not force:
    raise DeployError(f"{destination} already exists; pass --force to replace it")

  if dry_run:
    action = "replace" if destination.exists() else "copy"
    return f"[dry-run] {action} {skill.path} -> {destination}"

  target.path.mkdir(parents=True, exist_ok=True)
  if destination.exists():
    shutil.rmtree(destination)
  shutil.copytree(skill.path, destination, ignore=ignore_patterns)
  return f"copied {skill.name} -> {destination}"


def print_skills(skills: Iterable[Skill]) -> None:
  for skill in skills:
    print(f"{skill.name}\t{skill.description}")


def print_targets(agent: str, scope: str, project: Path) -> None:
  for agent_name in agents_for(agent):
    target = target_for(agent_name, scope, project)
    print(f"{target.agent}\t{target.scope}\t{target.path}")


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="Deploy reusable agent skills into personal or project-specific locations.",
  )
  parser.add_argument(
    "--agent",
    default=DEFAULT_AGENT,
    choices=["codex", "codex-legacy", "claude", "forge", "droid", "droid-compat", "opencode", "all"],
    help="Agent target to deploy for. Defaults to codex.",
  )
  parser.add_argument(
    "--scope",
    default="personal",
    choices=["personal", "project"],
    help="Install into a personal or project-specific skill directory.",
  )
  parser.add_argument(
    "--project",
    type=Path,
    default=Path.cwd(),
    help="Project root for --scope project. Defaults to the current directory.",
  )
  parser.add_argument(
    "--source",
    type=Path,
    default=default_source(),
    help="Directory containing skill folders. Defaults to ./skills in this repo.",
  )
  parser.add_argument(
    "--skill",
    action="append",
    default=[],
    help="Skill name to deploy directly. May be passed multiple times and bypasses the chooser.",
  )
  parser.add_argument("--all", action="store_true", help="Deploy every discovered skill.")
  parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without writing files.")
  parser.add_argument("--force", action="store_true", help="Replace existing destination skill directories.")
  parser.add_argument("--list-skills", action="store_true", help="List discovered skills and exit.")
  parser.add_argument("--list-targets", action="store_true", help="List resolved destination directories and exit.")
  return parser


def run(argv: Sequence[str] | None = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)

  try:
    skills = discover_skills(args.source)
    if args.list_skills:
      print_skills(skills)
      return 0

    if args.list_targets:
      print_targets(args.agent, args.scope, args.project)
      return 0

    if args.all:
      selected = list(skills)
    elif args.skill:
      selected = select_skills(skills, args.skill)
    else:
      if not sys.stdin.isatty():
        raise DeployError("chooser mode requires an interactive terminal; use --skill or --all")
      selected = choose_skills(skills)

    for agent_name in agents_for(args.agent):
      target = target_for(agent_name, args.scope, args.project)
      for skill in selected:
        print(deploy_skill(skill, target, dry_run=args.dry_run, force=args.force))
    return 0
  except UserCancel as error:
    print(f"error: {error}", file=sys.stderr)
    return 1
  except DeployError as error:
    print(f"error: {error}", file=sys.stderr)
    return 1


def main() -> None:
  raise SystemExit(run())


if __name__ == "__main__":
  main()
