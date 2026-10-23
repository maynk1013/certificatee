output "cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "vpc_id" {
  description = "VPC ID."
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "Private subnet IDs."
  value       = module.vpc.private_subnet_ids
}

output "cluster_endpoint" {
  description = "Kubernetes API endpoint. Empty until a real apply."
  value       = module.eks.cluster_endpoint
}
