# Terraform Backend Configuration for Azure Storage
# This file configures remote state storage in Azure Storage Account

terraform {
  backend "azurerm" {
    resource_group_name  = "hack2future"
    storage_account_name = "secondstorageeu"
    container_name       = "tfstate"
    key                  = "insurance-fraud-detection.tfstate"
    
    # Use access key authentication (set via environment variable)
    # Export ARM_ACCESS_KEY environment variable with the storage account key
  }
}
