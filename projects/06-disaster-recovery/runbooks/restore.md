# Restore runbook

## Targets, not measurements

- RPO target: 24 hours
- RTO target: 4 hours
- Cross-region recovery: not configured and not tested

The only measured time in this repository is the local synthetic restore elapsed time in `evidence/local-restore-drill.json` after the unit test runs. That number is not an AWS RTO.

## Prerequisites

- The Git commit that contains the Kubernetes manifests
- A backup payload and `metadata.json` with a matching sha256
- Approval before any AWS restore, overwrite, or delete
- A disposable database or the synthetic `orders.json` file

## Local drill

From the repository root, run the project 6 tests. The test copies `fixtures/app-data/orders.json`, writes metadata, corrupts the restore target, copies the backup back, and checks the checksum.

## AWS restore, only after approval

1. Confirm the recovery point in AWS Backup. Do not assume a recovery point exists; this repo did not create one.
2. Restore into a new resource name. Do not overwrite the only copy.
3. Run the application read-only check against the restored data.
4. If the check fails, keep the original resource and discard the failed restore.
5. Record the wall-clock time yourself. Do not copy the local drill time into an AWS RTO claim.

## Rollback

If a restored resource is wrong, stop using it and return the application config to the previous Git commit. Deleting the original resource is out of scope for this drill.
