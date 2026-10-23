# ATS-style bullets

These bullets describe the portfolio and the work already listed on the source resume in Downloads. Bracketed text is a placeholder. Measure it yourself before you publish that sentence.

## Portfolio

- Designed Terraform modules for VPC, IAM, and EKS, and validated them locally with `terraform fmt` and `terraform validate` without creating cloud resources.
- Packaged a demo web service in Helm with readiness probes, liveness probes, resource requests and limits, and a rolling update setting of `maxUnavailable: 0`.
- Wrote Argo CD Application manifests so the desired state stays in Git, and documented the sync path without claiming a live cluster sync.
- Modeled canary and blue-green decisions in Python, including a failed release that returns traffic weight to the previous version.
- Separated dev, staging, and production-style Terraform settings from reusable modules and added a check that rejects missing owner tags.
- Built a dry-run Python reporter for idle EC2 candidates, unattached EBS volumes, unattached Elastic IPs, and inconsistent tags.
- Versioned Prometheus rules and Grafana dashboard JSON, and demonstrated a local test alert from a fixed sample.
- Automated a synthetic backup checksum and restore drill, and documented RPO and RTO as targets rather than measured cloud results.
- Moved a demo application from a disabled hardcoded lookup to a secret provider, and tested that the secret value is absent from logs.

## Experience already on the source resume

Keep these only if you are comfortable defending them in an interview. This portfolio did not re-run that work.

- Automated infrastructure operations across AWS accounts using Ansible, SSM, and infrastructure-as-code practices.
- Implemented Ansible roles for Qualys Cloud Agent, Cortex XDR, and SSM Agent deployment and lifecycle tasks.
- Coordinated quarterly Linux patching through vulnerability review, change approval, deployment, and post-patch verification.
- Wrote Python and Bash checks for IAM review, inventory, and security-gap reporting.

## Placeholders you must replace or delete

- Reduced a named manual task from [previous minutes] to [current minutes] after timing both ways.
- Raised patch completion for [scope] from [before] to [after] during [quarter].
- Cut dashboard refresh time from [before] to [after] on [data set].

If you do not have the measurement, delete the bullet.
