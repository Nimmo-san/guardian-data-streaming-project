#!/bin/bash
set -e


# Vars
PROJECT_NAME="guardian-data-streaming-project"
TERRAFORM_DIR="./terraform"



echo "============================================="
echo " Starting Infrastructure Deployment Process "
echo "============================================="


if [ ! -f "./deploy.sh" ]; then
  echo "Run this script from the project root." >&2
  exit 1
fi

# Checking TF Dependency
if ! [ -x "$(command -v terraform )" ]; then
    echo "Terraform not installed. Install it first." >&2
    exit 1
fi
echo -e "👉 Terraform available!\n"

# Building Lambda layer
echo -r "Installing Lambda layer dependencies into ./layer/python...\n"
mkdir -p layer/python
pip install --target layer/python requests

# TF Initialising
echo -e "Initialising Terraform!\n"
cd $TERRAFORM_DIR
terraform init

echo -e "Intialised Terraform! ✅ \n"


# Planning TF Config for TESTING
echo -e "Planning Terraform Configuration..."
terraform plan 

# Applying TF Config
terraform apply -auto-approve


echo -e "Infrastructure Deployment Complete! ✅ "

