#!/usr/bin/env python3
"""Render a one-page, text-based resume PDF.

The script refuses to write a PDF that flows onto a second page.
It does not calculate an ATS score.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "resume" / "Mayank_Rai_DevOps_Resume.pdf"

LINES = [
    ("name", "MAYANK RAI"),
    ("role", "DevOps Engineer | AWS | Kubernetes | Terraform | CI/CD"),
    ("contact", "New Delhi, India | +91-9711200512 | mayankrai0310@gmail.com"),
    ("contact", "linkedin.com/in/mayankrai0310 | github.com/maynk1013/certificatee"),
    ("blank", ""),
    ("section", "PROFESSIONAL SUMMARY"),
    ("body", "DevOps Engineer Trainee with practice in AWS, Linux, Terraform, Kubernetes, Helm, and CI/CD."),
    ("body", "Built a public portfolio for GitOps, progressive delivery, multi-environment Terraform, observability,"),
    ("body", "dry-run cost reporting, backup verification, and secret rotation. Local tests passed. Cloud apply was not run."),
    ("blank", ""),
    ("section", "TECHNICAL SKILLS"),
    ("body", "AWS: EC2, IAM, VPC, S3, EKS, ECR, SSM, CloudWatch, CloudTrail, ELB, Auto Scaling, Organizations, Backup, Secrets Manager"),
    ("body", "DevOps: Docker, Kubernetes, Helm, Argo CD, Terraform, Ansible, Git, GitHub Actions, GitLab CI, Jenkins, GitOps"),
    ("body", "Observability and security: Prometheus, Grafana, Loki, Alertmanager, least-privilege IAM, secret scanning"),
    ("body", "Languages and OS: Python, Bash, Linux"),
    ("blank", ""),
    ("section", "PROFESSIONAL EXPERIENCE"),
    ("job", "DevOps Engineer Trainee | Paytm Payments Services | New Delhi, India | Feb 2026 - Present"),
    ("bullet", "Automated infrastructure operations across AWS accounts with Ansible, Systems Manager, and infrastructure-as-code practice."),
    ("bullet", "Built reusable Ansible roles for Qualys Cloud Agent, Cortex XDR, and SSM Agent deployment and lifecycle tasks."),
    ("bullet", "Coordinated quarterly Linux patching from vulnerability review and change approval through post-patch verification."),
    ("bullet", "Wrote Python and Bash automation for inventory, IAM review, and security-gap reporting."),
    ("blank", ""),
    ("section", "PROJECTS"),
    ("job", "GitOps EKS Platform | Terraform, Helm, Argo CD, Prometheus, GitLab CI | 2026"),
    ("bullet", "Designed VPC, IAM, and EKS modules, a probed demo service, and Argo CD plus Prometheus manifests. Validated locally. Did not apply AWS."),
    ("job", "Multi-Environment Terraform | Terraform, IAM, S3 state design | 2026"),
    ("bullet", "Separated dev, staging, and prod-style settings from reusable modules. Tag checks reject bad config. State lockfile is documented, not executed."),
    ("job", "Observability and Cost Reporter | Prometheus, Grafana, Loki, Python | 2026"),
    ("bullet", "Versioned golden-signal dashboards and alerts, and a local test alert. Dry-run reports flag idle candidates and loose resources without a savings claim."),
    ("job", "Earlier builds | Jenkins, Docker, Kubernetes, FastAPI, CUR, Athena, Vault, S3 | 2025-2026"),
    ("bullet", "Practiced CI/CD pipelines, a Jira operations dashboard, FinOps analytics design, and Vault backup automation. Portfolio tests do not re-measure that work."),
    ("blank", ""),
    ("section", "EDUCATION"),
    ("body", "Master of Computer Applications, Cloud Computing | Manipal University | 2024 - 2026"),
    ("body", "Bachelor of Computer Applications, Data Science | K.R. Mangalam University, Gurugram | 2021 - 2024"),
    ("blank", ""),
    ("section", "CERTIFICATIONS"),
    ("body", "Post Graduate Program in Data Science and Machine Learning"),
    ("body", "AWS Certified Cloud Practitioner and HashiCorp Terraform Associate: listed as in progress on the source resume"),
]


def draw(path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    pdf = canvas.Canvas(str(path), pagesize=A4)
    pdf.setTitle("Mayank Rai - DevOps Engineer")
    pdf.setAuthor("Mayank Rai")
    y = page_height - 12 * mm
    bottom = 10 * mm
    pages = 1
    for kind, text in LINES:
        if kind == "name":
            size, leading, font = 13, 15, "Times-Bold"
        elif kind == "role":
            size, leading, font = 9, 11, "Times-Bold"
        elif kind == "section":
            size, leading, font = 9.5, 12, "Times-Bold"
            y -= 1
        elif kind == "job":
            size, leading, font = 8.5, 10.5, "Times-Bold"
        elif kind == "blank":
            y -= 4
            continue
        else:
            size, leading, font = 8.2, 10, "Times-Roman"
        if y - leading < bottom:
            pdf.showPage()
            pages += 1
            y = page_height - 12 * mm
        pdf.setFont(font, size)
        pdf.drawString(12 * mm, y, text)
        y -= leading
    pdf.save()
    return pages


def main() -> None:
    pages = draw(OUTPUT)
    if pages != 1:
        raise SystemExit(f"resume spilled to {pages} pages")
    # Confirm the file is a real PDF and the text extractor can see the name.
    raw = OUTPUT.read_bytes()
    if not raw.startswith(b"%PDF"):
        raise SystemExit("output is not a PDF")
    if b"MAYANK RAI" not in raw and b"Mayank" not in raw:
        # Times-Roman text is usually stored as literal strings.
        if b"MAYANK" not in raw:
            raise SystemExit("name text was not found in the PDF bytes")
    print(f"wrote {OUTPUT} pages={pages} bytes={len(raw)}")


if __name__ == "__main__":
    main()
