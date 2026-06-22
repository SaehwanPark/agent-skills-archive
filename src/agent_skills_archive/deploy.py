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
  reference_path: Path | None = None


@dataclass(frozen=True)
class Operation:
  kind: str
  skill: Skill
  source: Path
  destination: Path


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
  canonical = home / ".agents" / "skills" if scope == "personal" else project / ".agents" / "skills"
  reference: Path | None = None

  if agent == "codex":
    pass
  elif agent == "codex-legacy":
    if scope != "personal":
      raise DeployError("codex-legacy only supports --scope personal")
    reference = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser() / "skills"
  elif agent in ("antigravity", "gemini"):
    if scope == "personal":
      reference = home / ".gemini" / "skills"
  elif agent == "claude":
    reference = (
      home / ".claude" / "skills" if scope == "personal" else project / ".claude" / "skills"
    )
  elif agent == "forge":
    if scope == "project":
      reference = project / ".forge" / "skills"
  elif agent == "droid":
    reference = (
      home / ".factory" / "skills" if scope == "personal" else project / ".factory" / "skills"
    )
  elif agent == "droid-compat":
    if scope != "project":
      raise DeployError("droid-compat only supports --scope project")
    reference = project / ".agent" / "skills"
  elif agent == "opencode":
    pass
  else:
    raise DeployError(f"unknown agent: {agent}")

  return Target(agent=agent, scope=scope, path=canonical, reference_path=reference)


def agents_for(agent: str) -> list[str]:
  if agent == "all":
    return ["codex", "claude", "forge", "droid", "opencode", "antigravity"]
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


def _lexists(path: Path) -> bool:
  return path.exists() or path.is_symlink()


def _link_points_to(destination: Path, source: Path) -> bool:
  return (
    destination.is_symlink()
    and destination.resolve(strict=False) == source.resolve(strict=False)
  )


def plan_deployment(skills: Sequence[Skill], targets: Sequence[Target]) -> list[Operation]:
  operations: list[Operation] = []
  seen: set[tuple[str, Path]] = set()
  for target in targets:
    for skill in skills:
      copy_destination = target.path / skill.name
      copy_key = ("copy", copy_destination)
      if copy_key not in seen:
        operations.append(Operation("copy", skill, skill.path, copy_destination))
        seen.add(copy_key)

      if target.reference_path is not None:
        link_destination = target.reference_path / skill.name
        link_key = ("link", link_destination)
        if link_key not in seen:
          operations.append(Operation("link", skill, copy_destination, link_destination))
          seen.add(link_key)
  return operations


def validate_operations(operations: Sequence[Operation], *, force: bool) -> None:
  for operation in operations:
    if not _lexists(operation.destination):
      continue
    if operation.kind == "link" and _link_points_to(operation.destination, operation.source):
      continue
    if not force:
      raise DeployError(f"{operation.destination} already exists; pass --force to replace it")


def _remove_destination(destination: Path) -> None:
  if destination.is_symlink() or destination.is_file():
    destination.unlink()
  else:
    shutil.rmtree(destination)


def execute_operation(operation: Operation, *, dry_run: bool, force: bool) -> str:
  destination = operation.destination
  exists = _lexists(destination)

  if operation.kind == "link" and _link_points_to(destination, operation.source):
    return f"already linked {destination} -> {operation.source}"

  if dry_run:
    action = f"replace-{operation.kind}" if exists else operation.kind
    return f"[dry-run] {action} {operation.source} -> {destination}"

  destination.parent.mkdir(parents=True, exist_ok=True)
  if exists:
    if not force:
      raise DeployError(f"{destination} already exists; pass --force to replace it")
    _remove_destination(destination)

  if operation.kind == "copy":
    shutil.copytree(operation.source, destination, ignore=ignore_patterns)
    return f"copied {operation.skill.name} -> {destination}"

  relative_source = os.path.relpath(operation.source, destination.parent)
  try:
    destination.symlink_to(relative_source, target_is_directory=True)
  except OSError as error:
    raise DeployError(f"could not link {destination} -> {operation.source}: {error}") from error
  return f"linked {destination} -> {operation.source}"


def deploy_operations(operations: Sequence[Operation], *, dry_run: bool, force: bool) -> list[str]:
  validate_operations(operations, force=force)
  return [execute_operation(operation, dry_run=dry_run, force=force) for operation in operations]


def deploy_skill(skill: Skill, target: Target, *, dry_run: bool, force: bool) -> str:
  operation = Operation("copy", skill, skill.path, target.path / skill.name)
  validate_operations([operation], force=force)
  return execute_operation(operation, dry_run=dry_run, force=force)


def print_skills(skills: Iterable[Skill]) -> None:
  for skill in skills:
    print(f"{skill.name}\t{skill.description}")


def print_targets(agent: str, scope: str, project: Path) -> None:
  targets = [target_for(agent_name, scope, project) for agent_name in agents_for(agent)]
  canonical_paths: set[Path] = set()
  for target in targets:
    if target.path not in canonical_paths:
      print(f"canonical\t{target.scope}\tcopy\t{target.path}")
      canonical_paths.add(target.path)
    if target.reference_path is not None:
      print(f"{target.agent}\t{target.scope}\tlink\t{target.reference_path}\t{target.path}")


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="Deploy reusable agent skills into personal or project-specific locations.",
  )
  parser.add_argument(
    "--agent",
    default=DEFAULT_AGENT,
    choices=["codex", "codex-legacy", "claude", "forge", "droid", "droid-compat", "opencode", "antigravity", "all"],
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
  parser.add_argument("--dry-run", action="store_true", help="Show deployment operations without writing files.")
  parser.add_argument("--force", action="store_true", help="Replace conflicting destination entries.")
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

    targets = [
      target_for(agent_name, args.scope, args.project)
      for agent_name in agents_for(args.agent)
    ]
    operations = plan_deployment(selected, targets)
    for message in deploy_operations(operations, dry_run=args.dry_run, force=args.force):
      print(message)
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
