# Create S3 Code bucket
resource "aws_s3_bucket" "code_bucket" {
  bucket = "${var.s3_bucket_prefix}-code"
  tags = {
    Name = "gdsp_code_bucket"
  }
}

# Create Lambda deployment package from src
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/../packages/function.zip"
}

# Create Layer package for requests
data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${path.module}/../layer"
  output_path = "${path.module}/../packages/layer.zip"
}

# Upload Lambda function ZIP to S3
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "function.zip"
  source = data.archive_file.lambda.output_path
  etag   = filemd5(data.archive_file.lambda.output_path)
}

# Upload Layer ZIP to S3
resource "aws_s3_object" "layer_zip" {
  bucket = aws_s3_bucket.code_bucket.id
  key    = "layer.zip"
  source = data.archive_file.layer.output_path
  etag   = filemd5(data.archive_file.layer.output_path)
}

# Define Lambda Layer for requests
resource "aws_lambda_layer_version" "requests_layer" {
  layer_name          = "requests_layer"
  compatible_runtimes = [ var.python_runtime ]
  s3_bucket           = aws_s3_bucket.code_bucket.bucket
  s3_key              = aws_s3_object.layer_zip.key
}

# Define the Lambda function
resource "aws_lambda_function" "guardian_stream" {
  function_name = "guardian_stream_lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  runtime       = var.python_runtime
  handler       = "main.lambda_handler"

  s3_bucket = aws_s3_bucket.code_bucket.id
  s3_key    = aws_s3_object.lambda_zip.key

  layers = [
    aws_lambda_layer_version.requests_layer.arn
  ]

  timeout     = 30
  memory_size = 256
}