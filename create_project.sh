#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

# Assign the first argument to a variable
PROJECT_NAME=$1

# Copy the template directory
cp -pr ./_template/ ./"$PROJECT_NAME"/

# Change into the newly created directory
cd "$PROJECT_NAME" || exit

# Confirm success
echo "Project '$PROJECT_NAME' has been created and moved into."
