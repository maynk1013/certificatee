output "cluster_name" {
  description = "EKS cluster name."
  value       = aws_eks_cluster.this.name
}

output "cluster_endpoint" {
  description = "Kubernetes API endpoint."
  value       = aws_eks_cluster.this.endpoint
}

output "cluster_certificate_authority" {
  description = "Base64 cluster CA data."
  value       = aws_eks_cluster.this.certificate_authority[0].data
  sensitive   = true
}

output "node_group_name" {
  description = "Managed node group name."
  value       = aws_eks_node_group.default.node_group_name
}

output "secrets_kms_key_arn" {
  description = "KMS key used for Kubernetes secret encryption."
  value       = aws_kms_key.secrets.arn
}
