# Cloud Diary ☁️📓

A secure serverless diary application built using:

- Amazon Cognito (Authentication)
- API Gateway (Routing + JWT Authorizer)
- AWS Lambda (Business Logic)
- DynamoDB (Storage)
- S3 (Frontend Hosting)

## Architecture

S3 → Cognito → API Gateway → Lambda → DynamoDB

## Setup

1. Create Cognito User Pool
2. Create API Gateway HTTP API with JWT Authorizer
3. Deploy Lambda
4. Create DynamoDB table:
   - Partition Key: UserID (String)
   - Sort Key: EntryID (String)
5. Update frontend config section with your values

## Security

- JWT authentication
- User-level data isolation
- Serverless architecture
