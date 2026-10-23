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
  description = "Environment tag."
}

variable "owner" {
  type        = string
  description = "Owner tag."
}

variable "create_backup_resources" {
  type        = bool
  description = "Keep false until a backup vault create is explicitly approved."
  default     = false
}

variable "enable_cross_region_copy" {
  type        = bool
  description = "Cross-region copy is off and untested."
  default     = false
}

variable "vault_name" {
  type        = string
  description = "Backup vault name used only when create_backup_resources is true."
}
