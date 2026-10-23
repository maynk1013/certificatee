variable "name" {
  type        = string
  description = "Role name prefix."
}

variable "create" {
  type        = bool
  description = "Create the instance role. Keep false until an apply is approved."
  default     = false
}

variable "tags" {
  type        = map(string)
  description = "Ownership tags."
  default     = {}
}
