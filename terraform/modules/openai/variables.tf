variable "name" {
  description = "Azure OpenAI cognitive account name."
  type        = string
}

variable "custom_subdomain_name" {
  description = "Globally unique subdomain required for the OpenAI endpoint."
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

variable "sku_name" {
  description = "Cognitive account SKU."
  type        = string
}

variable "tags" {
  description = "Tags applied to OpenAI resources."
  type        = map(string)
  default     = {}
}

variable "gpt_model_name" {
  description = "GPT model and deployment name."
  type        = string
}

variable "gpt_model_version" {
  description = "GPT model version."
  type        = string
}

variable "gpt_deployment_capacity" {
  description = "GPT deployment TPM capacity (in thousands)."
  type        = number
}

variable "embedding_model_name" {
  description = "Embedding model and deployment name."
  type        = string
}

variable "embedding_model_version" {
  description = "Embedding model version."
  type        = string
}

variable "embedding_deployment_capacity" {
  description = "Embedding deployment TPM capacity (in thousands)."
  type        = number
}
