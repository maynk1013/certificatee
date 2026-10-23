variable "name" {
  description = "Name prefix for IAM roles."
  type        = string
}

variable "tags" {
  description = "Tags applied to IAM roles."
  type        = map(string)
  default     = {}
}
