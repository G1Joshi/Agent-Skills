#!/usr/bin/env python3

import sys
from pathlib import Path

SCRIPTS_PATH = Path(__file__).parent
ROOT_PATH = SCRIPTS_PATH.parent
SKILLS_PATH = ROOT_PATH / "skills"


def main() -> int:
    if not SKILLS_PATH.exists():
        print(f"Skills directory not found: {SKILLS_PATH}")
        return 1

    total = 0
    categories = {}

    for category in sorted(SKILLS_PATH.iterdir()):
        if not category.is_dir():
            continue

        skills = [s for s in category.iterdir() if s.is_dir() and (s / "SKILL.md").exists()]
        count = len(skills)
        categories[category.name] = count
        total += count

    print(f"{'Category':<20} {'Count':>6}")
    print("-" * 28)
    for cat, count in categories.items():
        print(f"{cat:<20} {count:>6}")
    print("-" * 28)
    print(f"{'Total':<20} {total:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
