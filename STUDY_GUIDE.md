# Study guide: GRC Gap Assessor

Read this before any interview where you mention the project. Run the tool yourself first, then go through each section.

## 1. Explain it in 30 seconds

> "It's a Python CLI that does a cybersecurity gap assessment against Saudi NCA ECC and EU NIS2 together.
> You answer 27 control questions once. Each control is mapped to ECC subdomains and NIS2 Article 21(2) measures.
> The tool calculates weighted compliance scores per domain and ranks every gap by risk to produce a remediation roadmap.
> It does what a GRC consultant does before an audit, so the client doesn't answer the same question twice."

## 2. Key concepts you must know

| Term | Simple meaning |
|---|---|
| GRC | Governance, Risk and Compliance: the policy, risk and audit side of security |
| Gap assessment | Compare "what you have" with "what the standard requires" and list the differences |
| NCA ECC | Saudi baseline controls from the National Cybersecurity Authority. 5 domains: Governance, Defense, Resilience, Third-party & Cloud, ICS |
| NIS2 | EU directive (2022/2555) that member states turned into national law from Oct 2024. Article 21 lists 10 minimum measures; Article 23 sets incident reporting deadlines (early warning within 24h, notification within 72h, final report within 1 month) |
| Control mapping | One control can satisfy several frameworks (e.g. MFA → ECC 2-2 and NIS2 21(2)(j)) |
| Risk = likelihood × impact | Here simplified to weight (impact) × size of the gap |

## 3. Walk through the code

1. `controls.json` holds the data. Each control has an id, a question, ECC codes, NIS2 letters, a weight and a remediation.
2. `load_controls()` checks the data is valid: no duplicate ids, weight 1 to 3, and every ECC/NIS2 code exists in `frameworks.py`.
3. `load_answers()` reads the CSV and rejects unknown controls, invalid statuses, duplicates and unanswered controls. Ask yourself: *why reject unanswered controls instead of treating them as missing?* Answer: silent defaults hide mistakes. An auditor wants every control answered on purpose.
4. `assess()` loops over each answer:
   - It skips `na`, turns the status into a score and adds `(weight, score)` to every subdomain, domain and NIS2 measure the control maps to.
   - When score < 1, it creates a `Gap` with `risk = weight × (1 − score)`.
   - Gaps are sorted by highest risk first.
5. `report.py` turns the `Result` into Markdown and HTML. `html.escape` is used so user notes can't inject HTML (prevents XSS in the report).

## 4. Likely interview questions

- **Why weighted scores?** Missing MFA is far worse than missing a mobile policy, and a plain average would treat them the same.
- **Weakness of your scoring?** "Partial" = 0.5 is subjective, and self-assessment depends on honest answers. In a real engagement you'd verify evidence (screenshots, configs, interviews).
- **How would you extend it?** Add ISO 27001 Annex A mapping, attach evidence, compare over time, and pull some answers automatically (e.g. check MFA status via an API).
- **Difference between ECC and NIS2?** ECC is a Saudi control list with specific controls. NIS2 is an EU directive that sets outcome-level measures and leaves the details to national laws.
- **What's `--fail-under` for?** It lets the tool act as a gate in CI/CD, the "compliance as code" idea.

## 5. Practise before the interview

- Change three answers in `examples/acme_logistics.csv` and predict the new score before you run it.
- Add a new control (e.g. "Security of DNS") with a mapping, then run the tests.
- Read the official NIS2 Article 21 text on EUR-Lex and the NCA ECC document, and note where my summaries simplify.
