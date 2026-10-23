output "security_group_id" {
  description = "Security group ID when compute is created."
  value       = try(aws_security_group.instance[0].id, null)
}

output "autoscaling_group_name" {
  description = "Auto Scaling group name when compute is created."
  value       = try(aws_autoscaling_group.this[0].name, null)
}
