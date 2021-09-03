# Web scraper tool
API for web domain scraping with parameter based filtering

## Notable dependencies:
- Blueprint via Flask
- jwt via PyJWT
- DynamoDB via flask-dynamo and boto3

## Models:

### General
- 
### Connectors
- 

## Dev API Key:
- f4379a7f-3635-446c-bd25-6a0bc36f21b5

## Runs at:
http://0.0.0.0:5000/

## Run in development mode: 
docker run -dt --name=yellow-box-softwareapi -v $PWD:/app -p 5000:5000 -e 'WORK_ENV=DEV' yellow-box-softwareapi

## Run in production mode:
docker run -dt --restart=always --name=yellow-box-softwareapi -p 5000:5000 -e 'WORK_ENV=PROD' yellow-box-softwareapi

## Current docs:
https://documenter.getpostman.com/

## Run DynamoDB locally:
docker run -d -p 8000:8000 amazon/dynamodb-local

### Ensure DynamoDB is running:
nc -z localhost 8000

### Check DynamoDB tables:
aws dynamodb list-tables --endpoint-url http://localhost:8000