# Create SQS 
resource "aws_sqs_queue" "guardian_content" {
  name = "guardian_content"
  message_retention_seconds = 259200  # 3 days
}

# Create IAM Role for Lambda execution 
resource "aws_iam_role" "lambda_exec_role" {
  name = "guardian_lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# Create IAM Policy for Lambda
resource "aws_iam_policy" "lambda_policy" {
  name = "guardian_lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    # Log group permissions
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      {
        # SQS permission
        Effect = "Allow",
        Action = "sqs:SendMessage",
        Resource = aws_sqs_queue.guardian_content.arn
      },
      {
        # SSM permission
        Effect = "Allow",
        Action = "secretsmanager:GetSecretValue",
        Resource = "*"
      }
    ]
  })
}

# Attach IAM Policy to Lambda
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Lambda log group removal with tf destroy
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.guardian_stream.function_name}"
  retention_in_days = 3 # Holds log data for 3 days
  lifecycle {
    prevent_destroy = false
  }
}