# Terraform configuration for importing existing Azure resources
# Backend configuration is in backend.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Import existing resource group
resource "azurerm_resource_group" "main" {
  name     = "hack2future"
  location = "East US"

  # Keep existing tags minimal to match actual state
  tags = {}
}

# Import existing App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "ASP-hack2future-a7e2"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Windows"
  sku_name            = "B2"

  tags = {
    "dev " = "kacper"
  }
}

# Import existing Web App  
resource "azurerm_windows_web_app" "main" {
  name                = "hack2future"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    # Match the current configuration (.NET)
    always_on = false
    
    application_stack {
      current_stack  = "dotnet"
      dotnet_version = "v8.0"
    }
  }

  tags = {
    "dev " = "kacper"
  }
}

# Import existing Storage Account (Document Store)
resource "azurerm_storage_account" "main" {
  name                     = "documentstoreeu"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Premium"
  account_replication_type = "ZRS"
  account_kind             = "StorageV2"

  tags = {
    dev = "robel"
  }
}

# Import existing Storage Account (Second Storage)
resource "azurerm_storage_account" "secondary" {
  name                     = "secondstorageeu"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  account_kind             = "StorageV2"

  tags = {}
}

# Import existing Cognitive Services (OpenAI)
resource "azurerm_cognitive_account" "openai" {
  name                          = "Hack2F"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  kind                          = "OpenAI"
  sku_name                      = "S0"
  custom_subdomain_name         = "hack2f"

  tags = {}
}
