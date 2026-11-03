"""Command line interface.

  python -m grc_gap template answers.csv
  python -m grc_gap assess answers.csv --org "Acme" --out report.md --html report.html
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .assessor import AssessmentError, assess, load_answers, load_controls, write_template
from .report import to_html, to_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="grc_gap",
        description="Cybersecurity gap assessment against Saudi NCA ECC and EU NIS2.",
    )
    parser.add_argument("--controls", type=Path, help="custom controls.json (optional)")
    sub = parser.add_subparsers(dest="command", required=True)

    t = sub.add_parser("template", help="write a blank answer sheet (CSV)")
    t.add_argument("output", type=Path)

    a = sub.add_parser("assess", help="score a filled-in answer sheet")
    a.add_argument("answers", type=Path)
    a.add_argument("--org", default="Organisation", help="organisation name for the report")
    a.add_argument("--out", type=Path, help="write Markdown report here (default: print it)")
    a.add_argument("--html", type=Path, help="also write an HTML report here")
    a.add_argument("--fail-under", type=float, metavar="PCT",
                   help="exit with code 2 if any framework scores below this percentage")

    args = parser.parse_args(argv)
    try:
        controls = load_controls(args.controls) if args.controls else load_controls()
        if args.command == "template":
            write_template(args.output, controls)
            print(f"Wrote blank answer sheet with {len(controls)} controls to {args.output}")
            print("Fill in 'status' with: implemented, partial, missing or na")
            return 0

        answers = load_answers(args.answers, controls)
        result = assess(controls, answers, args.org)
    except (AssessmentError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    md = to_markdown(result)
    if args.out:
        args.out.write_text(md, encoding="utf-8")
        print(f"Markdown report: {args.out}")
    else:
        print(md)
    if args.html:
        args.html.write_text(to_html(result), encoding="utf-8")
        print(f"HTML report: {args.html}")

    for name, score in result.overall.items():
        print(f"{name}: {round(score * 100)}%", file=sys.stderr)
    if args.fail_under is not None and any(s * 100 < args.fail_under for s in result.overall.values()):
        return 2
    return 0
