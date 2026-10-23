output "instance_profile_name" {
  description = "Instance profile name, or null when create is false."
  value       = try(aws_iam_instance_profile.instance[0].name, null)
}

output "role_arn" {
  description = "Instance role ARN, or null when create is false."
  value       = try(aws_iam_role.instance[0].arn, null)
}
