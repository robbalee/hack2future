#!/bin/bash
# Script to set up Cosmos DB credentials as environment variables

# Find the Terraform directory relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
TERRAFORM_DIR="$SCRIPT_DIR/terraform"

# Go to the terraform directory
if [ -d "$TERRAFORM_DIR" ]; then
    cd "$TERRAFORM_DIR" || { echo "Failed to change directory to $TERRAFORM_DIR"; exit 1; }
else
    echo "Warning: Terraform directory not found at $TERRAFORM_DIR"
fi

# Get the Cosmos DB endpoint and key from Terraform outputs
echo "Retrieving Cosmos DB credentials from Terraform remote state..."

# Since we're using remote state in Azure Storage, get outputs directly
COSMOS_ENDPOINT=$(terraform output -raw cosmos_db_endpoint 2>/dev/null)
COSMOS_KEY=$(terraform output -raw cosmos_db_primary_key 2>/dev/null)

if [ -z "$COSMOS_ENDPOINT" ] || [ -z "$COSMOS_KEY" ]; then
    echo "Warning: Could not retrieve Cosmos DB credentials from Terraform outputs."
    echo "Make sure Terraform is initialized and you have access to the Azure Storage backend."
    echo "Try running: terraform init && terraform plan"
    exit 1
fi

# Export as environment variables
export COSMOS_ENDPOINT="$COSMOS_ENDPOINT"
export COSMOS_KEY="$COSMOS_KEY"

echo "Cosmos DB credentials set as environment variables:"
echo "COSMOS_ENDPOINT=$COSMOS_ENDPOINT"
echo "COSMOS_KEY=****${COSMOS_KEY: -4}"

# Return to the original directory
cd - > /dev/null

echo "You can now run the application with Cosmos DB integration."
echo "To use these variables in your current shell, run: source $(basename "$0")"
