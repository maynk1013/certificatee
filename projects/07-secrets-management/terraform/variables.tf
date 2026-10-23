variable "aws_region" {
  type        = string
  description = "AWS region."
}

variable "create_secret_resource" {
  type        = bool
  description = "Keep false until secret creation is approved. The secret value is not stored in Terraform."
  default     = false
}

variable "secret_name" {
  type        = string
  description = "Secret name."
}
