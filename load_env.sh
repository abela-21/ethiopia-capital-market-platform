#!/bin/bash

# Exit on error
set -e

ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
    # Export all variables
    set -a
    source "$ENV_FILE"
    set +a
    
    # Replace ${PWD} with actual path
    export DATABASE_URL="${DATABASE_URL/\$\{PWD\}/$PWD}"
    
    echo "✅ Environment variables loaded successfully"
    echo "Environment Check:"
    echo "----------------"
    echo "FLASK_ENV: $FLASK_ENV"
    echo "DATABASE_URL: $DATABASE_URL"
    echo "JWT_SECRET_KEY: $JWT_SECRET_KEY"
    echo "PORT: $PORT"
    echo "FLASK_APP: $FLASK_APP"
else
    echo "❌ .env file not found"
    exit 1
fi