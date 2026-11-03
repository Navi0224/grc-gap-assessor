"""Turn a Result into a Markdown or HTML report."""

from __future__ import annotations

import html
from datetime import date

from .assessor import Result
from .frameworks import ECC_DOMAINS, ECC_SUBDOMAINS, NIS2_MEASURES, ecc_label, nis2_label


def _pct(x: float) -> str:
    return f"{round(x * 100)}%"


def _rating(x: float) -> str:
    if x >= 0.8:
        return "Good"
    if x >= 0.5:
        return "Needs work"
    return "Weak"


def to_markdown(r: Result) -> str:
    lines = [
        f"# Cybersecurity Gap Assessment: {r.organisation}",
        "",
        f"Date: {date.today().isoformat()}  ",
        "Frameworks: Saudi NCA Essential Cybersecurity Controls (ECC) and EU NIS2 Article 21(2)",
        "",
        "> Self-assessment tool for learning and pre-audit preparation. It is not an official",
        "> certification. Check results against the official NCA ECC and NIS2 texts.",
        "",
        "## Summary",
        "",
        "| Framework | Score | Rating |",
        "|---|---|---|",
    ]
    for name, score in r.overall.items():
        lines.append(f"| {name} | {_pct(score)} | {_rating(score)} |")
    c = r.counts
    lines += [
        "",
        f"Controls answered: {sum(c.values())} "
        f"(implemented {c['implemented']}, partial {c['partial']}, missing {c['missing']}, not applicable {c['na']})",
        "",
        f"Gaps found: {len(r.gaps)} "
        f"(High {sum(g.priority == 'High' for g in r.gaps)}, "
        f"Medium {sum(g.priority == 'Medium' for g in r.gaps)}, "
        f"Low {sum(g.priority == 'Low' for g in r.gaps)})",
        "",
        "## NCA ECC by domain",
        "",
        "| Domain | Score |",
        "|---|---|",
    ]
    for d, s in r.ecc_by_domain.items():
        lines.append(f"| {d}. {ECC_DOMAINS[d]} | {_pct(s)} |")
    lines += ["", "## NCA ECC by subdomain", "", "| Subdomain | Score |", "|---|---|"]
    for code, s in r.ecc_by_subdomain.items():
        lines.append(f"| {code} {ECC_SUBDOMAINS[code]} | {_pct(s)} |")
    lines += ["", "## NIS2 Article 21(2) measures", "", "| Measure | Score |", "|---|---|"]
    for letter, s in r.nis2_by_measure.items():
        lines.append(f"| ({letter}) {NIS2_MEASURES[letter]} | {_pct(s)} |")
    lines += ["", "## Remediation roadmap (highest risk first)", ""]
    if not r.gaps:
        lines.append("No gaps found.")
    for i, g in enumerate(r.gaps, start=1):
        maps = ", ".join([ecc_label(x) for x in g.control.ecc] + [nis2_label(x) for x in g.control.nis2])
        lines += [
            f"### {i}. [{g.priority}] {g.control.id} {g.control.title} ({g.answer.status})",
            "",
            f"- Risk score: {g.risk:g} (weight {g.control.weight})",
            f"- Maps to: {maps}",
            f"- Current state: {g.answer.notes or g.answer.evidence or 'not recorded'}",
            f"- Recommended action: {g.control.remediation}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def _bar(score: float) -> str:
    colour = "#2e7d32" if score >= 0.8 else "#ef6c00" if score >= 0.5 else "#c62828"
    return (f'<div class="bar"><span style="width:{score * 100:.0f}%;background:{colour}"></span></div>'
            f'<b>{_pct(score)}</b>')


def to_html(r: Result) -> str:
    e = html.escape
    rows = lambda items: "".join(f"<tr><td>{e(k)}</td><td>{_bar(v)}</td></tr>" for k, v in items)
    gaps = "".join(
        f"<tr class='{g.priority.lower()}'><td>{g.priority}</td><td>{e(g.control.id)} {e(g.control.title)}</td>"
        f"<td>{e(g.answer.status)}</td><td>{g.risk:g}</td>"
        f"<td>{e(', '.join(['ECC ' + x for x in g.control.ecc] + ['NIS2 (' + x + ')' for x in g.control.nis2]))}</td>"
        f"<td>{e(g.answer.notes or g.answer.evidence or '-')}</td><td>{e(g.control.remediation)}</td></tr>"
        for g in r.gaps
    ) or "<tr><td colspan='7'>No gaps found.</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Gap Assessment: {e(r.organisation)}</title>
<style>
body{{font-family:system-ui,Segoe UI,Arial,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#222}}
h1{{margin-bottom:.2rem}} .note{{background:#fff8e1;border-left:4px solid #f9a825;padding:.6rem 1rem}}
table{{border-collapse:collapse;width:100%;margin:1rem 0}} td,th{{border:1px solid #ddd;padding:.45rem;text-align:left;vertical-align:top;font-size:.92rem}}
th{{background:#f4f4f4}} .bar{{display:inline-block;width:160px;height:10px;background:#eee;margin-right:.5rem;border-radius:5px;overflow:hidden}}
.bar span{{display:block;height:100%}} tr.high td:first-child{{color:#c62828;font-weight:bold}}
tr.medium td:first-child{{color:#ef6c00;font-weight:bold}} tr.low td:first-child{{color:#555}}
.cards{{display:flex;gap:1rem}} .card{{flex:1;border:1px solid #ddd;border-radius:8px;padding:1rem}} .card .big{{font-size:2rem;font-weight:bold}}
</style></head><body>
<h1>Cybersecurity Gap Assessment: {e(r.organisation)}</h1>
<p>Date: {date.today().isoformat()} | Frameworks: Saudi NCA ECC and EU NIS2 Article 21(2)</p>
<p class="note">Self-assessment tool for learning and pre-audit preparation, not an official certification.
Check results against the official NCA ECC and NIS2 texts.</p>
<div class="cards">
{''.join(f'<div class="card">{e(n)}<div class="big">{_pct(s)}</div>{_rating(s)}</div>' for n, s in r.overall.items())}
<div class="card">Gaps<div class="big">{len(r.gaps)}</div>High {sum(g.priority == 'High' for g in r.gaps)} /
Medium {sum(g.priority == 'Medium' for g in r.gaps)} / Low {sum(g.priority == 'Low' for g in r.gaps)}</div>
</div>
<h2>NCA ECC by domain</h2><table>{rows((f"{d}. {ECC_DOMAINS[d]}", s) for d, s in r.ecc_by_domain.items())}</table>
<h2>NCA ECC by subdomain</h2><table>{rows((f"{c} {ECC_SUBDOMAINS[c]}", s) for c, s in r.ecc_by_subdomain.items())}</table>
<h2>NIS2 Article 21(2) measures</h2><table>{rows((f"({l}) {NIS2_MEASURES[l]}", s) for l, s in r.nis2_by_measure.items())}</table>
<h2>Remediation roadmap</h2>
<table><tr><th>Priority</th><th>Control</th><th>Status</th><th>Risk</th><th>Maps to</th><th>Current state</th><th>Recommended action</th></tr>
{gaps}</table>
</body></html>
"""
