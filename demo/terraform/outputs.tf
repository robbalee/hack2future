# Outputs for imported resources only

output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "Location of the resource group"
  value       = azurerm_resource_group.main.location
}

# Windows web app outputs removed - using Flask Linux app instead

output "linux_app_service_plan_name" {
  description = "Name of the Linux App Service Plan for Flask"
  value       = azurerm_service_plan.flask_app.name
}

output "windows_app_service_plan_name" {
  description = "Name of the existing Windows App Service Plan"
  value       = azurerm_service_plan.main.name
}

# Custom Vision Training outputs
output "custom_vision_training_endpoint" {
  description = "Custom Vision Training endpoint"
  value       = azurerm_cognitive_account.custom_vision_training.endpoint
}

output "custom_vision_training_key" {
  description = "Custom Vision Training primary key"
  value       = azurerm_cognitive_account.custom_vision_training.primary_access_key
  sensitive   = true
}

# Custom Vision Prediction outputs
output "custom_vision_prediction_endpoint" {
  description = "Custom Vision Prediction endpoint"
  value       = azurerm_cognitive_account.custom_vision_prediction.endpoint
}

output "custom_vision_prediction_key" {
  description = "Custom Vision Prediction primary key"
  value       = azurerm_cognitive_account.custom_vision_prediction.primary_access_key
  sensitive   = true
}

# Fraud Detection outputs
output "fraud_detection_endpoint" {
  description = "Fraud Detection Cognitive Services endpoint"
  value       = azurerm_cognitive_account.fraud_detection.endpoint
}

output "fraud_detection_key" {
  description = "Fraud Detection Cognitive Services primary key"
  value       = azurerm_cognitive_account.fraud_detection.primary_access_key
  sensitive   = true
}

# Backward compatibility - original app service plan name
output "app_service_plan_name" {
  description = "Name of the Windows App Service Plan (backward compatibility)"
  value       = azurerm_service_plan.main.name
}

output "storage_account_name" {
  description = "Main storage account name"
  value       = azurerm_storage_account.main.name
}

output "storage_account_primary_key" {
  description = "Main storage account primary key"  
  value       = azurerm_storage_account.main.primary_access_key
  sensitive   = true
}

output "storage_connection_string" {
  description = "Main storage account connection string"
  value       = azurerm_storage_account.main.primary_connection_string
  sensitive   = true
}

output "secondary_storage_account_name" {
  description = "Secondary storage account name"
  value       = azurerm_storage_account.secondary.name
}

output "cognitive_account_name" {
  description = "Cognitive Services account name"
  value       = azurerm_cognitive_account.openai.name
}

output "cognitive_account_endpoint" {
  description = "Cognitive Services endpoint"
  value       = azurerm_cognitive_account.openai.endpoint
}

# Cosmos DB Outputs
output "cosmos_db_endpoint" {
  description = "Endpoint for the Cosmos DB account"
  value       = azurerm_cosmosdb_account.main.endpoint
}

output "cosmos_db_primary_key" {
  description = "Primary key for the Cosmos DB account"
  value       = azurerm_cosmosdb_account.main.primary_key
  sensitive   = true
}

output "cosmos_db_connection_string" {
  description = "Connection string for the Cosmos DB account"
  value       = azurerm_cosmosdb_account.main.connection_strings[0]
  sensitive   = true
}

output "cosmos_db_name" {
  description = "Name of the Cosmos DB SQL database"
  value       = azurerm_cosmosdb_sql_database.main.name
}

output "cosmos_claims_container" {
  description = "Name of the Cosmos DB container for claims"
  value       = azurerm_cosmosdb_sql_container.claims.name
}

output "cosmos_events_container" {
  description = "Name of the Cosmos DB container for events"
  value       = azurerm_cosmosdb_sql_container.events.name
}

# Flask App Service outputs
output "flask_app_url" {
  description = "URL of the Flask insurance fraud detection app"
  value       = "https://${azurerm_linux_web_app.flask_app.default_hostname}"
}

output "flask_app_name" {
  description = "Name of the Flask app service"
  value       = azurerm_linux_web_app.flask_app.name
}

output "flask_app_resource_group" {
  description = "Resource group containing the Flask app"
  value       = azurerm_linux_web_app.flask_app.resource_group_name
}

output "flask_app_managed_identity" {
  description = "Managed identity principal ID for the Flask app"
  value       = azurerm_linux_web_app.flask_app.identity[0].principal_id
}

output "flask_app_service_plan" {
  description = "Name of the Linux App Service Plan for Flask"
  value       = azurerm_service_plan.flask_app.name
}
