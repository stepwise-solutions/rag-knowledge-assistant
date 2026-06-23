# Azure OpenAI module - cognitive account plus GPT and embedding deployments.

resource "azurerm_cognitive_account" "this" {
  name                  = var.name
  location              = var.location
  resource_group_name   = var.resource_group_name
  kind                  = "OpenAI"
  sku_name              = var.sku_name
  custom_subdomain_name = var.custom_subdomain_name

  # Managed identity enables passwordless access from future Container Apps workloads.
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

# GPT deployment for chat/completion workloads in the RAG assistant.
resource "azurerm_cognitive_deployment" "gpt" {
  name                 = var.gpt_model_name
  cognitive_account_id = azurerm_cognitive_account.this.id

  model {
    format  = "OpenAI"
    name    = var.gpt_model_name
    version = var.gpt_model_version
  }

  sku {
    name     = "Standard"
    capacity = var.gpt_deployment_capacity
  }
}

# Embedding deployment for vectorizing documents and user queries.
resource "azurerm_cognitive_deployment" "embedding" {
  name                 = var.embedding_model_name
  cognitive_account_id = azurerm_cognitive_account.this.id

  model {
    format  = "OpenAI"
    name    = var.embedding_model_name
    version = var.embedding_model_version
  }

  sku {
    name     = "Standard"
    capacity = var.embedding_deployment_capacity
  }
}
