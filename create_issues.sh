#!/bin/bash

# Create issues for auth-service

# Function to create an issue
create_issue() {
    local title=$1
    local body=$2
    local labels=$3
    
    echo "Creating issue: $title"
    gh issue create --title "$title" --body "$body" --label "$labels"
}

# Function to create a label if it doesn't exist
create_label() {
    local label_name=$1
    local label_color=$2
    local label_desc=$3
    
    # Check if label exists
    if ! gh label list | grep -q "^$label_name"; then
        echo "Creating label: $label_name"
        gh label create "$label_name" --color "$label_color" --description "$label_desc"
    else
        echo "Label $label_name already exists"
    fi
}

# Create labels
create_label "security" "e11d21" "Security related issues"
create_label "enhancement" "a2eeef" "New feature or request"
create_label "configuration" "c5def5" "Configuration related issues"
create_label "authentication" "5319e7" "Authentication related issues"

# Create issues
create_issue "Standardize configuration management" "Implement consistent configuration management using pydantic-settings across all services. Externalize all configurable values." "configuration,enhancement"
create_issue "Enhance JWT security" "Ensure JWT tokens are properly secured with strong secret keys and appropriate expiration times. Implement token refresh and revocation mechanisms." "security,authentication"
create_issue "Add comprehensive error handling" "Implement consistent error handling and logging across all authentication endpoints. Add proper HTTP status codes and error messages." "enhancement"

echo "All issues created for auth-service!"