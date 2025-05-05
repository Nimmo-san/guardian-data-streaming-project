# Guardian Data Streaming Project

A Python-based serverless application that fetches relevant news articles from The Guardian API and publishes them to an AWS SQS message broker for further analysis or processing. Designed for integration in modern data platforms with AWS Lambda, SQS, and Secrets Manager.

---

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Using the Makefile](#using-the-makefile)
- [Core Components](#core-components)
- [Testing](#testing)
- [Deployment](#deployment)
- [Example Event Payload](#example-event-payload)
- [Sample Output Format](#sample-output-format)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Features

- Searches Guardian articles using custom search terms and optional dates
- Publishes up to 10 results in JSON format to an SQS Queue
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

### Prerequisites 
Tools used
- **Python 3.11.x**: For the Lambda functions and local development
- **Terraform**: Infrastructure as Code for AWS resource provisioning
- **AWS**: Lambda, CloudWatch, Secrets Manager
- **boto3**: Python AWS SDK for interacting with AWS Services

## Project Setup
To setup the project, follow these steps
1. Clone the repo
```sh
git clone https://github.com/Nimmo-san/guardian-data-streaming-project.git
cd Guardian-Data-Streaming-Project
```
2. 

## Using the Makefile

### Makefile Commands

- **Environment Setup**
  - `make create-environment`: Creates a virtual environment.
  - `make requirements`: Installs project dependencies from requirements.txt

- **Development Setup**
  - `make dev-setup`: Installs bandit, black, flake8, and coverage tools.
  
- **Testing & Code Quality**
  - `make run-bandit`: Run Bandit for security checks.
  - `make run-black`: Formats code with Black.
  - `make run-flake8`: Lints code with Flake8.
  - `make run-test`: Runs all tests using pytest.
  - `make check-coverage`: Runs tests with coverage reporting.
  - `make run-checks`: Executes all checks: formatting, linting, tests, and coverage.

- **Clean Up**
  - `make clean`: Removes the virtual environment, .coverage, .pytest_cache and Python bytecode (pycache)

## Core Components

### 'src/'
| Module/File         | Description |
|----------------------|-------------|
| `main.py`           | Entry point for the Lambda function. Parses input (from an AWS event), retrieves articles, and publishes them to the SQS message broker. |
| `guardian_api.py`   | Contains logic for calling The Guardian Content API using a search term and optional date filter. Returns a list of up to 10 structured articles with a content preview. |
| `message_broker.py` | Publishes articles as JSON messages to an AWS SQS queue. Handles message formatting and delivery. |

### SQS
- **SQS Queue (`guardian_content`)**:
  - Stores up to 10 articles per run as JSON messages.
  - Message retention is limited to **3 days** to comply with minimal data storage requirements and keep the system stateless.

## Testing 
1. Unit Testing
    - Verifying each function's logic with pytest
2. Integration Testing
    - Testing the entire pipeline by triggering events and verifying outputs in the SQS Queue


## Deployment

1. Run script from root folder
```sh
./deploy.sh
    Note: exec permission needs to be given
```
2. Verify resources in AWS
    - Check Lambda function, SQS Queue, and Cloudwatch Logs


## Example Event Payload
```json
{
  "search_term": "machine learning",
  "date_from": "2024-01-01",
  "queue_url": "https://sqs.eu-west-2.amazonaws.com/123456789012/guardian_content"
}
```

## Sample Output Format 
### SQS Message format
```json
{
  "webPublicationDate": "2024-05-01T12:00:00Z",
  "webTitle": "AI and the Future of Work",
  "webUrl": "https://www.theguardian.com/...",
  "content_preview": "Artificial intelligence is changing the landscape of employment..."
}
```

## Future Improvements

### Infrastructure

- **EventBridge Scheduler**: Automate Lambda execution to run hourly/daily.
- **Dead Letter Queue (DLQ)**: Add an SQS DLQ for better error handling, message durability, and logging failed messages.
- **Monitoring & Alerts**: Integrate with CloudWatch Alarms or AWS SNS to notify on Lambda failures or high error rates.

### Functionality 

- **Content Sentiment Analysis**: Add a Lambda consumer or post-processor that analyses article sentiment or topic classification.
- **Support for More Fields**: Extend message structure to include section names, author(s), tags, etc.
- **Terraform Variable Flexibility**: Make message retention period configurable via Terraform variables for flexibility across environments.


### Packaging

- **Lambda Container Image**: Package the application as a Docker container for more dependency flexibility.

## Contributing

Thanks for your interest in contributing! This project welcomes improvements, ideas, and bug fixes.
