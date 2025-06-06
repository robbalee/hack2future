#!/bin/bash

# Terraform Remote State Setup Script
# This script helps team members set up access to the remote Terraform state
# Updated: June 6, 2025 - Remote state is now configured and working

set -e

echo "🚀 Setting up Terraform Remote State Environment..."
echo "📍 State Location: secondstorageeu/tfstate/insurance-fraud-detection.tfstate"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Get the storage account key
echo "🔑 Retrieving storage account access key..."
ARM_ACCESS_KEY=$(az storage account keys list \
  --resource-group hack2future \
  --account-name secondstorageeu \
  --query '[0].value' -o tsv)

if [ -z "$ARM_ACCESS_KEY" ]; then
    echo "❌ Failed to retrieve storage account key"
    exit 1
fi

echo "✅ Storage account key retrieved"

# Export the environment variable
export ARM_ACCESS_KEY="$ARM_ACCESS_KEY"

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Verify state access
echo "📋 Verifying remote state access..."
terraform state list

echo "✅ Terraform initialized successfully!"
echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "💡 Current imported resources:"
terraform state list | sed 's/^/   ✅ /'
echo ""
echo "💡 To use Terraform commands in new sessions, set:"
echo "   export ARM_ACCESS_KEY=\"$ARM_ACCESS_KEY\""
echo ""
echo "📋 Available commands:"
echo "   terraform plan     - See what changes will be made"
echo "   terraform apply    - Apply changes to infrastructure"
echo "   terraform state    - Manage state operations"
echo "   terraform state list - List all resources in state"
echo ""
