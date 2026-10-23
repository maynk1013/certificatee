variable "name" {
  type        = string
  description = "Name prefix."
}

variable "cidr" {
  type        = string
  description = "VPC CIDR."
}

variable "azs" {
  type        = list(string)
  description = "Two or more availability zones."
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
  description = "Create one NAT gateway. This has an hourly cost if applied."
  default     = false
}

variable "tags" {
  type        = map(string)
  description = "Required ownership tags."
  default     = {}
}
