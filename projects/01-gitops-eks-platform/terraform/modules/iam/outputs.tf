output "cluster_role_arn" {
  description = "IAM role ARN for the EKS control plane."
  value       = aws_iam_role.cluster.arn
}

output "cluster_role_name" {
  description = "IAM role name for the EKS control plane."
  value       = aws_iam_role.cluster.name
}

output "node_role_arn" {
  description = "IAM role ARN for the managed node group."
  value       = aws_iam_role.node.arn
}

output "node_role_name" {
  description = "IAM role name for the managed node group."
  value       = aws_iam_role.node.name
}
