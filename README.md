# GRC Gap Assessor: Saudi NCA ECC + EU NIS2

A command-line tool that scores an organisation's cybersecurity controls against two frameworks:

- **Saudi NCA Essential Cybersecurity Controls (ECC)**, the baseline that the Saudi National Cybersecurity Authority requires of government bodies and critical national infrastructure.
- **EU NIS2 Directive, Article 21(2)**, the ten minimum risk-management measures for essential and important entities in the EU.

You fill in one answer sheet (27 controls). The tool maps each answer to both frameworks and calculates weighted compliance scores. It then produces a **risk-ranked remediation roadmap** in Markdown and HTML.

Sample output: [examples/sample_report.md](examples/sample_report.md) (open `examples/sample_report.html` in a browser for the visual version).

## Why I built it

This tool imitates the gap assessment a GRC consultant runs before an audit. One assessment is mapped to more than one regulation, so the client only answers each question once.

## Quick start

```bash
# Python 3.10+; no third-party packages needed (pytest only for tests)
python -m grc_gap template my_answers.csv          # 1. blank answer sheet
# 2. fill in status = implemented / partial / missing / na (+ evidence, notes)
python -m grc_gap assess my_answers.csv --org "My Company" --out report.md --html report.html
```

Try it with the fictional example:

```bash
python -m grc_gap assess examples/acme_logistics.csv --org "Acme Logistics (fictional)" --html report.html
```

Use `--fail-under 70` to exit with code 2 when any framework scores below 70%. This lets the tool act as a compliance gate in a CI pipeline.

## How scoring works

| Status | Score |
|---|---|
| implemented | 1.0 |
| partial | 0.5 |
| missing | 0.0 |
| na | excluded |

- Each control has a **weight** (1 to 3) based on how much damage a gap could cause.
- Area score = Σ(weight × score) / Σ(weight).
- Gap risk = weight × (1 − score). **High** if risk ≥ 2, **Medium** if ≥ 1, otherwise **Low**.

## Project layout

```
grc_gap/
  controls.json   27 controls, each mapped to ECC subdomains and NIS2 measures
  frameworks.py   ECC domain/subdomain names and NIS2 Article 21(2) measures
  assessor.py     loading, validation, scoring, gap ranking
  report.py       Markdown and HTML reports
  cli.py          command-line interface
tests/            pytest tests
examples/         fictional company answers + generated sample report
```

## Run the tests

```bash
pip install pytest
python -m pytest -q
```

## Limitations (read before using for real)

- The control wording and mappings are my own simplified summaries. They are not the official text. ECC subdomain numbering follows the ECC structure, so check it against the latest official NCA ECC document.
- The tool covers ECC domains 1 to 4. Domain 5 (industrial control systems) has a separate NCA standard and is out of scope.
- It is a self-assessment aid, not a certification or legal advice.

## Ideas for future work

- Add ISO 27001:2022 Annex A as a third mapping.
- Store evidence file links and produce an audit evidence pack.
- Compare two assessments over time to show progress.

---
*Built with AI assistance (Claude) as a learning project; I reviewed, ran and tested all of the code.*
