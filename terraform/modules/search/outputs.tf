output "service_name" {
  description = "Azure AI Search service name."
  value       = azurerm_search_service.this.name
}

output "endpoint" {
  description = "Azure AI Search HTTPS endpoint."
  value       = "https://${azurerm_search_service.this.name}.search.windows.net"
}

output "id" {
  description = "Azure AI Search service resource ID."
  value       = azurerm_search_service.this.id
}

output "principal_id" {
  description = "System-assigned managed identity principal ID."
  value       = azurerm_search_service.this.identity[0].principal_id
}
