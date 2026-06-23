output "account_name" {
  description = "Azure OpenAI cognitive account name."
  value       = azurerm_cognitive_account.this.name
}

output "endpoint" {
  description = "Azure OpenAI endpoint URL."
  value       = azurerm_cognitive_account.this.endpoint
}

output "gpt_deployment_name" {
  description = "GPT model deployment name."
  value       = azurerm_cognitive_deployment.gpt.name
}

output "embedding_deployment_name" {
  description = "Embedding model deployment name."
  value       = azurerm_cognitive_deployment.embedding.name
}

output "account_id" {
  description = "Azure OpenAI cognitive account resource ID."
  value       = azurerm_cognitive_account.this.id
}

output "principal_id" {
  description = "System-assigned managed identity principal ID."
  value       = azurerm_cognitive_account.this.identity[0].principal_id
}
