#!/bin/bash
# Script to start the Flask application with Cosmos DB integration

# Source the Cosmos DB environment variables
echo "Setting up Cosmos DB environment variables..."
source "$(dirname "$0")/setup_cosmos_env.sh"

# Start the Flask application
echo "Starting Flask application..."
python "$(dirname "$0")/app.py"
