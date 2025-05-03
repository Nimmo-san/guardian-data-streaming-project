terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }

# GDSP - guardian data streaming project
  # backend "s3" {
  #   bucket = "gdsp-backend-tfstate"
  #   key = "tfstate/terraform.tfstate"
  #   region = "eu-west-2"
  # }
}


data "aws_caller_identity" "current" {}
data "aws_region" "current" {}