variable "name" {
  description = "Azure AI Search service name."
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

variable "sku" {
  description = "Search service SKU (standard recommended for production)."
  type        = string
}

variable "tags" {
  description = "Tags applied to the search service."
  type        = map(string)
  default     = {}
}
