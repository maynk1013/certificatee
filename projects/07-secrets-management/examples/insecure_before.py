"""Teaching example of the old pattern.

Do not copy this into an application. The function below is the pattern that
was removed: a secret value living in source code. The replacement is
`secrets_lab.app.DemoApp`, which receives a provider.
"""


def insecure_lookup() -> str:
    raise RuntimeError("hardcoded secret lookup is disabled; use FileSecretStore or AwsSecretsProvider")
