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
├── scripts/
│   └── Register-Container-Apps.ps1
└── modules/
    ├── resource_group/     # Resource group
    ├── openai/             # Azure OpenAI + model deployments
    ├── search/             # Azure AI Search
    ├── storage/            # Document storage account + container
    ├── keyvault/           # RBAC Key Vault + application secrets
    └── containerapps/      # Container Apps Environment
```

## Resources Created

| Module | Resources |
|--------|-----------|
| `resource_group` | Azure Resource Group |
| `openai` | Cognitive Account (OpenAI), GPT deployment (`gpt-4.1-mini`), Embedding deployment (`text-embedding-3-large`) |
| `search` | Azure AI Search (Free tier by default; vector search supported with storage limits) |
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

## Prerequisites (Windows)

Install the following before running Terraform:

1. **[Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows)** — verify with:

   ```powershell
   az --version
   ```

2. **[Terraform](https://developer.hashicorp.com/terraform/install#windows)** — verify with:

   ```powershell
   terraform --version
   ```

   Requires Terraform >= 1.8.

3. **An active Azure subscription** with permissions to create resources and assign RBAC roles (Owner, or User Access Administrator + Contributor).

4. **Azure OpenAI and Azure AI Search quota** in the target region (`uksouth` is the default).

Open PowerShell and navigate to the Terraform directory:

```powershell
cd C:\path\to\rag-knowledge-assistant\terraform
```

## Login

Authenticate with Azure CLI:

```powershell
az login
```

A browser window opens for sign-in. Set the active subscription (Terraform reads the ID from your local config, not from git):

```powershell
az account set --subscription "<your-subscription-id>"
```

Confirm the active subscription:

```powershell
az account show --query "{name:name, id:id}" -o table
```

## Configuration

Core values (`project_name`, `environment`, `location`) have defaults in `variables.tf`. The **subscription ID is not stored in git** — provide it locally using one of these options:

### Option 1: `terraform.tfvars` (recommended)

`terraform.tfvars` is listed in `.gitignore` and is never pushed.

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
notepad terraform.tfvars
```

Edit `terraform.tfvars` and set your subscription ID:

```hcl
subscription_id = "<your-subscription-id>"
```

The example file defaults to `search_sku = "free"` for dev cost control. Change to `"basic"` or `"standard"` for production workloads with more storage and semantic ranking.

### Option 2: Environment variable

```powershell
$env:TF_VAR_subscription_id = "<your-subscription-id>"
```

| Variable | Source |
|----------|--------|
| `subscription_id` | Local only (`terraform.tfvars` or `TF_VAR_subscription_id`) |
| `project_name` | Default: `rag-assistant` |
| `environment` | Default: `dev` |
| `location` | Default: `uksouth` |
| `search_sku` | Default: `free` |

## Terraform Commands

Run all commands from the `terraform/` directory with PowerShell.

Initialize providers and modules:

```powershell
terraform init
```

Preview planned changes:

```powershell
terraform plan
```

Apply infrastructure:

```powershell
terraform apply
```

Type `yes` when prompted to confirm.

Destroy infrastructure (when no longer needed):

```powershell
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

```powershell
terraform output
```

View a single output:

```powershell
terraform output search_endpoint
```

## Connect to the Application

After `terraform apply`, copy values into the project root `.env` file for local development. Retrieve Azure OpenAI and Search keys from the [Azure Portal](https://portal.azure.com) or Azure CLI:

```powershell
# Search admin key
az search admin-key show --service-name (terraform output -raw search_service_name) --resource-group (terraform output -raw resource_group_name)

# OpenAI key
az cognitiveservices account keys list --name (terraform output -raw openai_account_name) --resource-group (terraform output -raw resource_group_name)
```

Example `.env` mapping:

```env
AZURE_OPENAI_ENDPOINT=<openai_endpoint>
AZURE_OPENAI_GPT_DEPLOYMENT=<openai_gpt_deployment_name>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<openai_embedding_deployment_name>
AZURE_SEARCH_ENDPOINT=<search_endpoint>
AZURE_SEARCH_INDEX_NAME=rag-documents
```

Then create the search index and ingest documents — see the [project README](../README.md).

## Key Vault Secrets

The Key Vault module stores these secrets (RBAC-protected):

- `azure-openai-endpoint`
- `azure-openai-gpt-deployment`
- `azure-openai-embedding-deployment`
- `azure-search-endpoint`

Grant application identities the **Key Vault Secrets User** role on the vault before they read secrets at runtime.

## Search SKU Notes

| SKU | Use case |
|-----|----------|
| `free` (default) | Dev and small workloads. Vector search supported. 50 MB storage, 3 indexes max, 1 service per subscription. |
| `basic` / `standard` | Production. More storage, semantic ranker on paid tiers, scalable partitions. |

The Free tier cannot be upgraded in place — create a new search service on a paid SKU and re-index your documents.

## Production Notes

- Key Vault purge protection is enabled by default (`key_vault_purge_protection_enabled = true`).
- Storage uses GRS replication and blob versioning with soft delete.
- No API keys or credentials are hardcoded; use managed identities and Key Vault references in application code.
- For production hardening, consider adding private endpoints, network ACLs, and a dedicated deployment pipeline with remote state (Azure Storage backend).

## Troubleshooting

**OpenAI model availability**: Confirm `gpt-4.1-mini` and `text-embedding-3-large` are available in your region via [Azure OpenAI Studio](https://oai.azure.com/).

**Key Vault RBAC errors on apply**: The deploying principal needs permission to assign the **Key Vault Secrets Officer** role. Retry after RBAC propagation (typically 1–2 minutes).

**Search name conflicts**: Search service names are globally unique. Change `project_name` or `environment` if the name is taken.

**409 Conflict on search service create**: If a previous service with the same name was recently deleted, Azure may still be cleaning up. Wait 15–60 minutes and retry, or use a different `project_name` / `environment`.

**Terraform not recognised**: Close and reopen PowerShell after installing Terraform, or add the install directory to your PATH.

**SSL / certificate errors with Azure CLI**: Common on corporate networks. Contact your IT team or configure the proxy/certificate bundle for Azure CLI.
