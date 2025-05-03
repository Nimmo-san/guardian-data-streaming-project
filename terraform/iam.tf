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
        Effect = "Allow",
        Action = "sqs:SendMessage",
        Resource = aws_sqs_queue.guardian_content.arn
      },
      {
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