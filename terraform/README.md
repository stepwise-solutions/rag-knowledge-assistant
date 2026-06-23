# Azure Infrastructure for RAG Knowledge Assistant

Production-oriented Terraform configuration that provisions Azure resources for a Retrieval-Augmented Generation (RAG) knowledge assistant.

## Architecture

```text
terraform/
├── main.tf                 # Root module wiring
├── variables.tf            # Input variables
├── outputs.tf              # Root outputs
├── providers.tf            # AzureRM provider configuration
├── terraform.tfvars.example
└── modules/
    ├── resource_group/     # Resource group
    ├── openai/             # Azure OpenAI + model deployments
    ├── search/             # Azure AI Search (semantic ranking)
    ├── storage/            # Document storage account + container
    ├── keyvault/           # RBAC Key Vault + application secrets
    └── containerapps/      # Container Apps Environment
```

## Resources Created

| Module | Resources |
|--------|-----------|
| `resource_group` | Azure Resource Group |
| `openai` | Cognitive Account (OpenAI), GPT deployment (`gpt-4o-mini`), Embedding deployment (`text-embedding-3-large`) |
| `search` | Azure AI Search (Standard SKU, semantic search enabled) |
| `storage` | Storage Account (HTTPS, versioning, soft delete), private `documents` container |
| `keyvault` | Key Vault (RBAC), secrets for OpenAI and Search endpoints/deployments |
| `containerapps` | Azure Container Apps Environment (for future FastAPI and ingestion jobs) |

## Naming Convention

Resources follow `<project>-<environment>-<resource>`:

- `rag-assistant-dev-rg`
- `rag-assistant-dev-openai`
- `rag-assistant-dev-search`
- `rag-assistant-dev-kv`

Storage account names are globally unique and omit hyphens due to Azure constraints (for example, `ragassistantdevst`).

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.8
- An active **Azure Subscription**
- Sufficient permissions to create resources and assign RBAC roles (Owner or User Access Administrator + Contributor)
- Azure OpenAI and Azure AI Search quota in the target region (UK South / `uksouth` is supported for semantic search)

## Login

Authenticate with Azure CLI:

```bash
az login
```

Set the active subscription (Terraform reads the ID from your local config, not from git):

```bash
az account set --subscription "<your-subscription-id>"
```

## Configuration

Core values (`project_name`, `environment`, `location`) have defaults in `variables.tf`. The **subscription ID is not stored in git** — provide it locally using one of these options:

### Option 1: `terraform.tfvars` (recommended)

`terraform.tfvars` is listed in `.gitignore` and is never pushed.

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and set your subscription ID:

```hcl
subscription_id = "<your-subscription-id>"
```

### Option 2: Environment variable

PowerShell:

```powershell
$env:TF_VAR_subscription_id = "<your-subscription-id>"
```

Bash:

```bash
export TF_VAR_subscription_id="<your-subscription-id>"
```

| Variable | Source |
|----------|--------|
| `subscription_id` | Local only (`terraform.tfvars` or `TF_VAR_subscription_id`) |
| `project_name` | Default: `rag-assistant` |
| `environment` | Default: `dev` |
| `location` | Default: `uksouth` |

## Terraform Commands

Initialize providers and modules:

```bash
terraform init
```

Preview planned changes:

```bash
terraform plan
```

Apply infrastructure:

```bash
terraform apply
```

Destroy infrastructure (when no longer needed):

```bash
terraform destroy
```

## Outputs

After a successful apply, Terraform exposes:

| Output | Description |
|--------|-------------|
| `resource_group_name` | Name of the shared resource group |
| `openai_endpoint` | Azure OpenAI HTTPS endpoint |
| `openai_account_name` | Azure OpenAI cognitive account name |
| `openai_gpt_deployment_name` | GPT chat model deployment name |
| `openai_embedding_deployment_name` | Embedding model deployment name |
| `search_endpoint` | Azure AI Search HTTPS endpoint |
| `search_service_name` | Azure AI Search service name |
| `storage_account_name` | Blob storage account for document ingestion |
| `documents_container_name` | Private blob container name (`documents`) |
| `key_vault_name` | Key Vault storing application configuration secrets |
| `key_vault_uri` | Key Vault URI for secret retrieval |
| `container_apps_environment_id` | Container Apps Environment ID for future app deployment |

View outputs:

```bash
terraform output
```

## Key Vault Secrets

The Key Vault module stores these secrets (RBAC-protected):

- `azure-openai-endpoint`
- `azure-openai-gpt-deployment`
- `azure-openai-embedding-deployment`
- `azure-search-endpoint`

Grant application identities the **Key Vault Secrets User** role on the vault before they read secrets at runtime.

## Production Notes

- Key Vault purge protection is enabled by default (`key_vault_purge_protection_enabled = true`).
- Storage uses GRS replication and blob versioning with soft delete.
- Azure AI Search uses the Standard SKU with semantic ranking enabled.
- No API keys or credentials are hardcoded; use managed identities and Key Vault references in application code.
- For production hardening, consider adding private endpoints, network ACLs, and a dedicated deployment pipeline with remote state (Azure Storage backend).

## Troubleshooting

**OpenAI model availability**: Confirm `gpt-4o-mini` and `text-embedding-3-large` are available in your region via Azure OpenAI Studio.

**Key Vault RBAC errors on apply**: The deploying principal needs permission to assign the **Key Vault Secrets Officer** role. Retry after RBAC propagation (typically 1–2 minutes).

**Search name conflicts**: Search service names are globally unique. Change `project_name` or `environment` if the name is taken.
