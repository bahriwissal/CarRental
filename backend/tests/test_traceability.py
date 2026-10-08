"""Guards the requirements-as-code conventions in tests/features/.

Every Scenario / Scenario Outline must carry exactly one @REQ-<AREA>-<NNN> tag, and IDs are unique.
"""

import re
from pathlib import Path

FEATURES = Path(__file__).parent / "features"
REQ_TAG = re.compile(r"@(REQ-[A-Z]+-\d{3})\b")


def collect_scenarios():
    """Yield (file, line_no, scenario_title, [req ids]) for every scenario."""
    for path in sorted(FEATURES.glob("*.feature")):
        pending_tags: list[str] = []
        for no, raw in enumerate(path.read_text().splitlines(), start=1):
            line = raw.strip()
            if line.startswith("@"):
                pending_tags += REQ_TAG.findall(line)
            elif line.startswith(("Scenario:", "Scenario Outline:")):
                yield path.name, no, line, pending_tags
                pending_tags = []
            elif line and not line.startswith("#"):
                pending_tags = []


def test_feature_files_exist():
    assert list(FEATURES.glob("*.feature")), "no feature files found"


def test_every_scenario_has_exactly_one_requirement_id():
    problems = [
        f"{file}:{no} {title} -> {ids or 'no @REQ tag'}"
        for file, no, title, ids in collect_scenarios()
        if len(ids) != 1
    ]
    assert not problems, "\n".join(problems)


def test_requirement_ids_are_unique():
    seen: dict[str, str] = {}
    duplicates = []
    for file, no, _, ids in collect_scenarios():
        for req in ids:
            if req in seen:
                duplicates.append(f"{req} in {seen[req]} and {file}:{no}")
            seen[req] = f"{file}:{no}"
    assert not duplicates, "\n".join(duplicates)
