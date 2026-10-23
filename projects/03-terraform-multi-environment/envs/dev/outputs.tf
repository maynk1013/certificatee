output "vpc_id" {
  description = "VPC ID for this environment."
  value       = module.networking.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs."
  value       = module.networking.private_subnet_ids
}
