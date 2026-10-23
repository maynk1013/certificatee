resource "aws_secretsmanager_secret" "app" {
  count       = var.create_secret_resource ? 1 : 0
  name        = var.secret_name
  description = "Demo application secret. Put the value with the AWS CLI, not with Terraform."
}

data "aws_iam_policy_document" "read" {
  statement {
    sid     = "ReadOneSecret"
    actions = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:000000000000:secret:${var.secret_name}*",
    ]
  }
}
