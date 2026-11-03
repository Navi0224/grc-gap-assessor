"""Core logic: load controls and answers, score them, and find the gaps.

How scoring works (simple on purpose, so it is easy to explain):
  - Each answer has a status: implemented = 1.0, partial = 0.5, missing = 0.0.
    "na" (not applicable) is left out of the scores completely.
  - Each control has a weight from 1 to 3 (how much damage a gap could cause).
  - A framework area's score = sum(weight * status score) / sum(weight).
  - A gap's risk = weight * (1 - status score). So a missing weight-3 control
    has risk 3 (High) and a partial weight-1 control has risk 0.5 (Low).
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

from .frameworks import ECC_DOMAINS, ECC_SUBDOMAINS, NIS2_MEASURES

STATUS_SCORES = {"implemented": 1.0, "partial": 0.5, "missing": 0.0}
VALID_STATUSES = set(STATUS_SCORES) | {"na"}
DEFAULT_CONTROLS = Path(__file__).with_name("controls.json")


class AssessmentError(ValueError):
    """Raised when the input files are not valid."""


@dataclass
class Control:
    id: str
    title: str
    question: str
    ecc: list[str]
    nis2: list[str]
    weight: int
    remediation: str


@dataclass
class Answer:
    control_id: str
    status: str
    evidence: str = ""
    notes: str = ""


@dataclass
class Gap:
    control: Control
    answer: Answer
    risk: float

    @property
    def priority(self) -> str:
        if self.risk >= 2:
            return "High"
        if self.risk >= 1:
            return "Medium"
        return "Low"


@dataclass
class Result:
    organisation: str
    overall: dict[str, float]          # framework name -> score 0..1
    ecc_by_domain: dict[str, float]    # "1".."5" -> score (only scored domains)
    ecc_by_subdomain: dict[str, float]
    nis2_by_measure: dict[str, float]
    gaps: list[Gap] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)


def load_controls(path: Path = DEFAULT_CONTROLS) -> list[Control]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    controls = [Control(**item) for item in data]
    seen = set()
    for c in controls:
        if c.id in seen:
            raise AssessmentError(f"Duplicate control id {c.id}")
        seen.add(c.id)
        if not 1 <= c.weight <= 3:
            raise AssessmentError(f"{c.id}: weight must be 1-3")
        for code in c.ecc:
            if code not in ECC_SUBDOMAINS:
                raise AssessmentError(f"{c.id}: unknown ECC subdomain {code}")
        for letter in c.nis2:
            if letter not in NIS2_MEASURES:
                raise AssessmentError(f"{c.id}: unknown NIS2 measure {letter}")
    return controls


def load_answers(path: Path, controls: list[Control]) -> list[Answer]:
    known = {c.id for c in controls}
    answers: list[Answer] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"control_id", "status"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise AssessmentError("CSV must have at least the columns: control_id, status")
        for line_no, row in enumerate(reader, start=2):
            cid = (row.get("control_id") or "").strip()
            status = (row.get("status") or "").strip().lower()
            if not cid:
                continue  # skip blank lines
            if cid not in known:
                raise AssessmentError(f"Line {line_no}: unknown control id '{cid}'")
            if status not in VALID_STATUSES:
                raise AssessmentError(
                    f"Line {line_no}: status '{status}' for {cid} must be one of "
                    + ", ".join(sorted(VALID_STATUSES))
                )
            answers.append(Answer(cid, status, (row.get("evidence") or "").strip(),
                                  (row.get("notes") or "").strip()))
    answered = {a.control_id for a in answers}
    if len(answered) != len(answers):
        raise AssessmentError("A control is answered more than once")
    unanswered = sorted(known - answered)
    if unanswered:
        raise AssessmentError("No answer for: " + ", ".join(unanswered)
                              + " (use status 'na' if it does not apply)")
    return answers


def _weighted(pairs: list[tuple[int, float]]) -> float | None:
    total = sum(w for w, _ in pairs)
    if total == 0:
        return None
    return sum(w * s for w, s in pairs) / total


def assess(controls: list[Control], answers: list[Answer], organisation: str = "Organisation") -> Result:
    by_id = {c.id: c for c in controls}
    ecc_sub: dict[str, list[tuple[int, float]]] = {}
    ecc_dom: dict[str, list[tuple[int, float]]] = {}
    nis2: dict[str, list[tuple[int, float]]] = {}
    all_ecc: list[tuple[int, float]] = []
    all_nis2: list[tuple[int, float]] = []
    gaps: list[Gap] = []
    counts = {s: 0 for s in VALID_STATUSES}

    for a in answers:
        c = by_id[a.control_id]
        counts[a.status] += 1
        if a.status == "na":
            continue
        score = STATUS_SCORES[a.status]
        pair = (c.weight, score)
        if c.ecc:
            all_ecc.append(pair)
        if c.nis2:
            all_nis2.append(pair)
        for code in c.ecc:
            ecc_sub.setdefault(code, []).append(pair)
            ecc_dom.setdefault(code.split("-")[0], []).append(pair)
        for letter in c.nis2:
            nis2.setdefault(letter, []).append(pair)
        if score < 1.0:
            gaps.append(Gap(c, a, risk=c.weight * (1 - score)))

    # Highest risk first; ties broken by control id so output is stable.
    gaps.sort(key=lambda g: (-g.risk, g.control.id))

    def scored(groups):
        out = {}
        for key, pairs in groups.items():
            value = _weighted(pairs)
            if value is not None:
                out[key] = value
        return dict(sorted(out.items(), key=lambda kv: _sort_key(kv[0])))

    overall = {}
    for name, pairs in (("NCA ECC", all_ecc), ("NIS2", all_nis2)):
        value = _weighted(pairs)
        if value is not None:
            overall[name] = value

    return Result(
        organisation=organisation,
        overall=overall,
        ecc_by_domain={k: v for k, v in scored(ecc_dom).items() if k in ECC_DOMAINS},
        ecc_by_subdomain=scored(ecc_sub),
        nis2_by_measure=scored(nis2),
        gaps=gaps,
        counts=counts,
    )


def _sort_key(code: str):
    """Sort '1-10' after '1-9' and letters alphabetically."""
    parts = code.split("-")
    return [int(p) if p.isdigit() else p for p in parts]


def write_template(path: Path, controls: list[Control]) -> None:
    """Write a blank answer sheet the user fills in."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["control_id", "title", "question", "status", "evidence", "notes"])
        for c in controls:
            writer.writerow([c.id, c.title, c.question, "", "", ""])
