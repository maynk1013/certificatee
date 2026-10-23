# Project 5 — AWS cost report tool

This is a dry-run Python tool. It reads a snapshot, finds idle-instance candidates, unattached volumes, unattached Elastic IPs, and tag problems, then writes CSV and JSON. The default command does not stop, delete, detach, or modify anything.

The sample report uses synthetic inventory. Savings fields are null unless you pass `--use-supplied-prices`. A supplied price is still an estimate, not a Cost Explorer result, and not a measured saving.

## Samajh lo, Hinglish mein

Tool ek inspector hai, cleaner nahi. Pehle woh list banata hai: yeh instance ka CPU bahut kam dikhta hai, yeh disk kisi EC2 se attached nahi hai, yeh Elastic IP khali padi hai, ya tags incomplete hain. Report mein reason aur recommended action hota hai.

Dry-run default hai. Matlab sirf report. Stop karna alag command hai, aur woh bhi tabhi jab code mein allow switch aur approved resource id dono hon. Sample path AWS ko call nahi karta.

Agar price catalog nahi diya, to savings column khali rehta hai. Main khud se monthly saving ka number nahi likhta.

## Local test

From the repository root:

```bash
PYTHONPATH=projects/05-aws-cost-optimizer/src python3 -m pytest projects/05-aws-cost-optimizer/tests -q
PYTHONPATH=projects/05-aws-cost-optimizer/src python3 -m costopt \
  --input projects/05-aws-cost-optimizer/sample_data/inventory.json \
  --output /tmp/costopt-report
```

The unit test also writes `evidence/sample-report.json`.

## Optional live mode

Live AWS calls are not implemented as the default CLI. `aws_client.call_with_retry` is the small wrapper a later live collector can use. It was tested with mocked `ClientError` responses for access denied and throttling. No AWS API was called.

Lambda `handler` returns a dry-run payload. EventBridge was not created.

## IAM

`iam/read-only-policy.json` allows describe and metric reads. `ec2:Describe*` and Cost Explorer actions require `Resource: "*"` in IAM. The remediation example is a separate file and is not attached by any Terraform in this project. It allows `ec2:StopInstances` only when the resource tag `CostOptAllowStop` is `true`.

## Troubleshooting

| Result | Meaning |
| --- | --- |
| `insufficient data` | CPU was missing. The instance is not called idle. |
| Savings is null | No price catalog was supplied. |
| `RemediationRefused` | The allow switch or the approved id list was missing. |
| `AccessDenied` | The wrapper returns `AwsCallError` and does not invent a finding. |

## Limitations

- Lookback is represented by the snapshot's CPU average. The sample does not query CloudWatch.
- No monthly savings number is claimed for the sample inventory.
- Slack is optional and untested against a real webhook. The empty webhook test checks that no request is made.
