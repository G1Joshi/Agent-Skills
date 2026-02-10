#!/usr/bin/env python3

import re
import sys
from pathlib import Path

SCRIPTS_PATH = Path(__file__).parent
ROOT_PATH = SCRIPTS_PATH.parent
SKILLS_PATH = ROOT_PATH / "skills"


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def validate_skill(skill_path: Path) -> list[str]:
    errors = []
    skill_file = skill_path / "SKILL.md"

    if not skill_file.exists():
        errors.append("Missing SKILL.md")
        return errors

    content = skill_file.read_text()
    frontmatter = parse_frontmatter(content)

    if not frontmatter:
        errors.append("Missing or invalid frontmatter (---)")
        return errors

    if "name" not in frontmatter:
        errors.append("Missing 'name' field")
    if "description" not in frontmatter:
        errors.append("Missing 'description' field")

    if "name" in frontmatter:
        expected_name = skill_path.name
        actual_name = frontmatter["name"]
        if actual_name != expected_name:
            errors.append(f"Name mismatch: '{actual_name}' != folder '{expected_name}'")

    return errors


def main() -> int:
    if not SKILLS_PATH.exists():
        print(f"Skills directory not found: {SKILLS_PATH}")
        return 1

    stats = {}
    all_errors = []

    for category in sorted(SKILLS_PATH.iterdir()):
        if not category.is_dir():
            continue

        stats[category.name] = {"valid": 0, "invalid": 0}

        for skill in sorted(category.iterdir()):
            if not skill.is_dir():
                continue

            errors = validate_skill(skill)
            if errors:
                stats[category.name]["invalid"] += 1
                path = f"{category.name}/{skill.name}"
                all_errors.append((path, errors))
            else:
                stats[category.name]["valid"] += 1

    if all_errors:
        print("Validation errors:\n")
        for path, errors in all_errors:
            print(f"  {path}:")
            for error in errors:
                print(f"    - {error}")
        print()

    print(f"{'Category':<20} {'Valid':>8} {'Invalid':>8} {'Total':>8}")
    print("-" * 48)
    total_valid = total_invalid = 0
    for cat, counts in stats.items():
        valid, invalid = counts["valid"], counts["invalid"]
        total_valid += valid
        total_invalid += invalid
        print(f"{cat:<20} {valid:>8} {invalid:>8} {valid + invalid:>8}")
    print("-" * 48)
    print(f"{'Total':<20} {total_valid:>8} {total_invalid:>8} {total_valid + total_invalid:>8}")
    return 0 if total_invalid == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
