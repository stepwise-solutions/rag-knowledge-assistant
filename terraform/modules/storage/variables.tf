variable "name" {
  description = "Storage account name (3-24 lowercase alphanumeric characters)."
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

variable "container_name" {
  description = "Private blob container name for documents."
  type        = string
}

variable "blob_soft_delete_days" {
  description = "Soft-delete retention period for blobs and containers."
  type        = number
}

variable "tags" {
  description = "Tags applied to storage resources."
  type        = map(string)
  default     = {}
}
