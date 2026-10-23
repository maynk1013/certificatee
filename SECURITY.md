# Security

This repository is a public portfolio. It does not contain production credentials, and it should not receive any.

## Reporting

Open a GitHub issue for a bug in the sample code only if the issue does not include a secret, a customer name, or an internal hostname. For a leaked credential, rotate the credential first and do not paste it into the issue.

## Rules for changes

- Do not commit `.env`, AWS keys, private keys, kubeconfigs, or Terraform state.
- Do not run `terraform apply`, AWS Backup restore, or the cost remediation executor against a real account without explicit approval.
- Slack webhooks belong in a secret store or a mounted file, not in Git.
- The secret scanner in `tools/secret_scan.py` is a basic check. It can miss secrets. Review diffs as well.

## Scope

The sample applications are demos. They are not a production platform, and this repository does not claim a measured availability, cost saving, or recovery time.
