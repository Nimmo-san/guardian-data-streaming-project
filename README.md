# Guardian data streaming project

# Guardian Data Streaming Project

A Python-based serverless application that fetches relevant news articles from The Guardian API and publishes them to an AWS SQS message broker for further analysis or processing. Designed for integration in modern data platforms with AWS Lambda, SQS, and Secrets Manager.

---

## Features

- Searches Guardian articles using custom search terms and optional dates
- Publishes up to 10 results in JSON format to an SQS queue
- Extracts metadata and content previews (first 1000 characters)
- Designed for AWS Lambda with full CI/CD support
- Secrets securely retrieved from AWS Secrets Manager

---

## Architecture

```text
 Guardian API
     ↓
  Lambda
     ↓
 Articles as JSON
     ↓
  AWS SQS Queue 
```
## Project Structure

## Deployment

## Environment & Secrets

## Example Event Payload
```json
{
  "search_term": "machine learning",
  "date_from": "2024-01-01",
  "queue_url": "https://sqs.eu-west-2.amazonaws.com/123456789012/guardian_content"
}
```

## Sample Output Format (SQS Message)
```json
{
  "webPublicationDate": "2024-05-01T12:00:00Z",
  "webTitle": "AI and the Future of Work",
  "webUrl": "https://www.theguardian.com/...",
  "content_preview": "Artificial intelligence is changing the landscape of employment..."
}
```

## Contribution