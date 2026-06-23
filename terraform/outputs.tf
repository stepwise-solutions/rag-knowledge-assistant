output "resource_group_name" {
  description = "Name of the resource group hosting all RAG infrastructure."
  value       = module.resource_group.name
}

output "openai_endpoint" {
  description = "Azure OpenAI service endpoint URL."
  value       = module.openai.endpoint
}

output "openai_account_name" {
  description = "Azure OpenAI cognitive account name."
  value       = module.openai.account_name
}

output "openai_gpt_deployment_name" {
  description = "Deployment name for the GPT chat model."
  value       = module.openai.gpt_deployment_name
}

output "openai_embedding_deployment_name" {
  description = "Deployment name for the embedding model."
  value       = module.openai.embedding_deployment_name
}

output "search_endpoint" {
  description = "Azure AI Search service endpoint URL."
  value       = module.search.endpoint
}

output "search_service_name" {
  description = "Azure AI Search service name."
  value       = module.search.service_name
}

output "storage_account_name" {
  description = "Storage account name used for document ingestion."
  value       = module.storage.storage_account_name
}

output "documents_container_name" {
  description = "Private blob container name for uploaded documents."
  value       = module.storage.container_name
}

# output "key_vault_name" {
#   description = "Key Vault name storing application configuration secrets."
#   value       = module.keyvault.key_vault_name
# }

# output "key_vault_uri" {
#   description = "Key Vault URI for secret retrieval."
#   value       = module.keyvault.key_vault_uri
# }

# output "container_apps_environment_id" {
#   description = "Resource ID of the Container Apps managed environment."
#   value       = module.containerapps.environment_id
# }
