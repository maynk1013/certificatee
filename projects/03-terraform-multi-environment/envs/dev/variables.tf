variable "aws_region" {
  type        = string
  description = "AWS region."
}

variable "project" {
  type        = string
  description = "Project tag."
}

variable "environment" {
  type        = string
  description = "Environment name."

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "owner" {
  type        = string
  description = "Owner tag."
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR."
}

variable "azs" {
  type        = list(string)
  description = "Availability zones."
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "Public subnet CIDRs."
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "Private subnet CIDRs."
}

variable "enable_nat_gateway" {
  type        = bool
  description = "NAT gateway toggle. Prod-style config may set this to true."
  default     = false
}

variable "create_compute" {
  type        = bool
  description = "Safety switch for instances. Committed configs keep this false."
  default     = false
}
