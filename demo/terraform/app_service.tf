# Linux App Service Plan and App Service for Python Flask Insurance Fraud Detection
# Separate from existing Windows infrastructure

# Create Linux App Service Plan for Python Flask app
resource "azurerm_service_plan" "flask_app" {
  name                = "insurance-fraud-flask-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B2"  # Basic tier with 2 cores, suitable for demo/dev

  tags = {
    project     = "insurance-fraud-detection"
    environment = "dev"
    stack       = "python-flask"
  }
}

# Create Linux Web App for Flask application
resource "azurerm_linux_web_app" "flask_app" {
  name                = "insurance-fraud-detection-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.flask_app.location
  service_plan_id     = azurerm_service_plan.flask_app.id

  # Enable System-Assigned Managed Identity for secure Cosmos DB access
  identity {
    type = "SystemAssigned"
  }

  # Application settings for Flask app
  app_settings = {
    # Python runtime configuration
    "PYTHONPATH"               = "/home/site/wwwroot"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    
    # Flask configuration
    "FLASK_ENV"                = "production"
    "FLASK_APP"                = "app.py"
    
    # Cosmos DB configuration using managed identity
    "COSMOS_ENDPOINT"          = azurerm_cosmosdb_account.main.endpoint
    "COSMOS_DATABASE"          = azurerm_cosmosdb_sql_database.main.name
    "USE_MANAGED_IDENTITY"     = "true"
    
    # Storage account configuration
    "AZURE_STORAGE_ACCOUNT"    = azurerm_storage_account.main.name
    "AZURE_STORAGE_CONTAINER"  = "uploads"
    
    # Cognitive Services configuration
    "OPENAI_ENDPOINT"          = azurerm_cognitive_account.openai.endpoint
    "FRAUD_DETECTION_ENDPOINT" = azurerm_cognitive_account.fraud_detection.endpoint
  }

  site_config {
    # Python 3.11 runtime
    application_stack {
      python_version = "3.11"
    }
    
    # Security settings
    always_on                = true
    ftps_state              = "Disabled"
    http2_enabled           = true
    minimum_tls_version     = "1.2"
    
    # CORS for development (adjust for production)
    cors {
      allowed_origins = ["https://insurance-fraud-detection-app.azurewebsites.net"]
      support_credentials = true
    }
  }

  # Enable HTTPS only
  https_only = true

  tags = {
    project     = "insurance-fraud-detection"
    environment = "dev"
    stack       = "python-flask"
  }
}

# Grant the App Service managed identity access to Cosmos DB
resource "azurerm_cosmosdb_sql_role_assignment" "flask_app" {
  account_name        = azurerm_cosmosdb_account.main.name
  resource_group_name = azurerm_resource_group.main.name
  role_definition_id  = "/subscriptions/${data.azurerm_client_config.current.subscription_id}/resourceGroups/${azurerm_resource_group.main.name}/providers/Microsoft.DocumentDB/databaseAccounts/${azurerm_cosmosdb_account.main.name}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"
  scope               = azurerm_cosmosdb_account.main.id
  principal_id        = azurerm_linux_web_app.flask_app.identity[0].principal_id
}

# Grant the App Service managed identity access to Storage Account
resource "azurerm_role_assignment" "flask_app_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_web_app.flask_app.identity[0].principal_id
}

# Grant the App Service managed identity access to Cognitive Services
resource "azurerm_role_assignment" "flask_app_cognitive_openai" {
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azurerm_linux_web_app.flask_app.identity[0].principal_id
}

resource "azurerm_role_assignment" "flask_app_cognitive_fraud" {
  scope                = azurerm_cognitive_account.fraud_detection.id
  role_definition_name = "Cognitive Services User"
  principal_id         = azurerm_linux_web_app.flask_app.identity[0].principal_id
}
