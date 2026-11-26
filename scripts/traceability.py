"""Checks that every acceptance criterion in SPECS.md has at least one test.

    uv run python scripts/traceability.py

A criterion is declared in SPECS.md as "CA<number>" in the "Acceptance criteria" section
(or "Criterios de aceptación").
A test verifies it if it is marked with @pytest.mark.criterio("CA<number>").
Exits with code 1 if a criterion has no test or if a test cites a criterion that does not exist.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTION_PATTERN = r"^##\s*\d*\.?\s*(?:Acceptance criteria|Criterios de aceptación)\s*$(.*?)(?=^##\s|\Z)"
MARKER_PATTERN = r"criterio\(\s*[\"'](CA\d+)[\"']\s*\)"


def criteria_in_specs() -> set[str]:
    """Returns the CA identifiers declared in the acceptance criteria section of SPECS.md."""
    text = (ROOT / "SPECS.md").read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # ignore the template's instructions
    match = re.search(SECTION_PATTERN, text, flags=re.M | re.S | re.I)
    section = match.group(1) if match else ""
    return set(re.findall(r"\bCA\d+\b", section))


def criteria_in_tests() -> dict[str, list[str]]:
    """Maps each CA identifier cited by a test marker to the test files that cite it."""
    used: dict[str, list[str]] = {}
    for test_file in (ROOT / "tests").rglob("test_*.py"):
        for criterion_id in re.findall(MARKER_PATTERN, test_file.read_text(encoding="utf-8")):
            used.setdefault(criterion_id, []).append(str(test_file.relative_to(ROOT)))
    return used


def sort_key(criterion_id: str) -> tuple[str, int]:
    """Sorts CA identifiers numerically (CA2 before CA10)."""
    return criterion_id[:2], int(criterion_id[2:])


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console (cp1252) cannot display ✔/✘
    defined = criteria_in_specs()
    used = criteria_in_tests()
    if not defined:
        print("✘ SPECS.md has no acceptance criteria (CA1, CA2…) in the 'Acceptance criteria' section.")
        return 1
    without_test = sorted(defined - set(used), key=sort_key)
    unknown = sorted(set(used) - defined, key=sort_key)
    for criterion_id in sorted(defined, key=sort_key):
        files = ", ".join(sorted(set(used.get(criterion_id, [])))) or "NO TEST"
        print(f"{'✔' if criterion_id in used else '✘'} {criterion_id}: {files}")
    for criterion_id in unknown:
        files = ", ".join(sorted(set(used[criterion_id])))
        print(f"✘ {criterion_id}: cited by {files} but not defined in SPECS.md")
    if without_test or unknown:
        print(f"\n{len(without_test)} criterion/criteria without a test and {len(unknown)} unknown reference(s).")
        return 1
    print(f"\nAll criteria ({len(defined)}) have at least one test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())