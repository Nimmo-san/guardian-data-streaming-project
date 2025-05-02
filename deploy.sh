#!/bin/bash
set -e


# Vars
PROJECT_NAME="guardian-data-streaming-project"
TERRAFORM_DIR="./terraform"


echo "============================================="
echo " Starting Infrastructure Deployment Process "
echo "============================================="


# Checking TF Dependency
if ! [ -x "$(command -v terraform )" ]; then
    echo "❌ Terraform not installed. Install it first." >&2
    exit 1
fi
echo -e "👉 Terraform available!\n"

# TF Initialising
echo -e "👉 Initialising Terraform!\n"
cd $TERRAFORM_DIR
terraform init

echo -e "Intialised Terraform! ✅ \n"


# Planning TF Config for TESTING
echo -e "👉 Planning Terraform Configuration..."
terraform plan 

# Applying TF Config
terraform apply -auto-approve


echo "Infrastructure Deployment Complete! ✅ "

