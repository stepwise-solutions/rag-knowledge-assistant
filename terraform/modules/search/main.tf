# Azure AI Search module - dedicated search service with semantic ranking.

resource "azurerm_search_service" "this" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku

  # Semantic ranker improves relevance for RAG retrieval queries.
  semantic_search_sku = "standard"

  # Managed identity supports future RBAC-based indexer and query access.
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}
