variable "name" {
  description = "EKS cluster name."
  type        = string
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version. Confirm AWS support before any apply."
  type        = string
}

variable "subnet_ids" {
  description = "Private subnet IDs for the control plane and nodes."
  type        = list(string)
}

variable "cluster_role_arn" {
  description = "IAM role ARN for the EKS control plane."
  type        = string
}

variable "cluster_role_name" {
  description = "IAM role name for the EKS control plane."
  type        = string
}

variable "node_role_arn" {
  description = "IAM role ARN for worker nodes."
  type        = string
}

variable "node_role_name" {
  description = "IAM role name for worker nodes."
  type        = string
}

variable "endpoint_public_access" {
  description = "Whether the Kubernetes API is reachable from the internet."
  type        = bool
  default     = false
}

variable "public_access_cidrs" {
  description = "CIDRs allowed to reach a public API endpoint."
  type        = list(string)
  default     = []
}

variable "instance_types" {
  description = "Instance types for the managed node group."
  type        = list(string)
  default     = ["t3.small"]
}

variable "desired_size" {
  description = "Desired node count."
  type        = number
  default     = 2
}

variable "min_size" {
  description = "Minimum node count."
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum node count."
  type        = number
  default     = 3
}

variable "tags" {
  description = "Tags applied to supported resources."
  type        = map(string)
  default     = {}
}
