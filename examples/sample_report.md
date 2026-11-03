# Cybersecurity Gap Assessment: Acme Logistics (fictional)

Date: 2026-11-03  
Frameworks: Saudi NCA Essential Cybersecurity Controls (ECC) and EU NIS2 Article 21(2)

> Self-assessment tool for learning and pre-audit preparation. It is not an official
> certification. Check results against the official NCA ECC and NIS2 texts.

## Summary

| Framework | Score | Rating |
|---|---|---|
| NCA ECC | 38% | Weak |
| NIS2 | 38% | Weak |

Controls answered: 27 (implemented 5, partial 12, missing 9, not applicable 1)

Gaps found: 21 (High 9, Medium 12, Low 0)

## NCA ECC by domain

| Domain | Score |
|---|---|
| 1. Cybersecurity Governance | 45% |
| 2. Cybersecurity Defense | 41% |
| 3. Cybersecurity Resilience | 0% |
| 4. Third-Party and Cloud Computing Cybersecurity | 25% |

## NCA ECC by subdomain

| Subdomain | Score |
|---|---|
| 1-1 Cybersecurity Strategy | 50% |
| 1-2 Cybersecurity Management | 100% |
| 1-3 Cybersecurity Policies and Procedures | 50% |
| 1-4 Cybersecurity Roles and Responsibilities | 100% |
| 1-5 Cybersecurity Risk Management | 0% |
| 1-6 Cybersecurity in IT Projects | 50% |
| 1-7 Compliance with Cybersecurity Standards, Laws and Regulations | 0% |
| 1-8 Periodical Cybersecurity Review and Audit | 0% |
| 1-9 Cybersecurity in Human Resources | 100% |
| 1-10 Cybersecurity Awareness and Training | 50% |
| 2-1 Asset Management | 50% |
| 2-2 Identity and Access Management | 25% |
| 2-3 Information System and Processing Facilities Protection | 100% |
| 2-4 Email Protection | 50% |
| 2-5 Networks Security Management | 50% |
| 2-7 Data and Information Protection | 0% |
| 2-8 Cryptography | 100% |
| 2-9 Backup and Recovery Management | 50% |
| 2-10 Vulnerabilities Management | 0% |
| 2-11 Penetration Testing | 0% |
| 2-12 Event Logs and Monitoring Management | 50% |
| 2-13 Incident and Threat Management | 0% |
| 2-14 Physical Security | 100% |
| 2-15 Web Application Security | 50% |
| 3-1 Cybersecurity Resilience Aspects of Business Continuity Management | 0% |
| 4-1 Third-Party Cybersecurity | 0% |
| 4-2 Cloud Computing and Hosting Cybersecurity | 50% |

## NIS2 Article 21(2) measures

| Measure | Score |
|---|---|
| (a) Risk analysis and information system security policies | 36% |
| (b) Incident handling | 25% |
| (c) Business continuity, backup management, disaster recovery, crisis management | 25% |
| (d) Supply chain security | 25% |
| (e) Security in acquisition, development and maintenance, incl. vulnerability handling | 50% |
| (f) Policies to assess the effectiveness of security measures | 17% |
| (g) Basic cyber hygiene and cybersecurity training | 71% |
| (h) Cryptography and encryption | 100% |
| (i) Human resources security, access control and asset management | 44% |
| (j) Multi-factor authentication and secured communications | 50% |

## Remediation roadmap (highest risk first)

### 1. [High] C04 Risk management (missing)

- Risk score: 3 (weight 3)
- Maps to: ECC 1-5 Cybersecurity Risk Management, NIS2 21(2)(a) Risk analysis and information system security policies
- Current state: No formal risk register
- Recommended action: Adopt a method (e.g. ISO 27005 style), keep a risk register with owners and treatment plans, and reassess at least yearly or after major changes.

### 2. [High] C11 Least privilege and access reviews (missing)

- Risk score: 3 (weight 3)
- Maps to: ECC 2-2 Identity and Access Management, NIS2 21(2)(i) Human resources security, access control and asset management
- Current state: Several staff have standing domain admin rights
- Recommended action: Remove standing admin rights, separate admin accounts, and run quarterly access reviews for critical systems.

### 3. [High] C19 Vulnerability management (missing)

- Risk score: 3 (weight 3)
- Maps to: ECC 2-10 Vulnerabilities Management, NIS2 21(2)(e) Security in acquisition, development and maintenance, incl. vulnerability handling
- Current state: No regular vulnerability scanning
- Recommended action: Scan at least monthly, prioritise by CVSS, exploitability and asset criticality, and track fixes against SLAs.

### 4. [High] C22 Incident response (missing)

- Risk score: 3 (weight 3)
- Maps to: ECC 2-13 Incident and Threat Management, NIS2 21(2)(b) Incident handling
- Current state: No incident response plan
- Recommended action: Write an IR plan with roles and playbooks, run a tabletop exercise yearly, and document regulator reporting duties (NIS2: early warning within 24h, notification within 72h).

### 5. [High] C25 Business continuity (missing)

- Risk score: 3 (weight 3)
- Maps to: ECC 3-1 Cybersecurity Resilience Aspects of Business Continuity Management, NIS2 21(2)(c) Business continuity, backup management, disaster recovery, crisis management
- Current state: BCP does not cover cyber scenarios
- Recommended action: Add cyber scenarios to BCP/DR, define recovery time objectives and test the plan yearly.

### 6. [High] C06 Compliance and audit (missing)

- Risk score: 2 (weight 2)
- Maps to: ECC 1-7 Compliance with Cybersecurity Standards, Laws and Regulations, ECC 1-8 Periodical Cybersecurity Review and Audit, NIS2 21(2)(f) Policies to assess the effectiveness of security measures
- Current state: No internal audit of security controls
- Recommended action: Plan a yearly control review, track findings to closure and report results to management.

