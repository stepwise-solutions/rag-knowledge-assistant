variable "name" {
  description = "Container Apps managed environment name."
  type        = string
}

variable "resource_group_name" {
  description = "Target resource group name."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
}

variable "tags" {
  description = "Tags applied to the Container Apps environment."
  type        = map(string)
  default     = {}
}
