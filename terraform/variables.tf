variable "subscription_id" {
  description = "Azure subscription ID. Set via terraform.tfvars (gitignored) or TF_VAR_subscription_id — never commit this value."
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Short project name used in resource naming (e.g. rag-assistant)."
  type        = string
  default     = "rag-assistant"
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region for all resources (e.g. uksouth for UK South)."
  type        = string
  default     = "uksouth"
}

variable "openai_sku" {
  description = "SKU for the Azure OpenAI cognitive account."
  type        = string
  default     = "S0"
}

variable "search_sku" {
  description = "SKU for Azure AI Search (use standard for production RAG workloads)."
  type        = string
  default     = "standard"
}

variable "tags" {
  description = "Common tags applied to all resources."
  type        = map(string)
  default     = {}
}

variable "gpt_model_name" {
  description = "Azure OpenAI GPT model deployment name."
  type        = string
  default     = "gpt-4.1-mini"
}

variable "gpt_model_version" {
  description = "Azure OpenAI GPT model version."
  type        = string
  default     = "2025-04-14"
}

variable "gpt_deployment_capacity" {
  description = "GPT deployment capacity in thousands of tokens per minute (TPM)."
  type        = number
  default     = 20
}

variable "embedding_model_name" {
  description = "Azure OpenAI embedding model deployment name."
  type        = string
  default     = "text-embedding-3-large"
}

variable "embedding_model_version" {
  description = "Azure OpenAI embedding model version."
  type        = string
  default     = "1"
}

variable "embedding_deployment_capacity" {
  description = "Embedding deployment capacity in thousands of tokens per minute (TPM)."
  type        = number
  default     = 50
}

variable "documents_container_name" {
  description = "Private blob container name for RAG document ingestion."
  type        = string
  default     = "documents"
}

variable "key_vault_soft_delete_retention_days" {
  description = "Number of days to retain soft-deleted Key Vault objects."
  type        = number
  default     = 90
}

variable "key_vault_purge_protection_enabled" {
  description = "Enable purge protection on Key Vault (recommended for production)."
  type        = bool
  default     = true
}

variable "storage_blob_soft_delete_days" {
  description = "Number of days to retain soft-deleted blobs."
  type        = number
  default     = 7
}
