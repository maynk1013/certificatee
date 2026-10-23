# Project 7 — Secrets management and rotation

The demo application reads a secret through a provider. The local provider is a JSON file with versions. The AWS provider calls `GetSecretValue` and is tested with a fake client. Logs and the rotation evidence file contain status fields, not the secret value.

The old hardcoded lookup now raises an error that tells you to use a provider. Terraform can create an empty secret resource, and it does not set a secret version. Kubernetes reads the value with `secretKeyRef`.

## Samajh lo, Hinglish mein

Secret ko code mein likhna matlab password ko diary ke cover par chipka dena. Sahi tareeka: secret Secrets Manager ya local test store mein rahe, application sirf uska reference rakhe.

Rotation ka matlab naya value likhna, phir check karna ki application use padh pa rahi hai. Agar check fail ho, pointer purane version par wapas aata hai. Purana value delete nahi hota, taaki recovery ho sake.

IAM role ya Kubernetes service account annotation batata hai kaun sa pod secret padh sakta hai. Account ID `000000000000` placeholder hai.

## Local test

```bash
python3 -m pytest projects/07-secrets-management/secrets_lab/tests -q
terraform -chdir=projects/07-secrets-management/terraform init -backend=false
terraform -chdir=projects/07-secrets-management/terraform validate
python3 tools/secret_scan.py
```

## Failed rotation recovery

1. Read `evidence/rotation.json` or the command result. Status `rolled_back` means the current pointer is the previous version.
2. Confirm the application status endpoint reports `secret_present` and the log does not print the value.
3. If both versions are bad, put a new known test value with the file store or with `aws secretsmanager put-secret-value` after approval.
4. If AWS returns `AccessDeniedException`, fix the role. Do not paste the secret into a ticket or a pipeline log.
5. Revoke a leaked value by disabling the old version in Secrets Manager and rotating again. This revoke step was not executed against AWS.

## Audit and incident response

- CloudTrail should record `GetSecretValue`. This repo does not query CloudTrail.
- A leaked value in Git is handled by rotating the value, removing it from the current commit, and treating the old Git history as exposed.
- CI runs `tools/secret_scan.py`, which flags private-key blocks and `AKIA` followed by 16 letters or digits.

## Teardown

Local files can be deleted. AWS secret deletion requires approval and a recovery window. It was not run.

## Limitations

- HashiCorp Vault was not installed. The AWS provider is the implemented cloud path, and only the fake client was tested.
- The Kubernetes manifest was not applied.
- IRSA role ARN is a placeholder.
