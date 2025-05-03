output "sqs_queue_url" {
  value = aws_sqs_queue.guardian_content.id
}

output "lambda_function_name" {
  value = aws_lambda_function.guardian_stream.function_name
}