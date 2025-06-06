# Terraform Insurance Fraud Detection Infrastructure

This directory contains Terraform configuration files to deploy the insurance fraud detection system infrastructure on Microsoft Azure.

## Architecture

The infrastructure includes:

- **Resource Group**: Container for all resources
- **Virtual Network & Subnet**: Network isolation
- **App Service Plan & Web App**: Python Flask web application hosting
- **Function App**: Serverless functions for processing
- **Cosmos DB**: NoSQL database for claims and events storage
- **Storage Account**: Blob storage for documents and files
- **Container Registry**: Docker image storage
- **Application Insights**: Application monitoring and telemetry
- **Log Analytics Workspace**: Centralized logging
- **Event Grid**: Event-driven messaging

## Prerequisites

1. **Azure CLI**: Install and login to Azure
   ```bash
   az login
   ```

2. **Terraform**: Install Terraform (version >= 1.0)
   ```bash
   # Using Homebrew (macOS)
   brew install terraform
   
   # Or download from https://terraform.io/downloads
   ```

3. **Azure Subscription**: Ensure you have an active Azure subscription with sufficient permissions

## Quick Start

1. **Initialize Terraform**:
   ```bash
   cd terraform
   terraform init
   ```

2. **Plan the deployment**:
   ```bash
   terraform plan
   ```

3. **Apply the configuration**:
   ```bash
   terraform apply
   ```

4. **View outputs**:
   ```bash
   terraform output
   ```

## Configuration

### Variables

Key variables can be customized in `terraform.tfvars`:

- `resource_group_name`: Name of the Azure resource group
- `location`: Azure region (default: "East US")
- `prefix`: Prefix for resource names (2-6 characters)
- `environment`: Environment name (dev/staging/prod)
- `cosmos_db_throughput`: Cosmos DB throughput (400-100000)
- `app_service_sku`: App Service plan SKU
- `storage_replication_type`: Storage replication (LRS/GRS/RAGRS/ZRS)

### Environments

Create separate `.tfvars` files for different environments:

```bash
# Development
terraform apply -var-file="dev.tfvars"

# Staging
terraform apply -var-file="staging.tfvars"

# Production
terraform apply -var-file="prod.tfvars"
```

## Outputs

After deployment, Terraform will output important values:

- Web application URL
- Function App URL
- Cosmos DB endpoint and connection strings
- Storage account details
- Container registry information
- Application Insights keys

## Security Notes

- Sensitive outputs are marked as `sensitive = true`
- Use Azure Key Vault for production secrets
- Enable managed identities where possible
- Review and adjust network security rules

## Cost Optimization

- Use `B1` App Service plan for development
- Set appropriate Cosmos DB throughput
- Use `LRS` storage for development environments
- Monitor resource usage with Application Insights

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Troubleshooting

1. **Authentication Issues**: Ensure `az login` is completed
2. **Naming Conflicts**: Adjust the `prefix` variable
3. **Resource Limits**: Check Azure subscription limits
4. **Permission Errors**: Verify RBAC permissions

## Next Steps

1. Deploy the application code to the created resources
2. Configure CI/CD pipelines
3. Set up monitoring and alerting
4. Implement backup strategies
5. Configure scaling policies
