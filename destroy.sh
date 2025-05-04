#!/bin/bash
set -e



# Vars
PROJECT_NAME="guardian-data-streaming-project"
TERRAFORM_DIR="./terraform"


echo -e "\n========================================="
echo " Starting Infrastructure Cleanup Process "
echo -e "=========================================\n"


if [ ! -f "./deploy.sh" ]; then
  echo "Run this script from the project root." >&2
  exit 1
fi

# Checking TF Dependency
if ! [ -x "$(command -v terraform )" ]; then
    echo "Terraform not installed. Install it first." >&2
    exit 1
fi

echo -e " ==> Terraform available!\n"

# TF Initialising
echo -e "==> Initialising Terraform!\n"
cd $TERRAFORM_DIR
terraform init

echo -e "==> Intialised Terraform! ✅ \n"

# Destroy TF Managed Resources
echo "==> Destroying Terraform-managed Resources..."
terraform destroy -auto-approve

echo "==> Cleanup Complete! All Terraform Resources Have Been Destroyed! ✅ "