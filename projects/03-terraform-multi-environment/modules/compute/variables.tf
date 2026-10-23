variable "name" {
  type        = string
  description = "Compute name prefix."
}

variable "create" {
  type        = bool
  description = "Create a launch template and an Auto Scaling group."
  default     = false
}

variable "vpc_id" {
  type        = string
  description = "VPC ID."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs."
}

variable "instance_profile_name" {
  type        = string
  description = "IAM instance profile name."
  default     = null
}

variable "instance_type" {
  type        = string
  description = "Instance type used only when create is true."
  default     = "t3.micro"
}

variable "desired_capacity" {
  type        = number
  description = "Desired instances. The committed environments keep create=false."
  default     = 0
}

variable "tags" {
  type        = map(string)
  description = "Ownership tags."
  default     = {}
}
