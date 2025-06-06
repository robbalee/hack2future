# Terraform Remote State Configuration

This project uses Azure Storage as the Terraform remote backend for state management.

## Configuration

**Backend Details:**
- **Storage Account**: `secondstorageeu`
- **Resource Group**: `hack2future`
- **Container**: `tfstate`
- **State File**: `insurance-fraud-detection.tfstate`

## Setup Instructions

### For Team Members

1. **Prerequisites:**
   - Azure CLI installed and logged in
   - Terraform installed
   - Access to the `hack2future` resource group

2. **Environment Setup:**
   ```bash
   # Set the storage account access key
   export ARM_ACCESS_KEY="<storage-account-key>"
   
   # Initialize Terraform
   terraform init
   ```

3. **Get Storage Account Key:**
   ```bash
   az storage account keys list \
     --resource-group hack2future \
     --account-name secondstorageeu \
     --query '[0].value' -o tsv
   ```

### Alternative Authentication Methods

#### Option 1: Service Principal
```bash
export ARM_CLIENT_ID="<service-principal-id>"
export ARM_CLIENT_SECRET="<service-principal-secret>"
export ARM_SUBSCRIPTION_ID="<subscription-id>"
export ARM_TENANT_ID="<tenant-id>"
```

#### Option 2: Azure AD Authentication
Update `backend.tf`:
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "hack2future"
    storage_account_name = "secondstorageeu"
    container_name       = "tfstate"
    key                  = "insurance-fraud-detection.tfstate"
    use_azuread_auth     = true
  }
}
```

## Benefits

✅ **State Sharing**: Multiple team members can work with the same state  
✅ **State Locking**: Prevents concurrent modifications  
✅ **Backup & Versioning**: Azure Storage provides automatic versioning  
✅ **Security**: Access controlled through Azure RBAC  
✅ **Reliability**: Hosted in Azure with high availability  

## Security Best Practices

1. **Never commit** storage account keys to source control
2. **Use environment variables** for authentication
3. **Rotate keys** regularly
4. **Limit access** to the storage account
5. **Use managed identities** when possible in CI/CD

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure you have access to the storage account
2. **State Locked**: Wait for the lock to be released or break it if necessary
3. **Backend Configuration Changes**: Run `terraform init -reconfigure`

### Break State Lock (if needed)
```bash
terraform force-unlock <lock-id>
```

## CI/CD Integration

For GitHub Actions or Azure DevOps, use:
```yaml
env:
  ARM_ACCESS_KEY: ${{ secrets.ARM_ACCESS_KEY }}
```

Store the access key as a secret in your CI/CD system.
