# Resume project entries

Use these only where the wording matches what you can demo. Numbers in brackets are placeholders you must measure yourself. Do not paste a placeholder into a resume as if it were a result.

## GitOps platform for Amazon EKS

Stack: Terraform, Amazon VPC, IAM, EKS, Docker, Helm, Argo CD, Prometheus, Grafana, GitLab CI.

Designed reusable Terraform modules for a private-endpoint EKS layout, a Helm chart with readiness and liveness probes, and Argo CD application manifests. Added Prometheus rules and a Grafana dashboard definition. Local checks were Terraform validate, Helm lint, and Python tests. An EKS cluster was not created from this repo.

## Multi-environment Terraform

Stack: Terraform 1.10+, S3 backend design, IAM, VPC, Auto Scaling configuration.

Separated dev, staging, and production-style settings from networking, IAM, and compute modules. Documented encrypted S3 state and Terraform's native S3 lockfile. Added a tag policy check and an intentionally invalid fixture that validation rejects. Compute creation stays off in the committed files. No environment was applied.

## Observability and dry-run cost reporting

Stack: Prometheus rules, Grafana dashboards, Loki and Alloy values, Python.

Versioned golden-signal panels and example alerts for error ratio, average latency, and CPU pressure. A local lab queries sample metrics and logs and writes a reproducible test alert. The cost tool reports idle-instance candidates, unattached volumes, unattached Elastic IPs, and tag gaps from synthetic data, and it leaves savings empty unless a price catalog is supplied.

## What not to write

- Do not write a downtime percentage for project 2. The cluster rollout was not run.
- Do not write a monthly saving for project 5. The sample report does not contain one.
- Do not write an achieved RTO. The policy stores a target, and the drill stores a local elapsed time only.
