# Key Vault module - RBAC-enabled secret store for RAG application configuration.

resource "azurerm_key_vault" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = var.tenant_id
  sku_name            = "standard"

  # RBAC authorization replaces legacy access policies for production security.
  rbac_authorization_enabled = true

  soft_delete_retention_days = var.soft_delete_retention_days
  purge_protection_enabled   = var.purge_protection_enabled

  tags = var.tags
}

# Grant the Terraform deployer permission to create and manage secrets.
resource "azurerm_role_assignment" "deployer_secrets_officer" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = var.deployer_object_id
}

# Azure OpenAI endpoint consumed by backend and ingestion services.
resource "azurerm_key_vault_secret" "openai_endpoint" {
  name         = "azure-openai-endpoint"
  value        = var.openai_endpoint
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.deployer_secrets_officer]
}

# GPT deployment name for chat/completion API calls.
resource "azurerm_key_vault_secret" "openai_gpt_deployment" {
  name         = "azure-openai-gpt-deployment"
  value        = var.openai_gpt_deployment_name
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.deployer_secrets_officer]
}

# Embedding deployment name for vector generation.
resource "azurerm_key_vault_secret" "openai_embedding_deployment" {
  name         = "azure-openai-embedding-deployment"
  value        = var.openai_embedding_deployment_name
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.deployer_secrets_officer]
}

# Azure AI Search endpoint for retrieval queries.
resource "azurerm_key_vault_secret" "search_endpoint" {
  name         = "azure-search-endpoint"
  value        = var.search_endpoint
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.deployer_secrets_officer]
}
