locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = merge(
    {
      project     = var.project_name
      environment = var.environment
      managed_by  = "terraform"
    },
    var.tags
  )

  # Storage account names must be 3-24 lowercase alphanumeric characters only.
  storage_account_name = substr(replace("${var.project_name}${var.environment}st", "-", ""), 0, 24)
}

# Core resource group for the RAG platform.
module "resource_group" {
  source = "./modules/resource_group"

  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

# Azure OpenAI account and model deployments for chat and embeddings.
module "openai" {
  source = "./modules/openai"

  name                  = "${local.name_prefix}-openai"
  custom_subdomain_name = replace("${local.name_prefix}-openai", "_", "-")
  resource_group_name   = module.resource_group.name
  location              = module.resource_group.location
  sku_name              = var.openai_sku
  tags                  = local.common_tags

  gpt_model_name                = var.gpt_model_name
  gpt_model_version             = var.gpt_model_version
  gpt_deployment_capacity       = var.gpt_deployment_capacity
  embedding_model_name          = var.embedding_model_name
  embedding_model_version       = var.embedding_model_version
  embedding_deployment_capacity = var.embedding_deployment_capacity
}

# Azure AI Search service with semantic ranking enabled.
module "search" {
  source = "./modules/search"

  name                = "${local.name_prefix}-search"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  sku                 = var.search_sku
  tags                = local.common_tags
}

# Storage account and private documents container for ingestion pipelines.
module "storage" {
  source = "./modules/storage"

  name                  = local.storage_account_name
  resource_group_name   = module.resource_group.name
  location              = module.resource_group.location
  container_name        = var.documents_container_name
  blob_soft_delete_days = var.storage_blob_soft_delete_days
  tags                  = local.common_tags
}

# Container Apps managed environment for future FastAPI and ingestion workloads.
module "containerapps" {
  source = "./modules/containerapps"

  name                = "${local.name_prefix}-cae"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  tags                = local.common_tags
}

# Key Vault with RBAC authorization and application configuration secrets.
module "keyvault" {
  source = "./modules/keyvault"

  name                = "${local.name_prefix}-kv"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  deployer_object_id  = data.azurerm_client_config.current.object_id
  tags                = local.common_tags

  soft_delete_retention_days = var.key_vault_soft_delete_retention_days
  purge_protection_enabled   = var.key_vault_purge_protection_enabled

  openai_endpoint                  = module.openai.endpoint
  openai_gpt_deployment_name       = module.openai.gpt_deployment_name
  openai_embedding_deployment_name = module.openai.embedding_deployment_name
  search_endpoint                  = module.search.endpoint

  depends_on = [
    module.openai,
    module.search,
  ]
}
