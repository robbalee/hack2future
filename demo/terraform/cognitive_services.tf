# Cognitive Services resources for the insurance fraud detection system

# Custom Vision Training Service
resource "azurerm_cognitive_account" "custom_vision_training" {
  name                = "hack2future-cv-training"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "CustomVision.Training"
  sku_name            = "S0"

  custom_subdomain_name = "hack2future-cv-training"
  
  network_acls {
    default_action = "Allow"
  }

  public_network_access_enabled = true

  tags = {
    environment = var.environment
    project     = "insurance-fraud-detection"
    service     = "custom-vision-training"
  }
}

# Custom Vision Prediction Service
resource "azurerm_cognitive_account" "custom_vision_prediction" {
  name                = "hack2future-cv-prediction"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "CustomVision.Prediction"
  sku_name            = "S0"

  custom_subdomain_name = "hack2future-cv-prediction"
  
  network_acls {
    default_action = "Allow"
  }

  public_network_access_enabled = true

  tags = {
    environment = var.environment
    project     = "insurance-fraud-detection"
    service     = "custom-vision-prediction"
  }
}

# General Cognitive Services (Multi-service account)
resource "azurerm_cognitive_account" "fraud_detection" {
  name                = "hack2future-fraud-detection"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "CognitiveServices"
  sku_name            = "S0"

  public_network_access_enabled = true

  tags = {
    environment = var.environment
    project     = "insurance-fraud-detection"
    service     = "fraud-detection"
  }
}