### 7. [High] C16 Data classification and protection (missing)

- Risk score: 2 (weight 2)
- Maps to: ECC 2-7 Data and Information Protection, NIS2 21(2)(a) Risk analysis and information system security policies
- Current state: No data classification scheme
- Recommended action: Define a classification scheme, label key data stores and apply handling rules (access, sharing, DLP) per class.

### 8. [High] C20 Penetration testing (missing)

- Risk score: 2 (weight 2)
- Maps to: ECC 2-11 Penetration Testing, NIS2 21(2)(f) Policies to assess the effectiveness of security measures
- Current state: Never pen tested
- Recommended action: Commission a pen test of external and critical systems at least yearly and after major changes; retest fixes.

### 9. [High] C26 Third-party security (missing)

- Risk score: 2 (weight 2)
- Maps to: ECC 4-1 Third-Party Cybersecurity, NIS2 21(2)(d) Supply chain security
- Current state: No supplier security assessments
- Recommended action: Tier suppliers by risk, send security questionnaires to critical ones and add security and breach-notification clauses to contracts.

### 10. [Medium] C09 Asset inventory (partial)

- Risk score: 1.5 (weight 3)
- Maps to: ECC 2-1 Asset Management, NIS2 21(2)(i) Human resources security, access control and asset management
- Current state: Hardware listed; software and owners missing
- Recommended action: Build an asset inventory (CMDB or spreadsheet to start), assign owners and classify assets by criticality.

### 11. [Medium] C10 Multi-factor authentication (partial)

- Risk score: 1.5 (weight 3)
- Maps to: ECC 2-2 Identity and Access Management, NIS2 21(2)(j) Multi-factor authentication and secured communications
- Current state: MFA on email only; VPN and admin accounts not covered
- Recommended action: Enforce MFA starting with admins, VPN and email; prefer phishing-resistant methods (FIDO2/authenticator apps over SMS).

### 12. [Medium] C18 Backup and recovery (partial)

- Risk score: 1.5 (weight 3)
- Maps to: ECC 2-9 Backup and Recovery Management, NIS2 21(2)(c) Business continuity, backup management, disaster recovery, crisis management
- Current state: Nightly backups but no offline copy and no restore test
- Recommended action: Follow 3-2-1 backups with one offline/immutable copy and test restores at least quarterly.

### 13. [Medium] C21 Logging and monitoring (partial)

- Risk score: 1.5 (weight 3)
- Maps to: ECC 2-12 Event Logs and Monitoring Management, NIS2 21(2)(b) Incident handling
- Current state: Logs collected but nobody reviews alerts
- Recommended action: Forward logs from critical systems to a SIEM, define retention, and build alert use cases with someone responsible for triage.

### 14. [Medium] C01 Cybersecurity strategy (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 1-1 Cybersecurity Strategy, NIS2 21(2)(a) Risk analysis and information system security policies
- Current state: Strategy drafted but not yet approved by the board
- Recommended action: Write a 2-3 year strategy aligned to business goals, get it signed off by leadership and review it yearly.

### 15. [Medium] C03 Security policies (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 1-3 Cybersecurity Policies and Procedures, NIS2 21(2)(a) Risk analysis and information system security policies, NIS2 21(2)(f) Policies to assess the effectiveness of security measures
- Current state: Policies exist but last reviewed in 2023
- Recommended action: Create a policy set (acceptable use, access control, incident response, etc.), get approval, publish it and review at least yearly.

### 16. [Medium] C05 Security in IT projects (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 1-6 Cybersecurity in IT Projects, NIS2 21(2)(e) Security in acquisition, development and maintenance, incl. vulnerability handling
- Current state: Security review only for large projects
- Recommended action: Add security checkpoints to the project lifecycle: requirements, design review, code scanning and a pre-release security test.

### 17. [Medium] C08 Awareness and training (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 1-10 Cybersecurity Awareness and Training, NIS2 21(2)(g) Basic cyber hygiene and cybersecurity training
- Current state: Yearly training only; no phishing simulations
- Recommended action: Run onboarding and yearly training, plus quarterly phishing simulations; track completion rates.

### 18. [Medium] C13 Email protection (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 2-4 Email Protection, NIS2 21(2)(g) Basic cyber hygiene and cybersecurity training
- Current state: SPF and DKIM set; DMARC at p=none
- Recommended action: Enable advanced email filtering and publish SPF, DKIM and a DMARC policy, moving towards p=reject.

### 19. [Medium] C14 Network security (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 2-5 Networks Security Management, NIS2 21(2)(e) Security in acquisition, development and maintenance, incl. vulnerability handling
- Current state: Flat office network; servers in separate VLAN
- Recommended action: Segment networks by trust level, default-deny between zones and review firewall rules every 6 months.

### 20. [Medium] C24 Web application security (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 2-15 Web Application Security, NIS2 21(2)(e) Security in acquisition, development and maintenance, incl. vulnerability handling
- Current state: Public site behind CDN; no WAF; never tested against OWASP Top 10
- Recommended action: Put a WAF in front of public apps, enforce HTTPS and security headers, and test against the OWASP Top 10 before release.

### 21. [Medium] C27 Cloud security (partial)

- Risk score: 1 (weight 2)
- Maps to: ECC 4-2 Cloud Computing and Hosting Cybersecurity, NIS2 21(2)(d) Supply chain security
- Current state: Data hosted in-region; CIS benchmark review not done
- Recommended action: Review cloud configs against CIS benchmarks, enable cloud logging and confirm data residency rules are met.
