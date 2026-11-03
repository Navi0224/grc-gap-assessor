"""Reference names for the two frameworks this tool maps controls to.

The wording is a short summary in my own words, not the official text. Always
check the official documents before using this for real compliance work:
  - Saudi NCA Essential Cybersecurity Controls (ECC): https://nca.gov.sa
  - EU NIS2 Directive (EU) 2022/2555, Article 21(2): https://eur-lex.europa.eu
"""

# ECC subdomains, grouped into the 5 main ECC domains.
# Numbering follows the ECC subdomain structure (domain-subdomain).
ECC_DOMAINS = {
    "1": "Cybersecurity Governance",
    "2": "Cybersecurity Defense",
    "3": "Cybersecurity Resilience",
    "4": "Third-Party and Cloud Computing Cybersecurity",
    "5": "Industrial Control Systems Cybersecurity",
}

ECC_SUBDOMAINS = {
    "1-1": "Cybersecurity Strategy",
    "1-2": "Cybersecurity Management",
    "1-3": "Cybersecurity Policies and Procedures",
    "1-4": "Cybersecurity Roles and Responsibilities",
    "1-5": "Cybersecurity Risk Management",
    "1-6": "Cybersecurity in IT Projects",
    "1-7": "Compliance with Cybersecurity Standards, Laws and Regulations",
    "1-8": "Periodical Cybersecurity Review and Audit",
    "1-9": "Cybersecurity in Human Resources",
    "1-10": "Cybersecurity Awareness and Training",
    "2-1": "Asset Management",
    "2-2": "Identity and Access Management",
    "2-3": "Information System and Processing Facilities Protection",
    "2-4": "Email Protection",
    "2-5": "Networks Security Management",
    "2-6": "Mobile Devices Security",
    "2-7": "Data and Information Protection",
    "2-8": "Cryptography",
    "2-9": "Backup and Recovery Management",
    "2-10": "Vulnerabilities Management",
    "2-11": "Penetration Testing",
    "2-12": "Event Logs and Monitoring Management",
    "2-13": "Incident and Threat Management",
    "2-14": "Physical Security",
    "2-15": "Web Application Security",
    "3-1": "Cybersecurity Resilience Aspects of Business Continuity Management",
    "4-1": "Third-Party Cybersecurity",
    "4-2": "Cloud Computing and Hosting Cybersecurity",
}

# NIS2 Article 21(2): the ten minimum risk-management measures, (a) to (j).
NIS2_MEASURES = {
    "a": "Risk analysis and information system security policies",
    "b": "Incident handling",
    "c": "Business continuity, backup management, disaster recovery, crisis management",
    "d": "Supply chain security",
    "e": "Security in acquisition, development and maintenance, incl. vulnerability handling",
    "f": "Policies to assess the effectiveness of security measures",
    "g": "Basic cyber hygiene and cybersecurity training",
    "h": "Cryptography and encryption",
    "i": "Human resources security, access control and asset management",
    "j": "Multi-factor authentication and secured communications",
}


def ecc_label(code: str) -> str:
    return f"ECC {code} {ECC_SUBDOMAINS.get(code, '(unknown)')}"


def nis2_label(letter: str) -> str:
    return f"NIS2 21(2)({letter}) {NIS2_MEASURES.get(letter, '(unknown)')}"
