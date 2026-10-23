variable "name" {
  description = "Short name prefix for VPC resources."
  type        = string
}

variable "cidr" {
  description = "IPv4 CIDR for the VPC."
  type        = string
}

variable "azs" {
  description = "Availability zones. Provide at least two."
  type        = list(string)

  validation {
    condition     = length(var.azs) >= 2
    error_message = "Provide at least two availability zones."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDRs for public subnets, one per AZ."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDRs for private subnets, one per AZ."
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Create a single NAT gateway for private subnet egress."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to supported resources."
  type        = map(string)
  default     = {}
}
