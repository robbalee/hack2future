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
