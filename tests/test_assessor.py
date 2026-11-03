import csv
from pathlib import Path

import pytest

from grc_gap.assessor import Answer, AssessmentError, Control, assess, load_answers, load_controls, write_template
from grc_gap.cli import main
from grc_gap.report import to_html, to_markdown

EXAMPLE = Path(__file__).parent.parent / "examples" / "acme_logistics.csv"


def make_controls():
    return [
        Control("X1", "MFA", "q", ["2-2"], ["j"], 3, "fix 1"),
        Control("X2", "Backups", "q", ["2-9"], ["c"], 1, "fix 2"),
        Control("X3", "Policies", "q", ["1-3"], ["a"], 2, "fix 3"),
    ]


def test_bundled_controls_are_valid():
    controls = load_controls()
    assert len(controls) == 27
    assert len({c.id for c in controls}) == 27


def test_weighted_score_and_na_excluded():
    controls = make_controls()
    answers = [Answer("X1", "implemented"), Answer("X2", "missing"), Answer("X3", "na")]
    r = assess(controls, answers)
    # (3*1.0 + 1*0.0) / (3 + 1) = 0.75 ; X3 is not applicable so not counted
    assert r.overall["NCA ECC"] == pytest.approx(0.75)
    assert r.overall["NIS2"] == pytest.approx(0.75)
    assert "1-3" not in r.ecc_by_subdomain


def test_gap_risk_and_priority_ordering():
    controls = make_controls()
    answers = [Answer("X1", "partial"), Answer("X2", "missing"), Answer("X3", "missing")]
    r = assess(controls, answers)
    # X3: 2*1 = 2 (High), X1: 3*0.5 = 1.5 (Medium), X2: 1*1 = 1 (Medium)
    assert [g.control.id for g in r.gaps] == ["X3", "X1", "X2"]
    assert [g.priority for g in r.gaps] == ["High", "Medium", "Medium"]


def test_rejects_bad_status(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("control_id,status\nX1,maybe\nX2,missing\nX3,missing\n")
    with pytest.raises(AssessmentError, match="maybe"):
        load_answers(p, make_controls())


def test_rejects_unknown_and_missing_controls(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("control_id,status\nZZ,missing\n")
    with pytest.raises(AssessmentError, match="unknown control"):
        load_answers(p, make_controls())
    p.write_text("control_id,status\nX1,missing\n")
    with pytest.raises(AssessmentError, match="No answer for: X2, X3"):
        load_answers(p, make_controls())


def test_template_round_trip(tmp_path):
    controls = load_controls()
    out = tmp_path / "t.csv"
    write_template(out, controls)
    rows = list(csv.DictReader(out.open()))
    assert [r["control_id"] for r in rows] == [c.id for c in controls]


def test_example_end_to_end(tmp_path):
    controls = load_controls()
    r = assess(controls, load_answers(EXAMPLE, controls), "Acme Logistics")
    assert 0 < r.overall["NCA ECC"] < 1
    assert r.gaps[0].priority == "High"
    md = to_markdown(r)
    assert "Remediation roadmap" in md and "C22 Incident response" in md
    assert "<table>" in to_html(r)


def test_cli_fail_under(tmp_path):
    code = main(["assess", str(EXAMPLE), "--out", str(tmp_path / "r.md"), "--fail-under", "90"])
    assert code == 2
    assert (tmp_path / "r.md").exists()
