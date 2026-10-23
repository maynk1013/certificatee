output "secret_arn" {
  description = "Secret ARN when the resource is created. The secret value is not an output."
  value       = try(aws_secretsmanager_secret.app[0].arn, null)
}

output "read_policy_json" {
  description = "Least-privilege read policy for one secret name."
  value       = data.aws_iam_policy_document.read.json
}
