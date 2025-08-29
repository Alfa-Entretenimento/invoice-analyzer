#!/bin/bash

# Deploy script for Invoice Analyzer - AWS Elastic Beanstalk
# Deploys Flask application to AWS

set -e  # Exit on any error

# Configuration
APP_NAME="invoice-analyzer"
ENV_NAME="invoice-analyzer-prod"
REGION="sa-east-1"  # São Paulo
PROFILE="alfabet"
BUCKET_NAME="alfa-invoice-analyzer"
CLOUDFRONT_DOMAIN=""  # Will be set after CloudFront creation

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=> Starting deployment for Invoice Analyzer System...${NC}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}[ERROR] AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${YELLOW}[WARNING] EB CLI is not installed. Installing...${NC}"
    pip3 install awsebcli --upgrade
fi

# Step 1: Create S3 bucket for static files if it doesn't exist
echo -e "${YELLOW}[S3] Creating S3 bucket for static files...${NC}"
aws s3api create-bucket \
    --bucket ${BUCKET_NAME} \
    --region ${REGION} \
    --profile ${PROFILE} \
    --create-bucket-configuration LocationConstraint=${REGION} 2>/dev/null || true

# Upload static files to S3
echo -e "${YELLOW}[S3] Uploading static files...${NC}"
aws s3 sync static/ s3://${BUCKET_NAME}/static/ \
    --profile ${PROFILE} \
    --exclude "*.DS_Store" \
    --acl public-read

# Step 2: Initialize Elastic Beanstalk application
echo -e "${YELLOW}[EB] Initializing Elastic Beanstalk application...${NC}"

# Create .ebignore file
cat > .ebignore << EOF
venv/
*.pdf
notas/
.git/
*.pyc
__pycache__/
test*.py
debug*.py
analise*.py
CHANGELOG.md
relatorio*
scripts/
EOF

# Create Procfile for Elastic Beanstalk
cat > Procfile << EOF
web: gunicorn app:app --bind 0.0.0.0:8000 --timeout 120
EOF

# Update requirements.txt with gunicorn
if ! grep -q "gunicorn" requirements.txt; then
    echo "gunicorn==21.2.0" >> requirements.txt
fi

# Initialize EB
eb init ${APP_NAME} \
    --region ${REGION} \
    --platform "Python 3.9" \
    --profile ${PROFILE} -p python-3.9

# Step 3: Create/Update environment
echo -e "${YELLOW}[EB] Creating/updating environment...${NC}"
eb create ${ENV_NAME} \
    --instance-type t3.small \
    --profile ${PROFILE} \
    --region ${REGION} \
    --timeout 30 \
    || eb deploy ${ENV_NAME} --profile ${PROFILE}

# Step 4: Get the application URL
APP_URL=$(eb status ${ENV_NAME} --profile ${PROFILE} | grep "CNAME:" | cut -d' ' -f2)

echo ""
echo -e "${GREEN}[SUCCESS] Application deployed successfully!${NC}"
echo ""
echo -e "${BLUE}[URL] Your application is available at:${NC}"
echo -e "      http://${APP_URL}"
echo ""

# Step 5: Create CloudFront distribution
echo -e "${YELLOW}[CloudFront] Creating CloudFront distribution...${NC}"

# Create CloudFront configuration
cat > cloudfront-config.json << EOF
{
    "CallerReference": "${APP_NAME}-$(date +%s)",
    "Aliases": {
        "Quantity": 0
    },
    "DefaultRootObject": "",
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "${APP_NAME}-eb",
                "DomainName": "${APP_URL}",
                "CustomOriginConfig": {
                    "HTTPPort": 80,
                    "HTTPSPort": 443,
                    "OriginProtocolPolicy": "http-only",
                    "OriginSslProtocols": {
                        "Quantity": 3,
                        "Items": ["TLSv1", "TLSv1.1", "TLSv1.2"]
                    }
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "${APP_NAME}-eb",
        "ViewerProtocolPolicy": "redirect-to-https",
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        },
        "ForwardedValues": {
            "QueryString": true,
            "Cookies": {
                "Forward": "all"
            },
            "Headers": {
                "Quantity": 1,
                "Items": ["*"]
            }
        },
        "MinTTL": 0,
        "DefaultTTL": 0,
        "MaxTTL": 0
    },
    "Comment": "Invoice Analyzer CloudFront Distribution",
    "Enabled": true
}
EOF

# Create CloudFront distribution
DISTRIBUTION_OUTPUT=$(aws cloudfront create-distribution \
    --distribution-config file://cloudfront-config.json \
    --profile ${PROFILE} \
    --output json 2>/dev/null || echo "{}")

if [ ! -z "$DISTRIBUTION_OUTPUT" ] && [ "$DISTRIBUTION_OUTPUT" != "{}" ]; then
    CLOUDFRONT_ID=$(echo $DISTRIBUTION_OUTPUT | grep -o '"Id":"[^"]*"' | cut -d'"' -f4)
    CLOUDFRONT_DOMAIN=$(echo $DISTRIBUTION_OUTPUT | grep -o '"DomainName":"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${GREEN}[SUCCESS] CloudFront distribution created${NC}"
    echo -e "${BLUE}[CloudFront] Distribution ID: ${CLOUDFRONT_ID}${NC}"
    echo -e "${BLUE}[CloudFront] Domain: https://${CLOUDFRONT_DOMAIN}${NC}"
else
    echo -e "${YELLOW}[WARNING] CloudFront distribution may already exist or creation failed${NC}"
fi

# Clean up
rm -f cloudfront-config.json

echo ""
echo -e "${GREEN}[DONE] Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}=> Application URLs:${NC}"
echo -e "   Elastic Beanstalk: http://${APP_URL}"
if [ ! -z "$CLOUDFRONT_DOMAIN" ]; then
    echo -e "   CloudFront (HTTPS): https://${CLOUDFRONT_DOMAIN}"
fi
echo ""
echo -e "${YELLOW}[NOTE] CloudFront distribution may take 15-20 minutes to be fully deployed.${NC}"
echo ""

# Optional: Open the website
read -p "[PROMPT] Open the application in browser? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        open "http://${APP_URL}"
    else
        echo -e "${YELLOW}[INFO] Please manually open: http://${APP_URL}${NC}"
    fi
fi

echo -e "${GREEN}[ALFA] Invoice Analyzer deployed for Alfa Entretenimento!${NC}"