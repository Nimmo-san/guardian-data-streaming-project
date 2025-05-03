variable "aws_region" {
  default = "eu-west-2"
}

variable "lambda_function_name" {
  default = "guardian_stream_lambda"
}

variable "guardian_api_secret_name" {
  default = "guardian_api_key"
}

variable "python_runtime" {
  default = "python3.11"
}

variable "s3_bucket_prefix" {
  default = "gdsp"
}