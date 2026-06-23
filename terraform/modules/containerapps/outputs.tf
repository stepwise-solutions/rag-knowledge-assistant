output "environment_id" {
  description = "Container Apps managed environment resource ID."
  value       = azurerm_container_app_environment.this.id
}

output "environment_name" {
  description = "Container Apps managed environment name."
  value       = azurerm_container_app_environment.this.name
}

output "default_domain" {
  description = "Default domain suffix for apps deployed in this environment."
  value       = azurerm_container_app_environment.this.default_domain
}
