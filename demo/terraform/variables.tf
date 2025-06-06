variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "rg-insurance-fraud-detection"
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "East US"
}

variable "prefix" {
  description = "Prefix for all resource names"
  type        = string
  default     = "ifd"
  validation {
    condition     = can(regex("^[a-z0-9]{2,6}$", var.prefix))
    error_message = "Prefix must be 2-6 characters long and contain only lowercase letters and numbers."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "cosmos_db_throughput" {
  description = "Throughput for Cosmos DB containers"
  type        = number
  default     = 400
  validation {
    condition     = var.cosmos_db_throughput >= 400 && var.cosmos_db_throughput <= 100000
    error_message = "Cosmos DB throughput must be between 400 and 100000."
  }
}

variable "app_service_sku" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "B1"
  validation {
    condition     = contains(["B1", "B2", "B3", "S1", "S2", "S3", "P1v2", "P2v2", "P3v2"], var.app_service_sku)
    error_message = "App Service SKU must be one of the supported tiers."
  }
}

variable "enable_monitoring" {
  description = "Enable Application Insights and Log Analytics"
  type        = bool
  default     = true
}

variable "storage_replication_type" {
  description = "Storage account replication type"
  type        = string
  default     = "LRS"
  validation {
    condition     = contains(["LRS", "GRS", "RAGRS", "ZRS"], var.storage_replication_type)
    error_message = "Storage replication type must be one of: LRS, GRS, RAGRS, ZRS."
  }
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
