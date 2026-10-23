data "aws_iam_policy_document" "backup_assume" {
  count = var.create_backup_resources ? 1 : 0
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "backup" {
  count              = var.create_backup_resources ? 1 : 0
  name               = "${var.vault_name}-backup"
  assume_role_policy = data.aws_iam_policy_document.backup_assume[0].json
}

resource "aws_iam_role_policy_attachment" "backup" {
  count      = var.create_backup_resources ? 1 : 0
  role       = aws_iam_role.backup[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_backup_vault" "this" {
  count = var.create_backup_resources ? 1 : 0
  name  = var.vault_name
}

resource "aws_backup_plan" "daily" {
  count = var.create_backup_resources ? 1 : 0
  name  = "${var.vault_name}-daily"

  rule {
    rule_name         = "daily-local-region"
    target_vault_name = aws_backup_vault.this[0].name
    schedule          = "cron(0 18 * * ? *)"

    lifecycle {
      delete_after = 35
    }

    dynamic "copy_action" {
      for_each = var.enable_cross_region_copy ? [1] : []
      content {
        destination_vault_arn = "arn:aws:backup:${var.aws_region}:000000000000:backup-vault:${var.vault_name}-dr"
        lifecycle {
          delete_after = 35
        }
      }
    }
  }
}
