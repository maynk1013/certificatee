# Portfolio roadmap

Recommended order is the folder order. Later projects reuse the same demo service idea, but each folder still runs alone.

| Order | Project | Depends on | Effort if you rebuild it | Validation milestone |
| --- | --- | --- | --- | --- |
| 1 | GitOps EKS | Terraform, Helm, Python | 4 to 6 focused days | `pytest`, `helm lint`, `terraform validate` |
| 2 | Progressive delivery | Project 1 app contract | 2 to 3 days | Healthy and failed rollout logs from `rollout_lab` |
| 3 | Multi-environment Terraform | Terraform 1.10 or newer | 2 to 3 days | Three environments validate, bad fixture fails |
| 4 | Observability | Metrics from the demo app | 2 to 3 days | Local alert scenario writes `evidence/test-alert.log` |
| 5 | Cost reporter | Python, mocked AWS errors | 2 to 3 days | Sample report with null savings |
| 6 | Disaster recovery | Synthetic data | 2 days | Checksum restore drill |
| 7 | Secrets | Local file store | 2 days | Rotation rollback and log redaction |

These ranges are planning estimates for a beginner repeating the work. They are not measured times from a timesheet.

## Publishing

1. Run `scripts/validate-all.sh` from the repository root.
2. Read the root README and remove any sentence you cannot demonstrate.
3. Confirm `git status` does not show `.env`, `*.tfstate`, or a kubeconfig.
4. Push to the repository you intend to show. This portfolio's remote is `https://github.com/maynk1013/certificatee.git`.
5. Put the one-page PDF path in your resume only after you can explain every bullet.

Do not apply the Terraform roots to a cloud account as part of publishing.
