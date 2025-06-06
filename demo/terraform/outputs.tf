# Outputs for imported resources only

output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "Location of the resource group"
  value       = azurerm_resource_group.main.location
}

output "webapp_url" {
  description = "URL of the web application"
  value       = "https://${azurerm_windows_web_app.main.default_hostname}"
}

output "webapp_name" {
  description = "Name of the web application" 
  value       = azurerm_windows_web_app.main.name
}

output "app_service_plan_name" {
  description = "Name of the App Service Plan"
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
