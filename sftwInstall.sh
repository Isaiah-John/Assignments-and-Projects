#!/bin/bash

# This script installs Git and checks for successful installation.

# Update package index
echo "Updating package index..."
sudo apt update -y

# Install git
echo "Installing Git..."
sudo apt install -y git

# Check if git was installed successfully
if command -v git >/dev/null 2>&1; then
  echo "Git installed successfully!"
  git --version
else
  echo "Git installation failed."
  exit 1
fi
