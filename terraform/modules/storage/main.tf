# Storage module - secure blob storage for RAG document ingestion.

resource "azurerm_storage_account" "this" {
  name                     = var.name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  # Enforce encrypted HTTPS traffic for all blob operations.
  https_traffic_only_enabled = true
  min_tls_version            = "TLS1_2"

  blob_properties {
    # Versioning preserves prior blob states for recovery and auditability.
    versioning_enabled = true

    # Soft delete protects against accidental blob deletion.
    delete_retention_policy {
      days = var.blob_soft_delete_days
    }

    # Soft delete for containers complements blob-level protection.
    container_delete_retention_policy {
      days = var.blob_soft_delete_days
    }
  }

  tags = var.tags
}

# Private container for uploaded source documents consumed by ingestion jobs.
resource "azurerm_storage_container" "documents" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}
