variable "name" {
  description = "Key Vault name."
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

variable "tenant_id" {
  description = "Azure AD tenant ID."
  type        = string
}

variable "deployer_object_id" {
  description = "Object ID of the principal running Terraform (for secret management RBAC)."
  type        = string
}

variable "soft_delete_retention_days" {
  description = "Soft-delete retention period for Key Vault."
  type        = number
}

variable "purge_protection_enabled" {
  description = "Whether purge protection is enabled."
  type        = bool
}

variable "openai_endpoint" {
  description = "Azure OpenAI endpoint URL to store as a secret."
  type        = string
}

variable "openai_gpt_deployment_name" {
  description = "GPT deployment name to store as a secret."
  type        = string
}

variable "openai_embedding_deployment_name" {
  description = "Embedding deployment name to store as a secret."
  type        = string
}

variable "search_endpoint" {
  description = "Azure AI Search endpoint URL to store as a secret."
  type        = string
}

variable "tags" {
  description = "Tags applied to Key Vault resources."
  type        = map(string)
  default     = {}
}
