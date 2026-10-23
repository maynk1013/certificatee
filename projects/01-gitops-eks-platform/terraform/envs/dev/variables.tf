variable "aws_region" {
  description = "AWS region for this environment."
  type        = string
}

variable "project" {
  description = "Project tag."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "owner" {
  description = "Owner tag. Use a team name, not a personal secret."
  type        = string
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
}

variable "kubernetes_version" {
  description = "EKS version to request. Confirm support before apply."
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR."
  type        = string
}

variable "azs" {
  description = "Availability zones."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDRs."
  type        = list(string)
}

variable "endpoint_public_access" {
  description = "Keep false unless you also restrict public_access_cidrs."
  type        = bool
  default     = false
}

variable "public_access_cidrs" {
  description = "CIDRs for a public API endpoint."
  type        = list(string)
  default     = []
}
