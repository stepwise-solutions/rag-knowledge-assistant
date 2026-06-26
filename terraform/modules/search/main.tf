# Azure AI Search module - dedicated search service for RAG retrieval.

resource "azurerm_search_service" "this" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku

  # Standard semantic ranker requires a paid search SKU (basic or above).
  # semantic_search_sku must be omitted entirely when sku is "free".
  semantic_search_sku = var.sku == "free" ? null : "standard"

  # Managed identity supports future RBAC-based indexer and query access.
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}
