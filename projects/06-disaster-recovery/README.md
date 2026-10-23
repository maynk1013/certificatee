# Project 6 — Backup verification and restore drill

Kubernetes manifests and the backup policy are in Git. A Python drill checks synthetic application data with sha256 metadata and restores it after a deliberate corruption. Terraform contains an AWS Backup vault and a daily plan, both gated by `create_backup_resources = false`.

Nothing was created in AWS. Cross-region copy is false and was not tested.

## Samajh lo, Hinglish mein

Backup ka matlab copy banana. Verification ka matlab copy ko trust karne se pehle checksum milana. Restore drill ka matlab copy ko wapas rakh kar dekhna ki data same hai.

Git khud Kubernetes YAML ka backup hai. Database ya EBS ke liye AWS Backup tab use hoga jab tum approve karo. Abhi woh resources count false hain, isliye `terraform apply` bhi unhe nahi banayega jab tak variable change na ho.

RPO target 24 hours hai: kitna data loss accept hai. RTO target 4 hours hai: kitni der mein service wapas chahiye. Yeh targets hain. Inhe measured result mat bolo. Local drill ki clock alag file mein likhi jaati hai.

## Local test

```bash
python3 -m pytest projects/06-disaster-recovery/backup_lab/tests -q
terraform -chdir=projects/06-disaster-recovery/terraform init -backend=false
terraform -chdir=projects/06-disaster-recovery/terraform validate
```

## Checklist

- Metadata file exists
- sha256 matches the payload
- Retention is at least 7 days
- Restored file matches the backup hash
- Cross-region flag is false
- AWS restore was not run

## Teardown

There is no cloud resource to delete from the tested path. If you later set `create_backup_resources` to true and apply, destroy only after approval:

```bash
terraform -chdir=projects/06-disaster-recovery/terraform destroy
```

## Limitations

- No RDS instance and no EKS backup were created.
- AWS Backup recovery points were not listed.
- The AWS managed backup policy is broad. It is attached only when the gated resources are created.
