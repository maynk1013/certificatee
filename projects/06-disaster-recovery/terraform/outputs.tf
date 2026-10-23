output "backup_plan_id" {
  description = "Backup plan ID when resources are created."
  value       = try(aws_backup_plan.daily[0].id, null)
}

output "cross_region_enabled" {
  description = "Whether a cross-region copy action is in the plan."
  value       = var.enable_cross_region_copy
}
