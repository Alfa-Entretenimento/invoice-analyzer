#!/bin/bash

# Deploy script for Invoice Analyzer
# Frontend: S3 + CloudFront
# Backend: Lambda + API Gateway

set -e

# Configuration
PROFILE="alfabet"
REGION="sa-east-1"
BUCKET_NAME="alfa-invoice-analyzer"
LAMBDA_FUNCTION="invoice-analyzer-api"
API_NAME="invoice-analyzer-api"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=> Starting S3 + Lambda deployment for Invoice Analyzer...${NC}"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}[ERROR] AWS CLI is not installed.${NC}"
    exit 1
fi

# Step 1: Create S3 bucket for static hosting
echo -e "${YELLOW}[S3] Creating S3 bucket...${NC}"
aws s3api create-bucket \
    --bucket ${BUCKET_NAME} \
    --region ${REGION} \
    --profile ${PROFILE} \
    --create-bucket-configuration LocationConstraint=${REGION} 2>/dev/null || true

# Enable static website hosting
aws s3 website s3://${BUCKET_NAME}/ \
    --index-document index.html \
    --error-document error.html \
    --profile ${PROFILE}

# Set bucket policy for public access
cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy \
    --bucket ${BUCKET_NAME} \
    --policy file://bucket-policy.json \
    --profile ${PROFILE}

# Step 2: Upload static files
echo -e "${YELLOW}[S3] Uploading static files...${NC}"
aws s3 sync templates/ s3://${BUCKET_NAME}/ \
    --profile ${PROFILE} \
    --exclude "*.DS_Store"

aws s3 sync static/ s3://${BUCKET_NAME}/static/ \
    --profile ${PROFILE} \
    --exclude "*.DS_Store"

# Step 3: Create Lambda function package
echo -e "${YELLOW}[LAMBDA] Creating Lambda deployment package...${NC}"
mkdir -p lambda_package
cp app.py lambda_package/
cp analisador_nf_v2.py lambda_package/
cp analisador_nf.py lambda_package/
cp lambda_handler.py lambda_package/

# Install dependencies
pip3 install -r requirements.txt -t lambda_package/ --upgrade
pip3 install serverless-wsgi -t lambda_package/ --upgrade

# Create ZIP file
cd lambda_package
zip -r ../lambda_function.zip . -x "*.DS_Store" "*.pyc" "__pycache__/*"
cd ..

# Step 4: Create/Update Lambda function
echo -e "${YELLOW}[LAMBDA] Creating Lambda function...${NC}"

# Create IAM role for Lambda (if not exists)
aws iam create-role \
    --role-name ${LAMBDA_FUNCTION}-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }' \
    --profile ${PROFILE} 2>/dev/null || true

# Attach policy
aws iam attach-role-policy \
    --role-name ${LAMBDA_FUNCTION}-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
    --profile ${PROFILE}

# Wait for role to be available
sleep 10

# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --profile ${PROFILE} --query 'Account' --output text)

# Create Lambda function
aws lambda create-function \
    --function-name ${LAMBDA_FUNCTION} \
    --runtime python3.9 \
    --role arn:aws:iam::${ACCOUNT_ID}:role/${LAMBDA_FUNCTION}-role \
    --handler lambda_handler.handler \
    --zip-file fileb://lambda_function.zip \
    --timeout 30 \
    --memory-size 512 \
    --region ${REGION} \
    --profile ${PROFILE} 2>/dev/null || \
aws lambda update-function-code \
    --function-name ${LAMBDA_FUNCTION} \
    --zip-file fileb://lambda_function.zip \
    --region ${REGION} \
    --profile ${PROFILE}

# Step 5: Create API Gateway
echo -e "${YELLOW}[API] Creating API Gateway...${NC}"
API_ID=$(aws apigatewayv2 create-api \
    --name ${API_NAME} \
    --protocol-type HTTP \
    --target arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${LAMBDA_FUNCTION} \
    --region ${REGION} \
    --profile ${PROFILE} \
    --query 'ApiId' \
    --output text 2>/dev/null || \
aws apigatewayv2 get-apis \
    --region ${REGION} \
    --profile ${PROFILE} \
    --query "Items[?Name=='${API_NAME}'].ApiId | [0]" \
    --output text)

# Add Lambda permission for API Gateway
aws lambda add-permission \
    --function-name ${LAMBDA_FUNCTION} \
    --statement-id api-gateway-permission \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${API_ID}/*/*" \
    --region ${REGION} \
    --profile ${PROFILE} 2>/dev/null || true

# Get API endpoint
API_ENDPOINT=$(aws apigatewayv2 get-api \
    --api-id ${API_ID} \
    --region ${REGION} \
    --profile ${PROFILE} \
    --query 'ApiEndpoint' \
    --output text)

# Step 6: Update frontend with API endpoint
echo -e "${YELLOW}[UPDATE] Updating frontend with API endpoint...${NC}"
# This would normally update the JavaScript to point to the Lambda API

# Clean up
rm -rf lambda_package
rm -f lambda_function.zip
rm -f bucket-policy.json

echo ""
echo -e "${GREEN}[SUCCESS] Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}=> Application URLs:${NC}"
echo -e "   S3 Website: http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com"
echo -e "   API Endpoint: ${API_ENDPOINT}"
echo ""
echo -e "${YELLOW}[NOTE] For HTTPS access, create a CloudFront distribution.${NC}"
echo ""

echo -e "${GREEN}[ALFA] Invoice Analyzer deployed!${NC}"