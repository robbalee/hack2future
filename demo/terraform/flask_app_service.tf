# Linux App Service Plan and Web App for Flask Application
# This is separate from the existing Windows App Service Plan

# Create a dedicated Linux App Service Plan for Flask
resource "azurerm_service_plan" "flask_linux" {
  name                = "asp-flask-fraud-detection-linux"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"  # Basic tier - can be upgraded later

  tags = {
    environment = "dev"
    project     = "insurance-fraud-detection"
    runtime     = "python"
  }
}

# Create Linux Web App for Flask application
resource "azurerm_linux_web_app" "flask_app" {
  name                = "insurance-fraud-detection-flask"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.flask_linux.id

  site_config {
    always_on = false  # Set to true for production
    
    application_stack {
      python_version = "3.11"
    }

    # Configure startup command for Flask
    app_command_line = "python -m gunicorn --bind=0.0.0.0 --timeout 600 app:app"
  }

  app_settings = {
    # Python runtime settings
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"     = "true"
    
    # Flask application settings
    "FLASK_ENV"        = "production"
    "FLASK_APP"        = "app.py"
    "PYTHONPATH"       = "/home/site/wwwroot"
    
    # Azure service connections (will be populated after deployment)
    "COSMOS_DB_ENDPOINT"    = azurerm_cosmosdb_account.main.endpoint
    "COSMOS_DB_KEY"         = azurerm_cosmosdb_account.main.primary_key
    "COSMOS_DB_DATABASE"    = azurerm_cosmosdb_sql_database.main.name
    
    # Storage account settings
    "AZURE_STORAGE_ACCOUNT_NAME" = azurerm_storage_account.main.name
    "AZURE_STORAGE_ACCOUNT_KEY"  = azurerm_storage_account.main.primary_access_key
    "AZURE_STORAGE_CONTAINER"    = "uploads"
    
    # Cognitive Services settings
    "OPENAI_ENDPOINT"     = azurerm_cognitive_account.openai.endpoint
    "OPENAI_API_KEY"      = azurerm_cognitive_account.openai.primary_access_key
    "FRAUD_DETECTION_ENDPOINT" = azurerm_cognitive_account.fraud_detection.endpoint
    "FRAUD_DETECTION_KEY"      = azurerm_cognitive_account.fraud_detection.primary_access_key
  }

  # Configure identity for managed identity access (future enhancement)
  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "dev"
    project     = "insurance-fraud-detection"
    runtime     = "python-flask"
  }
}

# Create storage container for file uploads
resource "azurerm_storage_container" "uploads" {
  name                  = "uploads"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Create storage container for backups
resource "azurerm_storage_container" "backups" {
  name                  = "backups"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}
