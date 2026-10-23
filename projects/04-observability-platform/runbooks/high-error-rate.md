# High error rate

## Sample incident

The local scenario uses 10 successful samples and 10 error samples. The error ratio is 0.5. The example threshold is 0.05. The local evaluator emits `DemoWebHighErrorRate`.

This is not a record of a production incident.

## Checks

1. Read the latest application log lines and separate 4xx from 5xx.
2. Check whether a new image tag was reconciled.
3. Check readiness. A failing `/readyz` should stop traffic before this alert if the rollout is configured.
4. If the error flag `FAIL_API` is set, that is a deliberate test failure.

## Mitigation

Roll back the application manifest in Git and let the GitOps controller reconcile. Do not delete the namespace as a first step.
